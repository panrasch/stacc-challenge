from flask import Flask, flash, redirect, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,SelectField,IntegerField,PasswordField,BooleanField,ValidationError,DateField
from wtforms.validators import DataRequired,EqualTo,Length
from datetime import datetime
from sqlalchemy import Enum
from enums import ChallengeType

# App
app = Flask(__name__)

# Config
app.secret_key = "secret"
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:admin@localhost/stacc'

# Initializing necessary classes
db = SQLAlchemy(app)
migrate = Migrate(app, db)
bcrypt = Bcrypt(app)

## Users class
# References table in MySQL database, holds info about users.
class Users(db.Model):
    __tablename__ = 'users'  # Set the table name explicitly
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(10), unique=True, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    date_registered = db.Column(db.DateTime, nullable=False)

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')
    
    @password.setter
    def password(self,password):
        self.password_hash = bcrypt.generate_password_hash(password)

    def verify_password(self,password):
        return bcrypt.check_password_hash(self.password_hash,password)

## Challenges class
# References table in MySQL database, holds info about challenges.
class Challenges(db.Model):
    __tablename__ = 'challenges'  # Set the table name explicitly
    challenge_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    challenge_type = db.Column(Enum('daily', 'weekly', 'monthly'), nullable=False)
    description = db.Column(db.Text)
    reward = db.Column(db.Integer)
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    user = db.relationship('Users', backref='challenges')

    def to_dict(self):
        return {
            'id': self.challenge_id,
            'name': self.name,
            'description': self.description,
            'challenge_type': self.challenge_type,
            'reward': self.reward,
            'user' : self.user_id
        }

## Transactions class
# Ref table in MySQL, holds info on transactions. 
class Transactions(db.Model):
    __tablename__ = 'transactions' # Set the table name explicitly
    id = db.Column(db.String(20), primary_key=True)
    date = db.Column(db.Date, nullable=False)
    description = db.Column(db.Text)
    amount = db.Column(db.Integer, nullable=False)
    currency = db.Column(db.String(3), nullable=False)
    account_id = db.Column(db.String(20), nullable=False, unique=True) # Should be foreign key referencing Account table ... 
    
## UserForm
# Prompts user with text boxes etc.
class UserForm(FlaskForm):
    username = StringField("Username:",validators=[DataRequired()])
    email = StringField("Email:",validators=[DataRequired()])
    password = PasswordField("Password:",validators=[DataRequired(),EqualTo('password2',message='Passwords Must Match!')])
    password2 = PasswordField("Repeat Password:",validators=[DataRequired()])
    submit = SubmitField("Submit")

## ChallengeForm
# Manually adding challenges with text boxes
class ChallengeForm(FlaskForm):
    name = StringField("Challenge name:",validators=[DataRequired()])
    challenge_type = SelectField("Challenge type:",choices=[(choice.name, choice.value) for choice in ChallengeType])
    description = StringField("Description:",validators=[DataRequired()])
    reward = IntegerField("Reward:",validators=[DataRequired()])
    # start_date = DateField("Start date:")
    # end_date = DateField("End date:")
    user_id = IntegerField("User:",validators=[DataRequired()])
    submit = SubmitField("Submit:")

## TransactionForm
# Form to input transactions.
class TransactionForm(FlaskForm):
    # date = DateField("Date:")
    description = StringField("Description:")
    amount = IntegerField("Amount:",validators=[DataRequired()])
    currency = StringField("Currency:",validators=[DataRequired()])
    account_id = StringField("Account:",validators=[DataRequired()])
    submit = SubmitField("Submit:")

# Displays list of users
@app.route('/users')
def list_users():
    users = Users.query.order_by(Users.date_registered)
    return render_template('users.html', users=users)

# Displays list of transactions
@app.route('/transactions')
def list_transactions():
    transactions = Transactions.query.order_by(Transactions.date)
    return render_template('transactions.html', transactions=transactions)

# Displays list of challenges
@app.route('/challenges')
def list_challenges():
    challenges = Challenges.query.all()
    return render_template('challenges.html', challenges=challenges)

# API route list of challenges in JSON response format
@app.route('/api/challenges', methods=['GET'])
def list_challenges_api():
    challenges = Challenges.query.all()

    challenge_data = [
        {
            "challenge_id": challenge.challenge_id,
            "name": challenge.name,
            "description": challenge.description,
            "challenge_type": challenge.challenge_type,
            "reward": challenge.reward,
            "start_date": challenge.start_date.strftime('%Y-%m-%d %H:%M:%S'),
            "end_date": challenge.end_date.strftime('%Y-%m-%d %H:%M:%S'),
            "user_id": challenge.user_id
        } for challenge in challenges
    ]
    return jsonify(challenges)

