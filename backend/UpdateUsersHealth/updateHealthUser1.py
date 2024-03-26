import pymongo
import random
import datetime
import time
from sendSMS import sendSMS
# MongoDB connection settings
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["mydatabase"]
healthcollection = db["user_health"]
usercollection = db["users"]
# Function to generate random health data
def generate_random_data():
    email = "vijay@gmail.com"
    user = usercollection.find_one({'email':email})
    if(user):
        print(user)
        count = user['health_data']
        usercollection.find_one_and_update({'email':email},{"$set":{'health_data':count+1}})
        data = {
            "count" : count,
            "timestamp": datetime.datetime.now(),
            "email" : email,
            "heart_rate": 10,#random.randint(50, 140),  # Random heart rate between 60 and 120 bpm
            "blood_pressure": {
                "systolic": random.randint(80, 150),  # Random systolic pressure between 90 and 140 mmHg
                "diastolic": random.randint(50, 100)   # Random diastolic pressure between 60 and 90 mmHg
            },
            "blood_glucose": round(random.uniform(60, 160), 1),  # Random blood glucose level between 70 and 140 mg/dL
            "body_temperature": round(random.uniform(30.0, 40.0), 1),  # Random body temperature between 36.0 and 37.5 degrees Celsius
            "respiratory_rate": random.randint(8, 30),  # Random respiratory rate between 12 and 20 breaths per minute
            "oxygen_saturation": random.randint(85, 110),  # Random oxygen saturation level between 95% and 100%
            "physical_activity": {
                "steps": random.randint(1000, 10000),  # Random steps between 1000 and 10000
                "distance": round(random.uniform(1.0, 10.0), 2),  # Random distance between 1.0 and 10.0 km
                "active_minutes": random.randint(30, 120)  # Random active minutes between 30 and 120
            },
            "sleep_patterns": {
                "duration": random.randint(240, 540),  # Random sleep duration between 4 and 9 hours
                "quality": random.randint(1, 5),  # Random sleep quality rating between 1 and 5
                "sleep_stages": ["deep", "light", "REM"]  # Random sleep stages
            },
            "blood_oxygen_level": random.randint(85, 110),  # Random blood oxygen level between 95% and 100%
            "weight": round(random.uniform(50.0, 100.0), 2),  # Random weight between 50.0 and 100.0 kg
            "environmental_factors": {
                "temperature": round(random.uniform(15.0, 30.0), 1),  # Random temperature between 15.0 and 30.0 degrees Celsius
                "humidity": random.randint(30, 70)  # Random humidity between 30% and 70%
            },
            "medication_adherence": random.choice(["adherent", "non-adherent"]),  # Random medication adherence status
            "water_intake": random.randint(1000, 3000),  # Random water intake between 1000 and 3000 ml
            "environmental_pollutants": {
                "air_quality": random.choice(["good", "moderate", "poor"]),  # Random air quality
                "particulate_matter": random.randint(10, 100)  # Random particulate matter level between 10 and 100
            },
            "blood_alcohol_level": round(random.uniform(0.0, 0.1), 3),  # Random blood alcohol level between 0.0% and 0.1%
            "uv_exposure": {
                "index": random.randint(0, 10),  # Random UV index between 0 and 10
                "duration": random.randint(30, 120)  # Random UV exposure duration between 30 and 120 minutes
            },
            "glucose_trends": ["stable", "increasing", "decreasing"],  # Random glucose trends
            "fall_detection": random.choice(["yes", "no"]),  # Random fall detection status
            "gait_analysis": random.choice(["normal", "abnormal"]),  # Random gait analysis result
            "posture_monitoring": random.choice(["good", "poor"]),  # Random posture monitoring result
            "electroencephalogram": "alpha waves",  # Random EEG data
            "skin_conductance": random.randint(10, 50),  # Random skin conductance level between 10 and 50
            "blood_flow": random.randint(40, 110),  # Random blood flow level between 50 and 100
            "blood_coagulation_status": {
                "prothrombin_time": round(random.uniform(10.0, 15.0), 1),  # Random prothrombin time between 10.0 and 15.0 seconds
                "partial_thromboplastin_time": round(random.uniform(25.0, 40.0), 1)  # Random partial thromboplastin time between 25.0 and 40.0 seconds
            }
        }
        return data
    else:
        return ('User not found')

# Insert random health data every minute
while True:
    s=""
    health_data = generate_random_data()
    if(health_data["heart_rate"]>100 or health_data["heart_rate"]<60):
        s+="Your Heart rate is abnomral \n Heart rate :"+str(health_data["heart_rate"])+"\n"
    # Checking Blood Pressure
    if health_data["blood_pressure"]["systolic"] < 90 or health_data["blood_pressure"]["systolic"] > 120 \
            or health_data["blood_pressure"]["diastolic"] < 60 or health_data["blood_pressure"]["diastolic"] > 80:
        s += "Your blood pressure is abnormal \nSystolic: " + str(health_data["blood_pressure"]["systolic"]) + " mmHg\n"
        s += "Diastolic: " + str(health_data["blood_pressure"]["diastolic"]) + " mmHg\n"

    # Checking Blood Glucose Level
    if health_data["blood_glucose"] < 70 or health_data["blood_glucose"] > 99:
        s += "Your blood glucose level is abnormal \nBlood Glucose Level: " + str(health_data["blood_glucose"]) + " mg/dL (fasting)\n"

    # Checking Body Temperature
    if health_data["body_temperature"] < 36.0 or health_data["body_temperature"] > 39.5:
        s += "Your body temperature is abnormal \nBody Temperature: " + str(health_data["body_temperature"]) + "°F\n"

    # Checking Heart Rate
    if health_data["heart_rate"] < 60 or health_data["heart_rate"] > 100:
        s += "Your heart rate is abnormal \nHeart Rate: " + str(health_data["heart_rate"]) + " bpm\n"

    # Checking Respiratory Rate
    if health_data["respiratory_rate"] < 12 or health_data["respiratory_rate"] > 20:
        s += "Your respiratory rate is abnormal \nRespiratory Rate: " + str(health_data["respiratory_rate"]) + " breaths per minute\n"

    # Checking Oxygen Saturation
    if health_data["oxygen_saturation"] < 95 or health_data["oxygen_saturation"] > 100:
        s += "Your oxygen saturation level is abnormal \nOxygen Saturation: " + str(health_data["oxygen_saturation"]) + "%\n"

    # Checking Blood Oxygen Level (SpO2)
    if health_data["blood_oxygen_level"] < 95 or health_data["blood_oxygen_level"] > 100:
        s += "Your blood oxygen level (SpO2) is abnormal \nBlood Oxygen Level (SpO2): " + str(health_data["blood_oxygen_level"]) + "%\n"

    # Checking Blood Flow (assuming no specific data provided)
    # Include code here if you have specific data to check for blood flow abnormalities

    # Check if any abnormalities were found
    if s:
        s += "Please take medical attention ASAP!!\n"
        sendSMS(s)

    print(s)
    healthcollection.insert_one(health_data)
    print("Inserted:", health_data)
    time.sleep(1)  # Wait for 1 minute before inserting the next data
