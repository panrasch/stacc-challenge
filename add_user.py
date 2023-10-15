from app import app, db, Users
from datetime import datetime

with app.app_context():
    # Create a new user
    new_user = Users(
        username='FakePerson',
        email='personfake@gmail.com',
        password_hash='root',
        date_registered=datetime.now()
    )

    # Add the user to the database session and commit the changes
    db.session.add(new_user)
    db.session.commit()

