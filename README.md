🩺 Disease Prediction and Dietary Recommendation System

An AI-powered healthcare support web application that predicts likely diseases from user-reported symptoms and generates a personalized 7-day dietary recovery plan — built with Flask, Scikit-learn, and SQLite.


📌 Overview

Many people experience common symptoms (fever, fatigue, nausea, etc.) but lack quick, reliable guidance on possible causes or next steps. This project bridges that gap by combining Machine Learning-based symptom analysis with structured nutritional recovery guidance, giving users an instant preliminary diagnosis and an actionable diet plan — all in one platform.

The system takes 8 binary symptom inputs, runs them through a trained classification model, predicts one of 15 supported medical conditions, and returns:


🔎 The predicted disease
💊 A suggested clinical solution
🥗 A tailored 7-day diet plan
🕘 A saved entry in the user's prediction history



⚠️ Disclaimer: This is a preliminary screening tool for educational purposes only. It does not replace professional medical diagnosis, lab tests, or physical examination by a doctor.




✨ Features


Secure Authentication – User registration and login with session-based access control
Symptom-Based Prediction – Simple checklist UI for 8 key clinical symptoms (fever, cough, headache, fatigue, sore throat, body pain, shortness of breath, nausea)
ML-Powered Diagnosis – Random Forest / Decision Tree classifier (disease_model.pkl) predicts across 15 medical conditions
Personalized Diet Plans – Auto-generated 7-day nutritional plan mapped to the predicted disease (105 total diet entries)
Prediction History – Persistent, per-user log of past diagnoses and diet recommendations
Responsive UI – Mobile-friendly interface built with HTML5, CSS3, and Bootstrap 5
Robust Error Handling – Graceful handling of invalid logins, duplicate registrations, and empty history states



🛠️ Tech Stack

LayerTechnologyBackendPython 3.13, Flask 3.0.xMachine LearningScikit-learn, NumPy, Pandas, JoblibDatabaseSQLite3FrontendHTML5, CSS3, Bootstrap 5, Jinja2 templatingIDEVisual Studio Code


🏗️ System Architecture

The application follows a modified Model–View–Controller (MVC) pattern:


Model – SQLite database (database.db) + ML models (.pkl files)
View – Jinja2-rendered HTML templates styled with CSS
Controller – Flask application (app.py) handling routing, ML inference calls, and database operations


Core Modules


User Authentication & Security Module – Registration, login, and session management
Symptom Processing & Feature Engineering Module – Converts selected symptoms into a numerical feature vector
Machine Learning Inference Module – Loads disease_model.pkl and predicts the most likely disease
Result Generation & Dietary Mapping Module – Maps predictions to solutions and 7-day diet plans, and renders the result dashboard



📂 Project Structure

├── app.py                  # Core Flask controller (routes, session handling)
├── disease_model.pkl       # Trained ML classification model
├── disease_solution.pkl    # Clinical knowledge base / solutions
├── database.db             # SQLite database (users & patients tables)
├── requirements.txt        # Python dependencies
├── templates/
│   ├── login.html          # User login page
│   ├── register.html       # New user registration
│   ├── index.html          # Symptom selection dashboard
│   ├── result.html         # Prediction + diet plan result page
│   └── history.html        # Past prediction history
└── static/                 # CSS / static assets


⚙️ Installation

Prerequisites


Python 3.13 (or compatible 3.x version)
pip


Setup

bash# Clone the repository
git clone https://github.com/<your-username>/disease-prediction-dietary-system.git
cd disease-prediction-dietary-system

# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate      # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the application
python app.py

The app will initialize the SQLite database automatically on first run and start a local Flask development server (default: http://127.0.0.1:5000).

Dependencies (requirements.txt)

Flask
scikit-learn
pandas
numpy
Joblib


🚀 Usage


Register / Log in to create a secure session.
On the dashboard, select the symptoms you're experiencing (Fever, Cough, Headache, Fatigue, Sore Throat, Body Pain, Shortness of Breath, Nausea).
Click Predict — your inputs are converted into a feature vector and passed to the ML model.
View your result: predicted disease, suggested solution, and a full 7-day diet plan.
Visit History anytime to review past predictions and recommendations.
Log out to securely close your session.



🧪 Testing


Unit Testing – Password hashing, symptom-to-vector conversion
Integration Testing – Flask ↔ SQLite ↔ ML model communication
User Acceptance Testing – Cross-device UI verification
Model Validation – ~92% accuracy on the test dataset, confusion matrix analysis to reduce cross-disease misclassification
Boundary Testing – Invalid logins, duplicate registrations, empty history states handled gracefully



🔭 Future Work


Multimodal Input – Image (e.g., skin rash) and voice-based symptom analysis
Wearable Integration – Real-time vitals via Google Fit / Apple Health APIs
Dynamic Diet Generation – LLM-powered personalized recipes based on allergies, BMI, and local food availability
Cloud Deployment – Migration from SQLite to PostgreSQL / AWS RDS for concurrent multi-user scale
Adherence Tracking – Checklist to track meal completion against the 7-day plan



⚠️ Limitations


Not a substitute for professional medical diagnosis or lab testing
No integration with real-time health sensors/wearables
Does not prescribe medications or dosages
English language only
No emergency alert or hospital integration



Department of Computer Science, Lahore Leads University, Lahore, Pakistan


📄 License

This project was developed as a Final Year Project (FYP) for academic purposes. Add your preferred license (e.g., MIT) here.
