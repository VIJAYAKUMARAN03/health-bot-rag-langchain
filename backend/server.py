from flask import Flask, request, jsonify
import pymongo
from datetime import datetime
from flask_cors import CORS
import json
from bson import json_util
from sentence_embeddings import get_response
# from pymongo import MongoClient

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes


# Connect to MongoDB
client = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = client["mydatabase"]
usercollection = mydb["users"]
healthcollection = mydb["user_health"]


@app.route('/register', methods=['POST'])
def register():
    # Extract user data from the request
    user_data = request.get_json()

    print(user_data)
    # Sample data validation
    if 'name' not in user_data or 'email' not in user_data or 'password' not in user_data \
            or 'phone' not in user_data or 'dob' not in user_data or 'height' not in user_data \
            or 'weight' not in user_data:
        return jsonify({'message': 'Incomplete user data'}), 200

    # Sample data
    data = {
        "name": user_data['name'],
        "email": user_data['email'],
        "password": user_data['password'],
        "phone": user_data['phone'],
        "address": user_data['address'],
        "blood_group": user_data['blood_group'],
        "gender": user_data['gender'],
        "dob": datetime.strptime(user_data['dob'], '%Y-%m-%d'),  # Assuming date format is YYYY-MM-DD
        "height": user_data['height'],  # in centimeters
        "weight": user_data['weight'],   # in kilograms
        "health_data":0
    }

    # Insert data into the collection
    usercollection.insert_one(data)

    # Return success response
    return jsonify({'message': 'User added successfully'}), 200

@app.route('/login', methods=['POST'])
def login():
    # Extract user data from the request
    user_data = request.get_json()

    print(user_data)

    # Sample data validation
    if 'email' not in user_data :
        return jsonify({'message': 'Email is missing'}), 200
    if 'password' not in user_data:
        return jsonify({'message': 'Password is missing'}), 200

    user = usercollection.find_one({'email':user_data['email']})
    print(user)
    if(user):
        print(user['password'] != user_data['password'])
        if(user['password'] != user_data['password']):
            return jsonify({'message': 'Wrong Password'}), 200
        
        return jsonify({'message': 'Logged in Successful'}), 200
    return jsonify({'message': 'User not found'}), 200


@app.route('/getHealth', methods=['GET'])
def getHealth():
    if 'email' not in request.args :
        return jsonify({'message': 'Email is missing'}), 200
    
    # Extract user data from the request
    email = request.args.get('email')

    print(email)

    # Sample data validation
    health = list(healthcollection.find({'email':email}))

    print(health)

    heart_rt = []
    bt = []
    bp = []
    bg=[]
    for h in health:
        heart_rt.append(h['heart_rate'])
        bt.append(h['body_temperature'])
        bp.append(h['respiratory_rate'])
        bg.append(h['blood_glucose'])

    print(heart_rt)
    if(health):
        health = json.loads(json_util.dumps(health))
        return jsonify({'heart_rate':heart_rt,'body_temperature':bt,'respiratory_rate':bp,'blood_glucose':bg}), 200
    
    return jsonify({'message': 'No user found or no health found'}), 200


@app.route('/chat', methods=['GET'])
def chat():

    if 'query' not in request.args :
        return jsonify({'message': 'Query is missing'}), 200
    # Extract user data from the request
    user_data = request.args.get('query')
    # user_data = request.form

    print(user_data)
    
    res = get_response(user_data)

    return jsonify({'message': res}), 200

        
if __name__ == '__main__':
    app.run(host="0.0.0.0",debug=True)