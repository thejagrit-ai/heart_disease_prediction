"""
Heart Disease Prediction System - Flask Backend
Project: Heart Disease Prediction using Machine Learning
Developers: Jagrit Sharma, Abhishek Godara, Deepanshu
Supervisor: Dr. Megha Chhabra
Faculty of Engineering & Technology - Department of Computer Applications

This is a complete, production-ready backend API for heart disease prediction.
The project demonstrates advanced machine learning techniques with high accuracy.
"""

from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from flask_httpauth import HTTPBasicAuth
import pickle
import numpy as np
import os
from datetime import datetime
import json

app = Flask(__name__, template_folder='../frontend', static_folder='../frontend/static')
CORS(app)
auth = HTTPBasicAuth()

# Admin credentials
ADMIN_CREDENTIALS = {
    'sjagrit2005@gmail.com': 'Jagrit@14'
}

# Load the trained model and scaler
model_path = os.path.join(os.path.dirname(__file__), '../models/heart_disease_model.pkl')
scaler_path = os.path.join(os.path.dirname(__file__), '../models/scaler.pkl')

with open(model_path, 'rb') as f:
    model = pickle.load(f)

with open(scaler_path, 'rb') as f:
    scaler = pickle.load(f)

# Feature names
FEATURE_NAMES = ['age', 'sex', 'cp', 'trestbps', 'chol', 'fbs', 'restecg', 'thalach', 'exang', 'oldpeak', 'slope', 'ca', 'thal']

# Admin verification
@auth.verify_password
def verify_password(username, password):
    if username in ADMIN_CREDENTIALS:
        if ADMIN_CREDENTIALS[username] == password:
            return username
    return None

# Routes

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/admin-login', methods=['POST'])
@auth.login_required
def admin_login():
    return jsonify({'message': 'Admin login successful', 'admin': auth.current_user()}), 200

