from app import app, db, Users
from datetime import datetime

with app.app_context():
    for i in range(1, 21):
        new_user = Users(
            username=f'user{i}',
            email=f'user{i}@mail.com',
            password_hash='root',
            date_registered=datetime.now()
        )

        # Add the user to the database session
        db.session.add(new_user)

    # Commit all the changes at once
    db.session.commit()

