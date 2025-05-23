# Medical Chatbot

A conversational medical chatbot that helps assess health conditions through interactive questioning and provides health recommendations based on machine learning predictions.

## Features

### 1. Interactive Health Assessment

- Collects patient information (age, gender, blood pressure, cholesterol)
- Gathers information about symptoms through dynamic questioning
- Provides severity-based recommendations
- Text-to-speech capability for better accessibility (optional)

### 2. Machine Learning Integration

- Uses multiple ML models (Decision Tree, Random Forest, SVM)
- Automatically selects the best performing model for predictions
- Provides preliminary condition assessments based on:
  - Reported symptoms
  - Patient profile (age, gender)
  - Health metrics (blood pressure, cholesterol)

### 3. Conversation Management

- Saves all conversations with timestamps
- Stores chat history in JSON format
- Maintains organized conversation records in the 'chats' directory

## Project Structure

```
medical-chatbot/
├── chats/                  # Conversation history storage
├── data/                   # Dataset storage
│   └── Disease_symptom_and_patient_profile_dataset.csv
├── medical_chatbot.py      # Main chatbot implementation
├── ml_models.py           # Machine learning models implementation
├── config.py              # Configuration and question sets
├── requirements.txt       # Project dependencies
└── README.md             # Documentation
```

## Setup and Installation

1. **Create and activate a virtual environment**:

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Unix/MacOS:
source venv/bin/activate
```

2. **Install dependencies**:

```bash
pip install -r requirements.txt
```

3. **Prepare the dataset**:

- Place your disease-symptom dataset in the `data` directory
- Ensure it's named `Disease_symptom_and_patient_profile_dataset.csv`
- Required columns:
  - Symptoms (Fever, Cough, Fatigue, Difficulty Breathing)
  - Patient Info (Age, Gender)
  - Health Metrics (Blood Pressure, Cholesterol Level)
  - Disease (target variable)

## Usage

1. **Run the chatbot**:

```bash
python medical_chatbot.py
```

2. **Initial setup**:

- Choose whether to enable voice output
- The system will automatically initialize and train ML models

3. **During the conversation**:

- Answer questions about your health profile
- Provide information about your symptoms
- Receive a health assessment including:
  - List of reported symptoms
  - Possible condition based on ML analysis
  - Severity-based recommendations

4. **After the conversation**:

- Chat history is automatically saved in the `chats` directory
- Each chat file includes:
  - Timestamp
  - Full conversation history
  - Final assessment
  - Predicted condition
