from app import app,db,Challenges, Users
from datetime import date

# Script to add one challenge
with app.app_context():
    # Create a new challenge
    new_challenge = Challenges(
        name='Homemade Coffee',
        description='Avoid spending that 20kr on coffee; make your own!',
        start_date=date.today(),
        end_date=date(2023,10,10),
        user_id=1
    )

    # Add the user to the database session and commit the changes
    db.session.add(new_challenge)
    db.session.commit()
