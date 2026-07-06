# API Examples

Run the API:

```bash
uvicorn app.main:app --reload
```

## Health Check

```bash
curl http://127.0.0.1:8000/health
```

```json
{
  "status": "ok",
  "service": "ADAPTY InBody Intelligence System"
}
```

## Create Client

```bash
curl -X POST http://127.0.0.1:8000/clients \
  -H "Content-Type: application/json" \
  -d '{"first_name":"Alex","last_name":"Demo","email":"alex.demo@example.com","phone":"+1-555-0100","gender":"male","birth_date":"1990-05-20","main_goal":"fat_loss"}'
```

## Create InBody-Style Record

```bash
curl -X POST http://127.0.0.1:8000/clients/1/inbody-records \
  -H "Content-Type: application/json" \
  -d '{"measurement_date":"2026-01-05","weight_kg":88.0,"body_fat_percentage":28.0,"skeletal_muscle_mass_kg":34.0,"bmi":27.2,"visceral_fat_level":10,"basal_metabolic_rate":1780,"waist_hip_ratio":0.91}'
```

## Get Progress Summary

```bash
curl http://127.0.0.1:8000/clients/1/summary
```

## Get Coach Report

```bash
curl http://127.0.0.1:8000/clients/1/coach-report
```
