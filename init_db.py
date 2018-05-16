from app import create_app, db
from models.user import User, Role


app = create_app()

with app.app_context():
    db.create_all()

    user_test = User(email='test@test.com')
    db.session.add(user_test)
    db.session.commit()

