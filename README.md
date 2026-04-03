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