@app.route('/api/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()

        # Validate input
        if not all(key in data for key in FEATURE_NAMES):
            return jsonify({'error': 'Missing required fields'}), 400

        # Extract and convert features
        features = np.array([[float(data[feature]) for feature in FEATURE_NAMES]])

        # Scale features
        features_scaled = scaler.transform(features)

        # Make prediction
        prediction = model.predict(features_scaled)[0]
        probability = model.predict_proba(features_scaled)[0]

        # Risk level classification
        risk_score = probability[1]
        if risk_score < 0.33:
            risk_level = "LOW RISK"
            color = "green"
        elif risk_score < 0.66:
            risk_level = "MODERATE RISK"
            color = "orange"
        else:
            risk_level = "HIGH RISK"
            color = "red"

        result = {
            'prediction': int(prediction),
            'risk_probability': float(probability[1]),
            'disease_probability': float(probability[1]) * 100,
            'no_disease_probability': float(probability[0]) * 100,
            'risk_level': risk_level,
            'color': color,
            'recommendation': get_recommendation(data, risk_score)
        }

        return jsonify(result), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

def get_recommendation(data, risk_score):
    """Generate personalized recommendations based on patient data"""
    recommendations = []

    if int(data.get('age', 0)) > 60:
        recommendations.append("Your age is a significant risk factor. Regular medical checkups are essential.")

    if int(data.get('chol', 0)) > 240:
        recommendations.append("Your cholesterol level is high. Consider dietary changes and consult your doctor.")

    if int(data.get('trestbps', 0)) > 140:
        recommendations.append("Your blood pressure is elevated. Monitor regularly and reduce sodium intake.")

    if int(data.get('thalach', 0)) < 100:
        recommendations.append("Your maximum heart rate is low. Increase physical activity gradually.")

    if int(data.get('exang', 0)) == 1:
        recommendations.append("You experience exercise-induced angina. Consult a cardiologist before strenuous activity.")

    if risk_score > 0.7:
        recommendations.append("⚠️ URGENT: Seek immediate medical consultation from a cardiologist.")
    elif risk_score > 0.5:
        recommendations.append("Schedule a detailed cardiac evaluation with your physician.")
    else:
        recommendations.append("Maintain healthy lifestyle habits and annual checkups.")

    return recommendations

@app.route('/api/info/about', methods=['GET'])
def about():
    about_data = {
        'title': 'Heart Disease Prediction System',
        'description': 'Advanced Machine Learning based heart disease prediction system',
        'accuracy': '81%',
        'dataset_size': '500+ patient records',
        'algorithm': 'Random Forest Classifier',
        'features_used': 13
    }
    return jsonify(about_data), 200

@app.route('/api/info/disease-info', methods=['GET'])
def disease_info():
    disease_data = {
        'what_is_heart_disease': {
            'title': 'What is Heart Disease?',
            'content': 'Heart disease refers to a range of conditions affecting the heart and blood vessels. Coronary artery disease (CAD) is the most common type, caused by atherosclerosis - the buildup of cholesterol plaque in arteries that restricts blood flow to the heart.',
            'types': [
                'Coronary Artery Disease (CAD)',
                'Heart Attack (Myocardial Infarction)',
                'Arrhythmias (Irregular Heartbeat)',
                'Heart Failure',
                'Valve Disorders'
            ]
        },
        'how_it_develops': {
            'title': 'How Does Heart Disease Develop?',
            'stages': [
                'Stage 1: Plaque begins to form in artery walls due to high cholesterol and other risk factors',
                'Stage 2: Plaque builds up over time, narrowing the arteries and reducing blood flow',
                'Stage 3: Blood clots may form when plaque ruptures, completely blocking blood flow',
                'Stage 4: Heart attack occurs when blood flow to heart muscle is severely restricted',
                'Stage 5: Repeated damage can lead to heart failure and permanent damage'
            ]
        },
        'risk_factors': {
            'title': 'Major Risk Factors',
            'factors': [
                'High Blood Pressure (>140/90 mmHg)',
                'High Cholesterol (>240 mg/dL)',
                'Smoking and Tobacco Use',
                'Diabetes',
                'Obesity (BMI > 30)',
                'Physical Inactivity',
                'Poor Diet (High in saturated fats)',
                'Age (Men >45, Women >55)',
                'Family History',
                'Stress and Sleep Disorders'
            ]
        },
        'prevention_tips': {
            'title': 'Prevention and Management',
            'tips': [
                '🥗 Eat Heart-Healthy Diet: Mediterranean or DASH diet (whole grains, fruits, vegetables)',
                '🏃 Exercise Regularly: 150 minutes of moderate activity per week',
                '🚭 Quit Smoking: Eliminates major risk factor immediately',
                '⚖️ Maintain Healthy Weight: Target BMI 18.5-24.9',
                '🧘 Reduce Stress: Practice meditation, yoga, or relaxation techniques',
                '😴 Get Adequate Sleep: 7-9 hours per night',
                '🍷 Limit Alcohol: Moderation is key',
                '📊 Monitor Blood Pressure & Cholesterol: Regular checkups',
                '💊 Take Medications: As prescribed by doctor',
                '❤️ Manage Existing Conditions: Diabetes, hypertension control'
            ]
        },
        'warning_signs': {
            'title': 'Warning Signs - Seek Immediate Care',
            'signs': [
                'Chest pain or pressure, especially during activity',
                'Shortness of breath at rest or during activity',
                'Sudden severe dizziness or fainting',
                'Unusual fatigue or weakness',
                'Heart palpitations or irregular heartbeat',
                'Persistent nausea or sweating',
                'Swelling in legs, ankles, or feet',
                'Difficulty exercising or reduced exercise tolerance'
            ]
        }
    }
    return jsonify(disease_data), 200

@app.route('/api/info/developers', methods=['GET'])
def developers():
    developers_data = {
        'project_name': 'Heart Disease Prediction System',
        'version': '1.0.0',
        'faculty': 'Faculty of Engineering & Technology',
        'department': 'Department of Computer Applications',
        'supervisor': 'Dr. Megha Chhabra',
        'team': [
            {
                'name': 'Jagrit Sharma',
                'roll_no': '231348043',
                'role': 'Data Preprocessing, Visualization & Feature Engineering',
                'contribution': 'Lead data scientist - handled dataset preparation and exploratory analysis'
            },
            {
                'name': 'Abhishek Godara',
                'roll_no': '231348045',
                'role': 'Model Building & Evaluation',
                'contribution': 'Machine learning engineer - trained and optimized multiple algorithms'
            },
            {
                'name': 'Deepanshu',
                'roll_no': '231348046',
                'role': 'Documentation, Presentation & Dynamic Input Script',
                'contribution': 'Full-stack developer - created frontend interface and deployment'
            }
        ],
        'technologies': [
            'Python 3.x',
            'Flask (Backend)',
            'React/HTML5/CSS3/JavaScript (Frontend)',
            'Scikit-learn (Machine Learning)',
            'Pandas & NumPy (Data Processing)',
            'SQLite (Database)'
        ],
        'project_duration': '2-3 months',
        'sdg_goal': 'SDG Goal 3 - Good Health and Well-Being',
        'acknowledgements': 'We acknowledge the use of UCI Heart Disease dataset and open-source libraries. This project is created for educational purposes.'
    }
    return jsonify(developers_data), 200

@app.route('/api/features', methods=['GET'])
def features():
    features_data = {
        'features': [
            {'name': 'Age', 'description': 'Patient age in years', 'range': '29-77'},
            {'name': 'Sex', 'description': '0: Female, 1: Male', 'range': '[0, 1]'},
            {'name': 'Chest Pain Type', 'description': '0: Typical Angina, 1: Atypical Angina, 2: Non-Angina, 3: Asymptomatic', 'range': '[0, 1, 2, 3]'},
            {'name': 'Resting Blood Pressure', 'description': 'in mm Hg', 'range': '90-210'},
            {'name': 'Serum Cholesterol', 'description': 'in mg/dL', 'range': '120-580'},
            {'name': 'Fasting Blood Sugar', 'description': '0: ≤120 mg/dL, 1: >120 mg/dL', 'range': '[0, 1]'},
            {'name': 'Resting ECG', 'description': '0: Normal, 1: ST-T abnormality, 2: LV hypertrophy', 'range': '[0, 1, 2]'},
            {'name': 'Max Heart Rate', 'description': 'Maximum heart rate achieved', 'range': '60-210'},
            {'name': 'Exercise Induced Angina', 'description': '0: No, 1: Yes', 'range': '[0, 1]'},
            {'name': 'ST Depression', 'description': 'ST depression induced by exercise', 'range': '0-6.2'},
            {'name': 'Slope of ST', 'description': '1: Upsloping, 2: Flat, 3: Downsloping', 'range': '[1, 2, 3]'},
            {'name': 'Major Vessels', 'description': 'Number of major blood vessels colored by fluoroscopy', 'range': '[0, 1, 2, 3]'},
            {'name': 'Thalassemia', 'description': '0: Normal, 1: Fixed defect, 2: Reversible defect', 'range': '[0, 1, 2]'}
        ]
    }
    return jsonify(features_data), 200

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)
