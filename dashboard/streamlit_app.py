"""Streamlit dashboard for the ADAPTY InBody Intelligence System."""

import os
from typing import Any

import pandas as pd
import requests
import streamlit as st

from app.db.seed import get_synthetic_clients, get_synthetic_records
from app.services.progress_analyzer import build_progress_summary

API_BASE_URL = os.getenv("ADAPTY_API_BASE_URL", "http://127.0.0.1:8000")


def _api_get(path: str) -> Any:
    """Read JSON from the API."""
    response = requests.get(f"{API_BASE_URL}{path}", timeout=2)
    response.raise_for_status()
    return response.json()


@st.cache_data(ttl=30)
def load_data() -> tuple[pd.DataFrame, pd.DataFrame, bool]:
    """Load data from the API with a synthetic fallback."""
    try:
        clients = _api_get("/clients?limit=100")
        records = _api_get("/inbody-records?limit=500")
        if clients:
            return pd.DataFrame(clients), pd.DataFrame(records), True
    except requests.RequestException:
        pass

    synthetic_clients = []
    synthetic_records = []
    records_by_email = get_synthetic_records()

    for index, client in enumerate(get_synthetic_clients(), start=1):
        client_row = {**client, "id": index}
        synthetic_clients.append(client_row)
        for record in records_by_email[str(client["email"])]:
            synthetic_records.append({**record, "client_id": index})

    return pd.DataFrame(synthetic_clients), pd.DataFrame(synthetic_records), False


def build_summary_for_client(
    clients_df: pd.DataFrame,
    records_df: pd.DataFrame,
    client_id: int,
) -> dict[str, Any]:
    """Build a dashboard summary for one client."""
    client_row = clients_df.loc[clients_df["id"] == client_id].iloc[0]
    client_records = (
        records_df.loc[records_df["client_id"] == client_id]
        .sort_values("measurement_date")
        .to_dict(orient="records")
    )
    summary = build_progress_summary(client_records, str(client_row["main_goal"]))
    return {
        "name": f"{client_row['first_name']} {client_row['last_name']}",
        "goal": client_row["main_goal"],
        "records": client_records,
        "summary": summary,
    }


def render_overview(clients_df: pd.DataFrame, records_df: pd.DataFrame) -> None:
    """Render portfolio MVP overview metrics."""
    most_common_goal = (
        clients_df["main_goal"].mode().iloc[0] if not clients_df.empty else "n/a"
    )

    latest_records = (
        records_df.sort_values("measurement_date").groupby("client_id").tail(1)
        if not records_df.empty
        else pd.DataFrame()
    )

    metric_columns = st.columns(5)
    metric_columns[0].metric("Clients", len(clients_df))
    metric_columns[1].metric("Records", len(records_df))
    metric_columns[2].metric(
        "Avg body fat",
        f"{latest_records['body_fat_percentage'].mean():.1f}%"
        if not latest_records.empty
        else "n/a",
    )
    metric_columns[3].metric(
        "Avg muscle",
        f"{latest_records['skeletal_muscle_mass_kg'].mean():.1f} kg"
        if not latest_records.empty
        else "n/a",
    )
    metric_columns[4].metric("Top goal", str(most_common_goal))


def render_client_profile(clients_df: pd.DataFrame, records_df: pd.DataFrame) -> int:
    """Render selected client profile and latest assessment."""
    client_names = {
        int(row["id"]): f"{row['first_name']} {row['last_name']}"
        for _, row in clients_df.iterrows()
    }
    selected_client_id = st.selectbox(
        "Client",
        options=list(client_names.keys()),
        format_func=lambda value: client_names[int(value)],
    )
    dashboard_summary = build_summary_for_client(
        clients_df,
        records_df,
        int(selected_client_id),
    )
    client_records = pd.DataFrame(dashboard_summary["records"])

    left_column, right_column = st.columns([1, 2])
    left_column.subheader(dashboard_summary["name"])
    left_column.write(f"Goal: {dashboard_summary['goal']}")
    left_column.write(f"Trend: {dashboard_summary['summary'].classification}")

    if not client_records.empty:
        latest = client_records.sort_values("measurement_date").iloc[-1]
        right_column.metric("Latest weight", f"{latest['weight_kg']:.1f} kg")
        right_column.metric("Latest body fat", f"{latest['body_fat_percentage']:.1f}%")
        right_column.metric(
            "Latest muscle mass",
            f"{latest['skeletal_muscle_mass_kg']:.1f} kg",
        )

    return int(selected_client_id)


def render_progress_charts(records_df: pd.DataFrame, client_id: int) -> None:
    """Render progress charts for one client."""
    client_records = records_df.loc[records_df["client_id"] == int(client_id)].copy()
    if client_records.empty:
        st.info("No records available.")
        return

    client_records["measurement_date"] = pd.to_datetime(
        client_records["measurement_date"]
    )
    chart_data = client_records.set_index("measurement_date")[
        [
            "weight_kg",
            "body_fat_percentage",
            "skeletal_muscle_mass_kg",
            "bmi",
        ]
    ]
    st.line_chart(chart_data)


def render_reports(clients_df: pd.DataFrame, records_df: pd.DataFrame, client_id: int) -> None:
    """Render a simple coach report."""
    dashboard_summary = build_summary_for_client(clients_df, records_df, int(client_id))
    summary = dashboard_summary["summary"]

    st.subheader("Coach Report")
    st.write(
        f"Weight change: {summary.weight_change_kg} kg. "
        f"Body fat change: {summary.body_fat_change_percentage} percentage points. "
        f"Skeletal muscle mass change: {summary.muscle_mass_change_kg} kg."
    )
    st.write(f"Classification: {summary.classification}")
    st.write("Next step: review consistency, recovery, training load, and nutrition targets.")


def main() -> None:
    """Render the Streamlit dashboard."""
    st.set_page_config(page_title="ADAPTY InBody", layout="wide")
    st.title("ADAPTY InBody Intelligence System")

    clients_df, records_df, using_api = load_data()
    st.caption("API data" if using_api else "Synthetic demo data")

    overview_tab, profile_tab, data_tab = st.tabs(["Overview", "Client", "Data"])

    with overview_tab:
        render_overview(clients_df, records_df)

    with profile_tab:
        selected_client_id = render_client_profile(clients_df, records_df)
        render_progress_charts(records_df, int(selected_client_id))
        render_reports(clients_df, records_df, int(selected_client_id))

    with data_tab:
        st.dataframe(clients_df, use_container_width=True, hide_index=True)
        st.dataframe(records_df, use_container_width=True, hide_index=True)


if __name__ == "__main__":
    main()
