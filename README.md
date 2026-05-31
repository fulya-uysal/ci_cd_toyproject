# 🚀 CI/CD Learning Project

A hands-on project to learn CI/CD with Python + GitHub Actions.

## Project Structure

```
cicd-learning-project/
├── app/
│   └── main.py              # FastAPI application
├── tests/
│   └── test_main.py         # Pytest tests
├── .github/
│   └── workflows/
│       └── ci-cd.yml        # ← THE PIPELINE (read this!)
├── Dockerfile               # Containerizes the app
├── requirements.txt
└── README.md
```

## 🧠 The CI/CD Pipeline — 4 Stages

```
Push code
    │
    ▼
[1] LINT ──── checks code style
    │  (fails fast if messy)
    ▼
[2] TEST ──── runs pytest + coverage
    │  (fails if any test breaks)
    ▼
[3] BUILD ─── builds Docker image + smoke test
    │  (fails if container doesn't start)
    ▼
[4] DEPLOY ── only runs on main branch
              (simulated — replace with real deploy)
```

## ⚡ Quick Start (run locally)

```bash
# 1. Create a virtual environment
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the API
uvicorn app.main:app --reload

# 4. Run tests
pytest tests/ --cov=app -v

# 5. Run the linter
flake8 app/ tests/
```

## 🎓 Learning Exercises

Work through these in order. Each one teaches a CI/CD concept.

### Exercise 1 — Trigger the pipeline
1. Create a GitHub repo and push this project
2. Go to the **Actions** tab in GitHub
3. Watch the pipeline run automatically
4. **Concept learned**: pipelines trigger on git events

### Exercise 2 — Break a test intentionally
1. Open `app/main.py`
2. Change `"status": "healthy"` to `"status": "ok"` in `/health`
3. Push to GitHub
4. Watch the TEST job fail (lint passes, test fails)
5. Fix it and push again
6. **Concept learned**: CI catches regressions before they reach production

### Exercise 3 — Break the linter
1. Add a line with 200 characters to any file
2. Push and watch LINT fail (TEST never even starts)
3. Fix it
4. **Concept learned**: fail fast — don't waste time on later stages

### Exercise 4 — Feature branch workflow
1. Create a new branch: `git checkout -b feature/add-search`
2. Add a new endpoint to `app/main.py`
3. Write a test for it in `tests/test_main.py`
4. Push the branch — pipeline runs (but deploy is SKIPPED)
5. Open a Pull Request to main
6. Merge it — pipeline runs again, this time DEPLOY runs too
7. **Concept learned**: branch protection + deploy only from main

### Exercise 5 — Add a real deployment
Replace the `echo` commands in the deploy job with one of:
- **Fly.io**: `flyctl deploy` (free tier available)
- **Render**: auto-deploy via webhook
- **Your own server**: SSH + docker pull + docker restart

## 📖 Key CI/CD Vocabulary

| Term | What it means |
|------|--------------|
| **Pipeline** | The entire automated workflow |
| **Job** | One stage in the pipeline (lint, test, build, deploy) |
| **Step** | One command inside a job |
| **Artifact** | A file produced by the pipeline (e.g. coverage report) |
| **Runner** | The VM that executes your jobs (ubuntu-latest) |
| **Trigger** | The event that starts the pipeline (push, PR) |
| **needs:** | Makes one job wait for another to succeed first |
| **if:** | Conditionally runs a job (e.g. only on main branch) |
