from app import db, app
from models import User, Task

with app.app_context():
    uq = db.session.query(User).filter_by(email='ticume@mailinator.com').first()
    print(uq.tasks)