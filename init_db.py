from app import create_app, db
from models.user import User

app = create_app()

with app.app_context():
    db.create_all()

    # user_test = User(email='test@test.com', password_hash='12345')
    # db.session.add(user_test)
    db.session.commit()
