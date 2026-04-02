"""
app.py - Main Flask application for Student Task Tracker

This is the entry point of the application. It configures the database
connection, defines all CRUD routes, and starts the Flask server.

Database Strategy:
    - LOCAL:  Uses SQLite (no setup needed)
    - RAILWAY: Uses PostgreSQL via DATABASE_URL environment variable
"""

import os
import logging
from flask import Flask, render_template, request, redirect, url_for, flash
from models import db, Task

# ---------------------------------------------------------------------------
# App Configuration
# ---------------------------------------------------------------------------

app = Flask(__name__)

# Secret key for flash messages (session security)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key')

# Database URL: use DATABASE_URL from Railway, or fall back to local SQLite
database_url = os.environ.get('DATABASE_URL', 'sqlite:///tasks.db')

# Railway PostgreSQL fix: Railway may provide 'postgres://' but SQLAlchemy
# requires 'postgresql://', so we replace it if needed.
if database_url.startswith('postgres://'):
    database_url = database_url.replace('postgres://', 'postgresql://', 1)

app.config['SQLALCHEMY_DATABASE_URI'] = database_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Suppress warning

# Initialize database with app
db.init_app(app)

# ---------------------------------------------------------------------------
# Logging Configuration (for monitoring evidence in coursework)
# ---------------------------------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s'
)
logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Create tables on first request (works for both SQLite and PostgreSQL)
# ---------------------------------------------------------------------------

with app.app_context():
    db.create_all()
    logger.info("Database tables created / verified successfully.")

# ---------------------------------------------------------------------------
# Routes - CRUD Operations
# ---------------------------------------------------------------------------


@app.route('/')
def index():
    """READ - Display all tasks on the homepage."""
    tasks = Task.query.order_by(Task.created_at.desc()).all()
    logger.info(f"Homepage loaded. Total tasks: {len(tasks)}")
    return render_template('index.html', tasks=tasks)


@app.route('/add', methods=['GET', 'POST'])
def add_task():
    """CREATE - Show add form (GET) or save a new task (POST)."""
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        description = request.form.get('description', '').strip()

        # Basic validation
        if not title:
            flash('Task title is required!', 'danger')
            return redirect(url_for('add_task'))

        new_task = Task(title=title, description=description)
        db.session.add(new_task)
        db.session.commit()

        logger.info(f"Task created: '{title}' (ID: {new_task.id})")
        flash('Task added successfully!', 'success')
        return redirect(url_for('index'))

    return render_template('add_task.html')


@app.route('/edit/<int:task_id>', methods=['GET', 'POST'])
def edit_task(task_id):
    """UPDATE - Show edit form (GET) or update existing task (POST)."""
    task = Task.query.get_or_404(task_id)

    if request.method == 'POST':
        task.title = request.form.get('title', '').strip()
        task.description = request.form.get('description', '').strip()
        task.status = request.form.get('status', 'Pending')

        if not task.title:
            flash('Task title is required!', 'danger')
            return redirect(url_for('edit_task', task_id=task_id))

        db.session.commit()

        logger.info(f"Task updated: '{task.title}' (ID: {task.id})")
        flash('Task updated successfully!', 'success')
        return redirect(url_for('index'))

    return render_template('edit_task.html', task=task)


@app.route('/complete/<int:task_id>')
def complete_task(task_id):
    """UPDATE - Mark a task as completed."""
    task = Task.query.get_or_404(task_id)
    task.status = 'Completed'
    db.session.commit()

    logger.info(f"Task completed: '{task.title}' (ID: {task.id})")
    flash('Task marked as completed!', 'success')
    return redirect(url_for('index'))


@app.route('/delete/<int:task_id>')
def delete_task(task_id):
    """DELETE - Remove a task from the database."""
    task = Task.query.get_or_404(task_id)
    task_title = task.title

    db.session.delete(task)
    db.session.commit()

    logger.info(f"Task deleted: '{task_title}' (ID: {task_id})")
    flash('Task deleted successfully!', 'success')
    return redirect(url_for('index'))


@app.route('/health')
def health_check():
    """Health check endpoint - useful for monitoring."""
    logger.info("Health check endpoint was called.")
    return {'status': 'healthy', 'app': 'Student Task Tracker'}, 200


# ---------------------------------------------------------------------------
# Run the app
# ---------------------------------------------------------------------------

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    logger.info(f"Starting Student Task Tracker on port {port}")
    app.run(host='0.0.0.0', port=port, debug=True)
