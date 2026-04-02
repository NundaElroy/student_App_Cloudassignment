"""
models.py - Database model for Student Task Tracker

This file defines the 'Task' table using SQLAlchemy ORM.
The same model works with both SQLite (local) and PostgreSQL (Railway).
"""

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone

# Create the SQLAlchemy database instance
# This will be initialized with the Flask app in app.py
db = SQLAlchemy()


class Task(db.Model):
    """
    Task model - represents a single student task.

    Fields:
        id          - Unique identifier (auto-incremented)
        title       - Short name of the task (required)
        description - Detailed description (optional)
        status      - Current status: 'Pending' or 'Completed'
        created_at  - Timestamp when the task was created
    """
    __tablename__ = 'tasks'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(20), nullable=False, default='Pending')
    created_at = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))

    def __repr__(self):
        return f'<Task {self.id}: {self.title} [{self.status}]>'
