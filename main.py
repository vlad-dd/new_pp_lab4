from flask_bcrypt import *
from flask import Flask, jsonify
from models import Event, User, RequestedUsers
from flask_restful import Api, request
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker



app = Flask(__name__)
api = Api(app)
engine = create_engine('postgresql://postgres:4412712345@localhost:5432/postgres')
Session = sessionmaker(bind=engine)
session = Session()


@app.route('/events', methods=['POST'])
def add_event():
    json = request.get_json()
    event_name = json["event_name"]
    date = json["date"]
    description = json["description"]
    status = json["status"]
    name = json["name"]
    ownerId = json["ownerId"]
    new_event = Event(event_name =event_name , date=date, description=description, status=status,
                      name=name, ownerId=ownerId)
    session.add(new_event)
    session.commit()
    message = {
        'status': 200,
        'message': 'success'
    }
    return jsonify(message)



@app.route('/events', methods=['GET'])
def get_all_user_events():
    try:
        all_events = session.query(Event).all()
        return jsonify("All events for created users successfully returned",all_events)
    except:
        return "Error, you have not events", 404


@app.route('/events/<int:id>', methods=['PUT'])
def update_event(id):
    try:
        event = session.query(Event).filter_by(id=id).first()
        if 'interested' in request.json:
            if request.json['interested']:
                event.interested += 1
            else:
                event.interested -= 1
            session.add(event)
            session.commit()
            return jsonify("Event was updated","Event_ID: ",id)

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
        session.add(event)
        session.commit()
        return jsonify("Event was updated","Event_ID: ",id)
    except:
        return "Invalid ID supplied", 400


@app.route('/renamevent/<int:id>', methods=['POST'])
def rename_event(id):
    try:
        event = session.query(Event).filter_by(id=id).first()
        if 'interested' in request.json:
            if request.json['interested']:
                event.interested += 1
            else:
                event.interested -= 1
            session.add(event)
            session.commit()
            return jsonify(event)
        name_update = request.json.get('event_name', '')
        if name_update:
            event.event_name = name_update
            session.add(event)
            session.commit()
            return jsonify("Event was renamed", id)
    except:
        return "Method not allowed", 405


@app.route('/<int:eventId>', methods=['GET'])
def getEventById(eventId):
    try:
        event = session.query(Event).filter_by(id=eventId).first()
        found = event
        session.add(found)
        session.commit()
        return jsonify("Event found", "EventId: ", eventId)
    except:
        return "Incorrect ID", 404


@app.route('/events/<int:id>', methods=['DELETE'])
def delete_event(id):
    try:
        event = session.query(Event).filter_by(id=id).first()
        session.delete(event)
        session.commit()
        return {
            "msg": "event deleted successfully",
            "id": id
        }
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
        password = generate_password_hash(password).decode('utf-8')

        session.add(User(username=username,firstName=firstName,lastName=lastName,password=password,
                               email=email,phone=phone,userStatus=userStatus))
        session.commit()
        message = {
            'status': 200,
            'message': 'success'
        }


        return jsonify(message)



@app.route('/login', methods=['GET'])
def login():
    pass

@app.route('/logout', methods=['GET'])
def log_out():
    pass



@app.route('/<string:username>', methods=['GET'])
def getUserByName(username):
    try:
        user = session.query(User).filter_by(username=username).first()
        found = user
        session.add(found)
        session.commit()
        return jsonify("User found","username of this user: ", username)
    except:
        return "Incorrect Username", 404


@app.route('/users/<int:id>', methods=['PUT'])
def update_user(id):
    user = session.query(User).filter_by(id=id).first()
    if 'interested' in request.json:
        if request.json['interested']:
            user.interested += 1
        else:
            user.interested -= 1
        session.add(user)
        session.commit()
        return jsonify("User was updated", "User_ID: ", id)

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
    session.add(user)
    session.commit()
    return jsonify("User was updated", "User_ID: ", id)


@app.route("/add_to_events", methods=['POST'])
def add_to_events():
    json = request.get_json()
    user_id = json["user_id"]
    event_id = json["event_id"]
    requested = RequestedUsers(user_id=user_id, event_id=event_id)
    session.add(requested)
    session.commit()
    return jsonify("User was added", 200)


@app.route('/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    try:
        user = session.query(User).filter_by(id=id).first()
        session.delete(user)
        session.commit()
        return {
            "msg": "User deleted successfully",
            "id": id
        }
    except:
        return "User not found", 404


if __name__ == "__main__":
    app.run(debug=True)
