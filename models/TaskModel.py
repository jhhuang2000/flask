# encoding=utf8
from models import db, DbBase
from sqlalchemy import Column, Date, DateTime, Integer, String, Time
from sqlalchemy.schema import FetchedValue


class Task(DbBase):
    __tablename__ = 'task'

    id = db.Column(db.Integer, primary_key=True)
    em = db.Column(db.String(50, 'utf8_general_ci'), server_default=db.FetchedValue())
    city = db.Column(db.String(50, 'utf8_general_ci'), server_default=db.FetchedValue())
    room = db.Column(db.String(50, 'utf8_general_ci'), server_default=db.FetchedValue())
    date = db.Column(db.Date)
    start_time = db.Column(db.Time)
    end_time = db.Column(db.Time)
    pwd = db.Column(db.String(50, 'utf8_general_ci'), server_default=db.FetchedValue())
    account = db.Column(db.String(50), server_default=db.FetchedValue())
    status_text = db.Column(db.String(255, 'utf8_general_ci'), server_default=db.FetchedValue())
    created_at = db.Column(db.DateTime, server_default=db.FetchedValue())
    updated_at = db.Column(db.DateTime)
