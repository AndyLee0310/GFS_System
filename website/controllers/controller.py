from flask import Blueprint, render_template, url_for, request, redirect, flash
from flask_login import current_user
from sqlalchemy import *
from ..models import *
from .. import db
import datetime, json, re

def create_system_record(description):
    new_record = SystemRecord(user_id=current_user.id, description=description, record_date=datetime.datetime.now().strftime("%Y-%m-%d"), record_time=datetime.datetime.now().strftime("%H:%M:%S"))
    db.session.add(new_record)
    db.session.commit()