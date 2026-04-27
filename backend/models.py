from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from datetime import datetime, timezone, timedelta

# 东八区时区
EAST_8 = timezone(timedelta(hours=8))

class FileRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    filename = db.Column(db.String(255), nullable=False)
    original_name = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=True)
    analysis = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(20), nullable=False, default='pending')
    error_message = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(EAST_8))
    updated_at = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(EAST_8), onupdate=lambda: datetime.now(EAST_8))
