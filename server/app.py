from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate

from models import db, Camper, Activity, Signup

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

# api = Api(app)


@app.route('/')
def index():
    response = make_response(
        {
            "message": "Hello Campers!"
        },
        200
    )
    return response

@app.route('/campers',methods = ['GET','POST'])
def campers():

    campers = Camper.query.all()
    if request.method == 'GET':
        campers_dict = [campers.to_dict() for campers in campers]

        response = make_response(
            campers_dict,
            200
        )
        return response
    
    elif request.method == 'POST':
        new_camper = Camper(
            name = request.get_json()['name'],
            age = request.get_json()['age']
        )
        db.session.add(new_camper)
        db.session.commit()

        camper_dict = new_camper.to_dict()
        response = make_response(
            camper_dict,
            201
        )
        return response

    else:
        response_body = {
            "message": "This record does not exist in our database. Please try again."
        }
        response = make_response(
            response_body,
            404
        )
        return response

@app.route('/campers/<int:id>',methods = ['GET'])
def campers_id(id):

    camper = Camper.query.filter(Camper.id == id).first()

    if request.method == 'GET':
        campers_dict = [camper.to_dict() for camper in camper]

        response = make_response(
            campers_dict,
            200
        )
        return response
    
    else:
        response_body = {
            "error": "Camper not found"
        }
        response = make_response(
            response_body,
            404
        )
        return response

@app.route('/activities',methods = ['GET','POST'])
def activities():

    activities = Activity.query.all()
    if request.method == 'GET':
        activity_dict = [activity.to_dict() for activity in activities]

        response = make_response(
            activity_dict,
            200
        )
        return response
    
    elif request.method == 'POST':
        # for attr in request.get_json():
        #     setattr(activities,attr,request.get_json['attr'])
        new_activity = Activity(
            name = request.get_json['name'],
            difficulty = request.get_json['difficulty']
        )
        db.session.add(new_activity)
        db.session.commit()

        activity_dict = new_activity.to_dict()

        response = make_response(
            activity_dict,
            201
        )

        return response

    else:
        response_body = {
            "message": "This record does not exist in our database. Please try again."
        }
        response = make_response(
            response_body,
            404
        )
        return response

@app.route('/activities/<int:id>',methods = ['GET','DELETE'])
def activities_id(id):
    activity = Activity.query.filter(Activity.id == id).first()

    if request.method == 'GET':
        activity_dict = activity.to_dict()

        response = make_response(
            activity_dict,
            200
        )
        return response
    
    elif request.method == 'DELETE':
        db.session.delete(activity)
        db.session.commit()

        
        response_dict = {'message': 'record successfully deleted'}

        response = make_response(
            jsonify(response_dict),
            200
        )

        return response
    
@app.route('/signups',methods = ['POST'])
def signups():
    if request.method == 'POST':
        new_signup = Signup(
            time = request.get_json()['time'],
            campers_id = request.get_json()['campers_id'],
            activity_id = request.get_json()['activity_id']
        )
        db.session.add(new_signup)
        db.session.commit()

        signup_dict = new_signup.to_dict()

        response = make_response(
            signup_dict,
            201
        )

        return response
    else:
        response_body = {
            "errors": ["validation errors"]
        }
        response = make_response(
            response_body,
            404
        )
        return response


if __name__ == '__main__':
    app.run(port=5555, debug=True)
