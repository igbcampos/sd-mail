from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import uuid
import jwt
import datetime
from functools import wraps

app = Flask(__name__)

app.config['SECRET_KEY']='Th1s1ss3cr3t'
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.Integer)
    name = db.Column(db.String(128))
    email = db.Column(db.String(128), unique=True, nullable=False)
    password = db.Column(db.String(128))

class Email(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now)
    sender = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    receiver = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    subject = db.Column(db.String(256), nullable=False)
    body = db.Column(db.Text)

def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token = None

        if 'x-access-tokens' in request.headers:
            token = request.headers['x-access-tokens']

        if not token:
            return jsonify({'message': 'a valid token is missing'})

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
            current_user = User.query.filter_by(public_id=data['public_id']).first()
        except:
            return jsonify({'message': 'token is invalid'})

        return f(current_user, *args, **kwargs)

    return decorator

@app.route('/register', methods=['POST'])
def signup_user():  
    data = request.get_json()  

    if User.query.filter_by(email=data['email']).first():
        return jsonify({'message': 'email address not available'})

    hashed_password = generate_password_hash(data['password'], method='sha256')
    
    new_user = User(public_id=str(uuid.uuid4()), name=data['name'], email=data['email'], password=hashed_password) 
    db.session.add(new_user)  
    db.session.commit()    

    return jsonify({'message': 'registered successfully'})

@app.route('/login', methods=['GET', 'POST'])  
def login_user(): 
    auth = request.authorization   

    if not auth or not auth.username or not auth.password:  
        return make_response('missing auth data', 401, {'WWW.Authentication': 'Basic realm: "login required"'})    

    user = User.query.filter_by(email=auth.username).first()   
    if not user:
        return make_response('invalid email or password',  401, {'WWW.Authentication': 'Basic realm: "login required"'})
        
    if check_password_hash(user.password, auth.password):  
        token = jwt.encode({'public_id': user.public_id, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(days=7)}, app.config['SECRET_KEY'])  
        return jsonify({'token' : token.decode('UTF-8')}) 

    return make_response('invalid email or password',  401, {'WWW.Authentication': 'Basic realm: "login required"'})

@app.route('/me', methods=['GET'])
@token_required
def user_data(current_user):
    output = {}

    output['name'] = current_user.name
    output['email'] = current_user.email

    return jsonify(output)

@app.route('/emails', methods=['POST'])
@token_required
def send_email(current_user):
    data = request.get_json()
    receiver = User.query.filter_by(email=data['receiver']).first() 

    if not receiver:
        return jsonify({'message': 'receiver not found'})  

    new_email = Email(sender=current_user.id, receiver=receiver.id, subject=data['subject'], body=data['body']) 
    db.session.add(new_email)  
    db.session.commit()    

    return jsonify({'message': 'email sent'})

@app.route('/emails/received', methods=['GET'])
@token_required
def get_emails_received(current_user):
    emails = Email.query.filter_by(receiver=current_user.id).all()
    output = []

    for email in emails:
        email_data = {}
        sender = User.query.filter_by(id=email.sender).first() 
        email_data['created_at'] = email.created_at
        email_data['sender'] = sender.email
        email_data['receiver'] = current_user.email
        email_data['subject'] = email.subject
        email_data['body'] = email.body
        output.append(email_data)

    return jsonify({'emails' : output})

@app.route('/emails/sent', methods=['GET'])
@token_required
def get_emails_sent(current_user):
    emails = Email.query.filter_by(sender=current_user.id).all()
    output = []

    for email in emails:
        email_data = {}
        receiver = User.query.filter_by(id=email.receiver).first() 
        email_data['created_at'] = email.created_at
        email_data['sender'] = current_user.email
        email_data['receiver'] = receiver.email
        email_data['subject'] = email.subject
        email_data['body'] = email.body
        output.append(email_data)

    return jsonify({'emails' : output})
