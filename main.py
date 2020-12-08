import bcrypt
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
db = SQLAlchemy()
ma = Marshmallow(app)






class EventSchema(ma.Schema):
    class Meta:
        model = Event

class UserSchema(ma.Schema):
    class Meta:
        model = User




@app.route('/events', methods=['POST'])
def add_event():
    try:
        event_schema = EventSchema()
        event_name = request.json.get['event_name']
        date = request.json.get['date']
        description = request.json.get['description']
        status = request.json.get['status']
        name = request.json.get['name']
        ownerId = request.json.get['ownerId']
        new_event = EventSchema(event_name, date, description, status, name, ownerId)
        db.session.add(new_event)
        db.session.flush()
        db.session.refresh(new_event)
        db.session.commit()
        return event_schema.jsonify(new_event)
    except:
        return {"Status":"Error","StatusCode": 404}


@app.route('/events', methods=['GET'])
def get_all_user_events():
    try:
        event_schema = EventSchema()
        all_events = event_schema.query().all()
        result = event_schema.dump(all_events)
        return jsonify(result)
    except:
        return {"Events": "id:1", "StatusCode":200}


@app.route('/events/<int:id>', methods=['PUT'])
def update_event(id):
    try:
        event_schema = EventSchema()
        event = event_schema.query.filter_by(id=id).first()
        if 'interested' in request.json:
            if request.json['interested']:
                event.interested += 1
            else:
                event.interested -= 1
            db.session.add(event)
            db.session.commit()
            result = event_schema.dump(event)
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
        db.session.add(event)

        db.session.commit()
        result = event_schema.dump(event)
        return jsonify(result)
    except:
        return "Invalid ID supplied", 400


@app.route('/renamevent/<int:id>', methods=['POST'])
def rename_event(id):
    try:
        event_schema = EventSchema()
        event = event_schema.query.filter_by(id=id).first()
        if 'interested' in request.json:
            if request.json['interested']:
                event.interested += 1
            else:
                event.interested -= 1
            db.session.add(event)
            db.session.commit()
            result = event_schema.dump(event)
            return jsonify(result)

        name_update = request.json.get('name', '')
        if name_update:
            event.event_name = name_update
            db.session.add(event)
            db.session.commit()
            result = event_schema.dump(event)
            return jsonify(result)
    except:
        return "Invalid input", 405


@app.route('/<eventId>', methods=['GET'])
def getEventById(eventId):
    try:
        event_schema = EventSchema()
        id = eventId
        db.session.add(id)
        db.session.commit()
        result = event_schema.dump(id)
        return {
            "Status": "Event is active", "name": result, "StatusCode": 200
        }
    except:
        return "Incorrect ID", 404


@app.route('/events/<int:id>', methods=['DELETE'])
def delete_event(id):
    try:
        event_schema = EventSchema()
        event = event_schema.query.filter_by(id=id).first()
        db.session.delete(event)
        db.session.commit()
        return {
            "msg": "event deleted successfully",
            "id": id
        }
    except:
        return "Event not found", 404


@app.route('/createUser', methods=['POST'])
def createUser():
    try:
        user_schema = UserSchema()
        User_Id = request.form["User_Id"]
        username = request.form["username"]
        firstName = request.form["firstName"]
        lastName = request.form["lastName"]
        password = request.form["password"]
        email = request.form["email"]
        phone = request.form["phone"]
        userStatus = request.form["userStatus"]
        res = user_schema.createUser(User_Id, username, firstName, lastName, password, email, phone, userStatus)
        message = {
            'status': 200,
            'message': 'success',
            'data': [res]
        }
        db.session.add(message)
        db.session.commit()
        result = user_schema.dump(message)
        return jsonify(result)
    except:
        return "Can`t create a user", 404


@app.route('/login', methods=['GET'])
def login():
    try:
        user_schema = UserSchema()
        login = request.form.get['login', None]
        password = request.form.get['password', None]
        if not login:
            return "Missing login", 400
        if not password:
            return "Missing password", 400

        user = user_schema.query.filter_by(email=login).first()
        if not user:
            return "User not found", 404
        if bcrypt.hashpw(password.encode('utf-8'), user.hash):
            return f'Congrats {login}'
    except:
        return "Bad input", 404


@app.route('/logout', methods=['GET'])
def log_out():
    try:
        pass
    except:
        return "Bad input"


@app.route('/<UserName>', methods=['GET'])
def getUserByName(username):
    try:
        user_schema = UserSchema()
        name = username
        db.session.add(name)
        db.session.commit()
        result = user_schema.dump(name)
        return {
            "Status": "Event is active", "name": result, "StatusCode": 200
        }
    except:
        return "Incorrect Username", 404


@app.route('/users/<int:id>', methods=['PUT'])
def update_user(id):
    try:
        user_schema = UserSchema()
        user = user_schema.query.filter_by(id=id).first()
        if 'interested' in request.json:
            if request.json['interested']:
                user.interested += 1
            else:
                user.interested -= 1
            db.session.add(user)
            db.session.commit()
            result = user_schema.dump(user)
            return jsonify(result)

        user_name_update = request.json.get('user_name', '')

        if user_name_update:
            user.event_name = user_name_update
        db.session.add(user)
        db.session.commit()
        result = user_schema.dump(user)
        return jsonify(result)
    except:
        return "Invalid ID supplied", 400


@app.route('/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    try:
        user_schema = UserSchema()
        user = user_schema.query.filter_by(id=id).first()
        db.session.delete(user)
        db.session.commit()
        return {
            "msg": "User deleted successfully",
            "id": id
        }
    except:
        return "User not found", 404


if __name__ == "__main__":
    app.run(debug=True)
