from flask_bcrypt import *
from flask import Flask, jsonify
import hashlib
from flask_jwt import JWT, jwt_required, current_identity
from models import Event, User
from flask_restful import Api, request
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


app = Flask(__name__)
api = Api(app)
app.config['SECRET_KEY'] = 'super-secret'
engine = create_engine('postgresql://postgres:4412712345@localhost:5432/postgres')
Session = sessionmaker(bind=engine)
session = Session()



def authenticate(username, password):
    user = session.query(User).filter_by(username=username, password=hashlib.md5(password.encode()).hexdigest()).first()
    return user

def identity(payload):
    user_id = payload['identity']
    return session.query(User).filter_by(id=user_id).first()

jwt = JWT(app, authenticate, identity)

@app.route('/events', methods=['POST'])
@jwt_required()
def add_event():
    json = request.get_json()
    event_name = json["event_name"]
    date = json["date"]
    description = json["description"]
    status = json["status"]
    name = json["name"]
    new_event = Event(event_name =event_name , date=date, description=description, status=status,
                      name=name, ownerId=json['ownerId'])
    session.add(new_event)
    session.commit()
    current_identity.events.append(session.query(Event).filter_by(ownerId=json['ownerId']).first())
    return jsonify("Event created")





@app.route('/events/all', methods=['GET'])
@jwt_required()
def get_all_user_events():
    try:
        all_events = session.query(Event).all()
        return jsonify("All events for created users successfully returned",all_events)
    except:
        return "Error, you have not events", 404


@app.route('/events/update/<int:id>', methods=['PUT'])
@jwt_required()
def update_event(id):
    try:
        event = session.query(Event).filter_by(id=id).first()
        if event in current_identity.created_events:
            event_name_update = request.json.get('event_name', '')
            date_update = request.json.get('date', '')
            description_update = request.json.get('description', '')
            status_update = request.json.get('status', '')
            name_update = request.json.get('name', '')

            if event_name_update:
                event.event_name = event_name_update
            if date_update:
                event.date = date_update
            if description_update:
                event.description = description_update
            if status_update:
                event.status = status_update
            if name_update:
                event.name = name_update
            session.commit()
            return jsonify("Event was updated"), 202
        return 'Event does not belong to user', 404
    except:
        return "Invalid ID supplied", 403


@app.route('/renamevent/<int:id>', methods=['POST'])
@jwt_required()
def rename_event(id):
    try:
        event = session.query(Event).filter_by(id=id).first()
        if event in current_identity.events:
            name_update = request.json.get('event_name', '')
            if name_update:
                event.event_name = name_update
                session.commit()
                return jsonify("Event was renamed")
        return 'Event does not belong to user', 404
    except:
        return "Invalid input", 405


@app.route('/<int:eventId>', methods=['GET'])
@jwt_required()
def getEventById(eventId):
    try:
        event = session.query(Event).filter_by(id=eventId).first()
        if event is not None:
            return jsonify("Event found", "EventId: ")
    except:
        return jsonify("Incorrect ID"), 404



@app.route('/events/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_event(id):
    try:
        event = session.query(Event).filter_by(id=id).first()
        if event in current_identity.events:
            session.delete(event)
            session.commit()
            return {
                "msg": "event deleted successfully",
                "id": id
            }
        return 'Event does not belong to user', 404
    except:
        return "Event not found", 404


@app.route('/createUser', methods=['POST'])
def createUser():
    json = request.get_json()
    username = json["username"]
    firstName = json["firstName"]
    lastName = json["lastName"]
    password = json["password"]
    email = json["email"]
    phone = json["phone"]
    userStatus = json["userStatus"]
    password = hashlib.md5(password.encode()).hexdigest()

    session.add(User(username=username, firstName=firstName, lastName=lastName, password=password,
                     email=email, phone=phone, userStatus=userStatus))
    session.commit()
    message = {
        'status': 200,
        'message': 'success'
    }

    return jsonify(message)

@app.route('/users/<int:id>', methods=['PUT'])
@jwt_required()
def update_user(id):
    user = session.query(User).filter_by(id=id).first()
    if user == current_identity:
        username_update = request.json.get('username', '')
        firstName_update = request.json.get('firstName', '')
        lastName_update = request.json.get('lastName', '')
        password_update = request.json.get('password', '')
        email_update = request.json.get('email', '')
        phone_update = request.json.get('phone', '')
        userStatus_update = request.json.get('userStatus', '')

        if username_update:
            user.username = username_update
        if firstName_update:
            user.firstName = firstName_update
        if lastName_update:
            user.lastName = lastName_update
        if password_update:
            user.password = password_update
        if email_update:
            user.email = email_update
        if phone_update:
            user.phone = phone_update
        if userStatus_update:
            user.userStatus = userStatus_update
        session.commit()
        return jsonify("User was updated", "User_ID: ", id)
    return 'You don\'t have access', 404

@app.route('/users/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_user(id):
    try:
        user = session.query(User).filter_by(id=id).first()
        if user == current_identity:
            session.delete(user)
            session.commit()
            return {
                "msg": "User deleted successfully",
                "id": id
            }
        return 'You don\'t have access', 404
    except:
        return jsonify("User not found")