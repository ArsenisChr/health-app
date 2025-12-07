# 🩺 HealthLab Coach

A smart, AI-powered health companion that analyzes your lifestyle, lab results, and personal preferences to classify your health profile and recommend personalized wellness events.

## 🚀 Features

*   **AI Lifestyle Clustering**: Classifies users into dynamic clusters (e.g., "Couch Potato", "Ironman") using Machine Learning (XGBoost) based on their profile and lab data.
*   **Smart PDF Analysis**: Extracts key biomarkers (Cholesterol, HDL, LDL, etc.) from uploaded PDF lab reports using OCR and regex processing.
*   **Personalized Recommendations**: Suggests local wellness events (Yoga, Hiking, etc.) tailored to the user's cluster and location via Langflow AI workflows.
*   **Accessibility First**: Includes a built-in accessibility widget for high contrast, font resizing, and link highlighting.
*   **Cloud Ready**: Designed for deployment on Azure Web Apps with persistent storage support.

## 🛠️ Tech Stack

*   **Backend**: Python, Flask
*   **Database**: SQLite (with cloud persistence logic)
*   **AI & Machine Learning**:
    *   **Langflow**: Orchestration for PDF extraction and Event recommendation workflows.
    *   **XGBoost**: User classification model.
    *   **Scikit-Learn**: Data preprocessing and encoding.
*   **Data Processing**: Pandas, pdfplumber
*   **Frontend**: HTML5, CSS3, Bootstrap 5, JavaScript

## 📂 Project Structure

```
health-app/
├── app.py                      # Main Flask application (Routes & DB logic)
├── backend.py                  # API integration with Langflow & PDF processing
├── ml_service.py               # Machine Learning inference service (loads XGBoost model)
├── cluster_classify_algorithm.py # ML Training script (Generates model artifacts)
├── requirements.txt            # Python dependencies
├── users.db                    # SQLite database (local dev)
├── templates/                  # HTML Templates (Jinja2)
│   ├── home.html               # Dashboard with Cluster display
│   ├── profile.html            # User profile & PDF upload
│   ├── events.html             # Event calendar & recommendations
│   └── ...
├── static/
│   ├── css/                    # Custom styles
│   └── js/                     # Frontend scripts (Accessibility widget)
└── ...
```

## 🧠 How It Works

1.  **User Onboarding**: Users register and complete a basic profile (Age, City, Interests).
2.  **Data Ingestion**: Users can upload PDF lab results. The app parses these files (`backend.py`) to extract biomarker data.
3.  **Classification**: The `ml_service.py` loads a pre-trained XGBoost model to classify the user into a lifestyle cluster (e.g., "Weekend Warrior") based on their data.
4.  **Event Recommendation**: The app communicates with a Langflow agent to fetch personalized event recommendations based on the user's location and interests.
5.  **Dashboard**: The user sees their "Cluster Level", progress, and a calendar of recommended events.

## 📦 Installation & Setup

1.  Clone the repository.
2.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
3.  Train the ML model (once) to generate artifacts:
    ```bash
    python cluster_classify_algorithm.py
    ```
4.  Run the Flask app:
    ```bash
    python app.py
    ```
5.  Visit `http://localhost:5000` in your browser.
