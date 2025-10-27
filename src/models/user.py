from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Import the db instance from main.py
from main import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    visitor_id = db.Column(db.String(36), unique=True, nullable=False)
    ip_address = db.Column(db.String(50))
    city = db.Column(db.String(100))
    region = db.Column(db.String(100))
    country = db.Column(db.String(100))
    location = db.Column(db.String(100))
    browser = db.Column(db.String(100))
    os = db.Column(db.String(100))
    device = db.Column(db.String(100))
    first_seen = db.Column(db.DateTime, default=datetime.utcnow)
    last_seen = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<User {self.visitor_id}>'
    
    def to_dict(self):
        return {
            'id': self.visitor_id,
            'ip_address': self.ip_address,
            'city': self.city,
            'region': self.region,
            'country': self.country,
            'location': self.location,
            'browser': self.browser,
            'os': self.os,
            'device': self.device,
            'first_seen': self.first_seen.timestamp() if self.first_seen else None,
            'last_seen': self.last_seen.timestamp() if self.last_seen else None
        }