# API route challenges by challenge type in JSON response format
@app.route('/api/challenges/<challenge_type>', methods=['GET'])
def challenges_by_type(challenge_type):
    challenges = Challenges.query.filter_by(challenge_type=challenge_type).all()
    return jsonify([challenge.to_dict() for challenge in challenges])

# API route to list of users in JSON format
@app.route('/api/users')
def get_users():
    users = Users.query.all()
    user_list = [
        {
            'user_id': user.user_id,
            'username': user.username,
            'email': user.email,
            'date_registered': user.date_registered.strftime('%Y-%m-%d %H:%M:%S')
        }
        for user in users
    ]
    return jsonify(user_list)

# API route to list of transactions in JSON format
@app.route('/api/transactions')
def get_transactions():
    transactions = Transactions.query.all()
    transaction_list = [
        {
            'id': transaction.id,
            'date': transaction.date,
            'description' : transaction.description,
            'amount' : transaction.amount,
            'currency' : transaction.currency,
            'account_id' : transaction.account_id
        }
        for transaction in transactions
    ]
    return jsonify(transaction_list)

# Route used to add users
@app.route('/users/add', methods=['GET', 'POST'])
# Adds a user based on UserForm input
def add_user():
    form = UserForm()
    if request.method == 'POST' and form.validate_on_submit():
        nameCheck = Users.query.filter_by(username=form.username.data).first()
        emailCheck = Users.query.filter_by(email=form.email.data).first()
        if nameCheck is None and emailCheck is None:
            # Hash the password
            hashed_password = bcrypt.generate_password_hash(form.password.data)
            new_user = Users(
                username=form.username.data,
                email=form.email.data,
                password_hash=hashed_password,
                date_registered=datetime.now()
            )
            db.session.add(new_user)
            db.session.commit()
            return jsonify({
                "message": "User added successfully",
                "user_id": new_user.user_id,
                "status": "success"
            })
        else:
            print(nameCheck,emailCheck)
            return jsonify({
                "message": "User already exists with the provided username or email",
                "status": "error"
            }), 400
        form.username.data = ''
        form.email.data = ''
        form.password.data = ''
    # return jsonify({
    #     "message": "Invalid request method or validation failed",
    #     "status": "error"
    # }), 405
    return render_template('add_user.html',form=form)

# Route to add challenges
@app.route('/challenges/add', methods=['GET', 'POST'])
# Adds challenge based on ChallengeForm input
def add_challenge():
    form = ChallengeForm()
    if request.method == 'POST': # and form.validate_on_submit():
        userCheck = Users.query.filter_by(user_id=form.user_id.data).first()
        if userCheck != None:
            new_challenge = Challenges(
                name=form.name.data,
                challenge_type=form.challenge_type.data,
                description=form.description.data,
                reward=form.reward.data,
                start_date=datetime.now(),
                end_date=datetime.now(),
                user_id=form.user_id.data
            )
            db.session.add(new_challenge)
            db.session.commit()

        #     return jsonify({
        #         "message": "Challenge added successfully",
        #         "challenge_id": new_challenge.challenge_id,
        #         "challenge_type": new_challenge.challenge_type,
        #         "status": "success"
        #     })
        
        # else:
        #     return jsonify({
        #         "message": "User not found or invalid user ID",
        #         "status": "error"
        #     }), 400
        
        form.name.data = ''
        form.challenge_type.data = None
        form.description.data = ''
        form.reward.data = None
        form.user_id.data = ''

    # return jsonify({
    #     "message": "Invalid request method",
    #     "status": "error"
    # }), 405

    return render_template('add_challenge.html',form=form)

# Route to add transactions
@app.route('/transactions/add', methods=['GET', 'POST'])
def add_transaction():
    form = TransactionForm()
    if form.validate_on_submit():
        new_transaction = Transactions(
            date=datetime.now(), # Placeholder date
            description=form.description.data,
            amount=form.amount.data,
            currency=form.currency.data,
            account_id=form.account_id.data
        )
        db.session.add(new_transaction)
        db.session.commit()
    return render_template('add_transaction.html',form=form)

# Route for deleting users
@app.route('/delete/<int:id>')
def delete(id):
    user_to_delete = Users.query.get_or_404(id)

    try:
        db.session.delete(user_to_delete)
        db.session.commit()
        return redirect('/users')
        # return jsonify({message: "User Deleted Successfully!"})
    except:
        return redirect('/users')
        # return jsonify({message: "Error :p"}, 500)

# Route for deleting challenges
@app.route('/delete_challenge/<int:id>')
def delete_challenge(id):
    challenge_to_delete = Challenges.query.get_or_404(id)

    try:
        db.session.delete(challenge_to_delete)
        db.session.commit()
        return redirect('/challenges')
        # return jsonify({"message": "Challenge Deleted Successfully"})
    except:
        return redirect('/challenges')
        # return jsonify({"message": "Failed to delete the challenge"}, 500)

''' 
Back-end dibble dabbling stops here. 
'''