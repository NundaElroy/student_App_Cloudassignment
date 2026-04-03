# Student Task Tracker

A simple Flask web app for tracking student tasks, built for a Cloud Computing PaaS assignment. Deploys on **Railway** with **PostgreSQL**.

## Features
- View, Add, Edit, Delete tasks (full CRUD)
- Mark tasks as completed
- PostgreSQL on Railway / SQLite locally
- Environment variable security
- Logging for monitoring evidence

## Project Structure
```
cloud_student_tracker/
├── app.py              # Flask app + routes
├── models.py           # SQLAlchemy Task model
├── templates/
│   ├── base.html       # Base layout (Bootstrap 5)
│   ├── index.html      # Task list page
│   ├── add_task.html   # Add task form
│   └── edit_task.html  # Edit task form
├── static/
│   └── style.css       # Custom CSS
├── requirements.txt    # Python dependencies
├── Procfile            # Railway startup command
├── .env.example        # Environment variable template
└── .gitignore          # Files to exclude from Git
```

## Local Development

```bash
# 1. Create virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # Mac/Linux

# 2. Install dependencies
pip install -r requirements.txt

# 3. Copy environment config
cp .env.example .env

# 4. Run the app (uses SQLite locally)
python app.py
```
Open **http://localhost:5000** in your browser.

## Deploy to Railway

1. Push code to a **GitHub repository**
2. Go to [railway.app](https://railway.app) → **New Project** → **Deploy from GitHub Repo**
3. Select your repo
4. Add **PostgreSQL**: Click **+ New** → **Database** → **PostgreSQL**
5. Railway auto-sets `DATABASE_URL` — no manual config needed
6. Add `SECRET_KEY` in **Variables** tab
7. Railway auto-deploys on every `git push`

## Deployment Readiness Checklist (Before Railway)

Confirm these are true before you deploy:

- ✅ `requirements.txt` includes `flask`, `gunicorn`, `psycopg2-binary`, `flask-sqlalchemy`
- ✅ Startup command exists via `Procfile`:
  - `web: gunicorn --bind 0.0.0.0:$PORT app:app`
- ✅ Secrets are not hardcoded:
  - `SECRET_KEY` comes from environment variables
  - `DATABASE_URL` comes from environment variables
- ✅ No secrets committed:
  - `.env` is ignored (see `.gitignore`)
  - local DB files are ignored (`instance/`, `*.db`)

## Railway Variables (Environment Configuration)

Set these in Railway → **Service** → **Variables**:

- `SECRET_KEY` (required): random long string
- `DATABASE_URL` (auto-provided): created when you add Railway PostgreSQL

Notes:
- Locally you can use `.env` (copy from `.env.example`).
- On Railway, do not upload `.env` — use the Variables UI.

## Railway PostgreSQL Integration (Verify It Works)

After provisioning PostgreSQL on Railway:

1. Confirm `DATABASE_URL` exists in Railway Variables.
2. Open the deployed app public URL.
3. Perform a CRUD test on the deployed site:
   - Add 1–2 tasks
   - Edit a task
   - Mark a task as completed
   - Delete a task
4. Refresh the page to confirm data persists.

## CI/CD Proof (GitHub → Railway Auto Redeploy)

To capture evidence that Railway redeploys automatically:

1. Make a tiny visible change (example: change the footer text in `templates/base.html`).
2. Commit + push to GitHub.
3. In Railway, watch the **Deployments** tab start a new deployment.
4. Refresh the public URL and screenshot the visible change.

## Monitoring / Logging Evidence

This app logs key actions (homepage load, create/update/delete/complete, health check).

For coursework evidence:

- Open Railway → **Logs** and trigger actions on the site.
- Capture screenshots that show:
  - request/activity logs (INFO level)
  - a deployment log (build + start)

### Realistic Error to Document (Recommended)

Error: **App deploys but the public URL is unreachable**.

Common cause: Gunicorn not binding to Railway’s `$PORT`.

How to document + fix:

1. Screenshot Railway Logs showing the service started but traffic fails / port mismatch.
2. Fix `Procfile` to:
   - `web: gunicorn --bind 0.0.0.0:$PORT app:app`
3. Commit + push, then screenshot the successful redeploy and working URL.

## Screenshots Checklist (What to Capture)

Capture these for your report (minimum set):

- GitHub repo page (shows commits + files)
- Railway project dashboard (project + service)
- Railway Variables (show `DATABASE_URL` exists; do NOT expose full secret values)
- Railway PostgreSQL plugin/service page (shows it’s provisioned)
- Railway Deployments tab (auto redeploy after a push)
- Railway Logs (INFO logs from your app + successful start)
- Deployed app in browser:
  - task list page
  - add/edit/complete/delete actions

## Short Report Notes (Copy-Friendly)

### Deployment process
- Pushed code to GitHub and connected repo to Railway.
- Railway built the app and started it using Gunicorn (`Procfile`).
- Public URL provided by Railway was used to access the deployed app.

### Environment configuration
- Configuration is provided via Railway Variables (`SECRET_KEY`, `DATABASE_URL`).
- No secrets are committed to GitHub; `.env` is ignored locally.

### Database integration
- Railway PostgreSQL is provisioned and automatically provides `DATABASE_URL`.
- Flask-SQLAlchemy uses `DATABASE_URL` to connect and perform CRUD on a single `tasks` table.

### CI/CD
- Railway is connected to the GitHub repo.
- Every `git push` triggers an automatic redeploy, providing continuous delivery.

### Monitoring / logging
- App emits logs for key actions and health checks.
- Railway Logs provide evidence of app activity and deployment troubleshooting.

### Scalability awareness
- Stateless Flask app: multiple instances can be run behind Railway’s routing.
- Database is external (PostgreSQL), so scaling app instances doesn’t lose data.
- This is coursework-sized; for production you’d add migrations, auth, and better observability.

### Railway vs Heroku (comparison)
- Both are PaaS platforms that support GitHub-based deployments and managed Postgres.
- Railway has a modern UI and simple plugin-based databases; Heroku is more established with many buildpack conventions.
- Both use environment variables for config; both provide logs for debugging deployments.
