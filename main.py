import bcrypt
from flask_bcrypt import *
from flask import Flask, jsonify
from flask_marshmallow import Marshmallow
from models import Event, User, Column, String, Integer
from flask_restful import Api, request
from flask_sqlalchemy import SQLAlchemy
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
    return jsonify("Event created")





@app.route('/events', methods=['GET']) # =====================
def get_all_user_events():
    try:
        all_events = session.query(Event).all()
        return jsonify(all_events)
    except:
        return "Error, you have not events", 404


@app.route('/events/<int:id>', methods=['PUT'])#=========================================
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
            result = session.dump(event)
            return jsonify(result)

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
        result = session.dump(event)
        return jsonify(result)
    except:
        return "Invalid ID supplied", 400


@app.route('/renamevent/<int:id>', methods=['POST']) #=============================
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
            result = session.dump(event)
            return jsonify(result)

        name_update = request.json.get('name', '')
        if name_update:
            event.event_name = name_update
            session.add(event)
            session.commit()
            result = session.dump(event)
            return jsonify(result)
    except:
        return "Invalid input", 405


@app.route('/<int:eventId>', methods=['GET'])
def getEventById(eventId):
    try:
        id = eventId
        session.add(id)
        session.commit()
        return {
            "Status": "Event is active", "name": id, "StatusCode": 200
        }
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
        User_Id = json["id"]
        username = json["username"]
        firstName = json["firstName"]
        lastName = json["lastName"]
        password = json["password"]
        email = json["email"]
        phone = json["phone"]
        userStatus = json["userStatus"]
        password = generate_password_hash(password).decode('utf-8')

        session.add(User(id=User_Id,username=username,firstName=firstName,lastName=lastName,password=password,
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
    try:
        pass
    except:
        return "Bad input"


@app.route('/<string:username>', methods=['GET'])
def getUserByName(username):
    try:
        found = username
        session.add(found)
        session.commit()
        return {
            "Status": "User founded", "username": found, "StatusCode": 200
        }
    except:
        return "Incorrect Username", 404


@app.route('/users/<int:id>', methods=['PUT'])
def update_user(id):
    try:
        json = request.get_json()
        user = session.query(User).filter_by(id=id).first()
        username_upd = json['username', '']
        firstName_upd = json('firstName', '')
        lastName_upd = json('lastName', '')
        password_upd = json('password', '')
        email_upd = json('email', '')
        userStatus_upd = json('userStatus', '')
        if username_upd:
            user.username = username_upd
        if firstName_upd:
            user.firstName = firstName_upd
        if lastName_upd:
            user.lastName = lastName_upd
        if password_upd:
            user.password = password_upd
        if email_upd:
            user.email = email_upd
        if userStatus_upd:
            user.userStatus = userStatus_upd
        session.add(user)
        session.commit()
        return jsonify("User was updated", 200)
    except:
        return "Invalid ID supplied", 400


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
