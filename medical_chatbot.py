import os
import json
import datetime
import pyttsx3
from colorama import init, Fore, Style
from config import SYMPTOMS, QUESTIONS, SEVERITY_LEVELS
from ml_models import MedicalMLModels

init()  # Initialize colorama for colored output

class MedicalChatbot:
    def __init__(self, use_voice=False):
        self.use_voice = use_voice
        self.responses = {}
        self.conversation_history = []
        self.ml_models = None
        
        if use_voice:
            # Initialize text-to-speech engine
            self.engine = pyttsx3.init()
            
        # Initialize ML models
        self.initialize_models()

    def initialize_models(self):
        """Initialize and train the ML models."""
        try:
            # Load the dataset from data directory
            dataset_path = os.path.join('data', 'Disease_symptom_and_patient_profile_dataset.csv')
            if os.path.exists(dataset_path):
                self.ml_models = MedicalMLModels()
                self.ml_models.train_models(dataset_path)
            else:
                print(f"{Fore.YELLOW}Warning: Dataset not found. ML predictions will be disabled.{Style.RESET_ALL}")
                self.ml_models = None
        except Exception as e:
            print(f"{Fore.RED}Error initializing ML models: {e}. ML predictions will be disabled.{Style.RESET_ALL}")
            self.ml_models = None

    def predict_disease(self):
        """Generate disease predictions based on reported symptoms and patient info."""
        if not self.ml_models:
            return None
            
        try:
            # Create feature vector
            features = {
                'Fever': 1 if self.responses.get('fever', False) else 0,
                'Cough': 1 if self.responses.get('cough', False) else 0,
                'Fatigue': 1 if self.responses.get('fatigue', False) else 0,
                'Difficulty Breathing': 1 if self.responses.get('difficulty_breathing', False) else 0,
                'Age': self.responses.get('age', 30),
                'Gender': 1 if self.responses.get('gender', '').lower() == 'male' else 0,
                'Blood Pressure': {
                    'low': 0,
                    'normal': 1,
                    'high': 2
                }.get(self.responses.get('blood_pressure', 'normal').lower(), 1),
                'Cholesterol Level': {
                    'low': 0,
                    'normal': 1,
                    'high': 2
                }.get(self.responses.get('cholesterol', 'normal').lower(), 1)
            }
            
            return self.ml_models.predict(features)
        except Exception as e:
            print(f"{Fore.RED}Error making prediction: {e}{Style.RESET_ALL}")
            return None

    def speak(self, text):
        """Speak the given text if voice is enabled."""
        if self.use_voice:
            self.engine.say(text)
            self.engine.runAndWait()

    def display_and_speak(self, text, color=Fore.BLUE):
        """Display text and speak it if voice is enabled."""
        print(f"{color}{text}{Style.RESET_ALL}")
        self.speak(text)

    def get_validated_input(self, question_type, prompt):
        """Get and validate user input based on the question type."""
        while True:
            user_input = input(f"{Fore.CYAN}> {Style.RESET_ALL}").strip().lower()
            
            if question_type == 'number':
                try:
                    age = int(user_input)
                    if 0 <= age <= 120:
                        return age
                    else:
                        self.display_and_speak("Please enter a valid age between 0 and 120.", Fore.RED)
                except ValueError:
                    self.display_and_speak("Please enter a valid number.", Fore.RED)
            
            elif question_type == 'boolean':
                if user_input in ['yes', 'no', 'y', 'n']:
                    return user_input in ['yes', 'y']
                else:
                    self.display_and_speak("Please answer with yes/no or y/n.", Fore.RED)
            
            else:  # text input
                if question_type == 'gender' and user_input not in ['male', 'female', 'm', 'f']:
                    self.display_and_speak("Please enter 'male' or 'female' (or 'm'/'f').", Fore.RED)
                    continue
                elif question_type == 'level' and user_input not in ['low', 'normal', 'high', 'l', 'n', 'h']:
                    self.display_and_speak("Please enter 'low', 'normal', or 'high' (or 'l'/'n'/'h').", Fore.RED)
                    continue
                return user_input

    def ask_initial_questions(self):
        """Ask the initial set of questions."""
        # Add questions for ML model features
        initial_questions = [
            {'id': 'age', 'text': 'What is your age?', 'type': 'number'},
            {'id': 'gender', 'text': 'What is your gender? (male/female)', 'type': 'gender'},
            {'id': 'blood_pressure', 'text': 'What is your blood pressure level? (low/normal/high)', 'type': 'level'},
            {'id': 'cholesterol', 'text': 'What is your cholesterol level? (low/normal/high)', 'type': 'level'},
        ]
        
        for question in initial_questions:
            self.display_and_speak(question['text'])
            response = self.get_validated_input(question['type'], question['text'])
            self.responses[question['id']] = response
            self.conversation_history.append({
                'question': question['text'],
                'response': response
            })

    def ask_symptom_questions(self):
        """Ask about symptoms and follow-up questions based on responses."""
        for question in QUESTIONS['symptoms']:
            self.display_and_speak(question['text'])
            has_symptom = self.get_validated_input('boolean', question['text'])
            self.responses[question['id']] = has_symptom
            self.conversation_history.append({
                'question': question['text'],
                'response': has_symptom
            })

            if has_symptom and question['id'] in SYMPTOMS:
                # Ask follow-up questions for this symptom
                for follow_up in SYMPTOMS[question['id']]['follow_up_questions']:
                    if follow_up in QUESTIONS['follow_up']:
                        self.display_and_speak(QUESTIONS['follow_up'][follow_up])
                        response = self.get_validated_input('boolean', QUESTIONS['follow_up'][follow_up])
                        self.responses[follow_up] = response
                        self.conversation_history.append({
                            'question': QUESTIONS['follow_up'][follow_up],
                            'response': response
                        })

    def analyze_symptoms(self):
        """Analyze the collected symptoms and provide a recommendation."""
        severity = 'low'
        reported_symptoms = []

        for symptom_id, has_symptom in self.responses.items():
            if symptom_id in SYMPTOMS and has_symptom:
                reported_symptoms.append(SYMPTOMS[symptom_id]['name'])
                symptom_severity = SYMPTOMS[symptom_id]['severity']
                if symptom_severity == 'high':
                    severity = 'high'
                elif symptom_severity == 'medium' and severity != 'high':
                    severity = 'medium'

        # Get ML prediction
        prediction = self.predict_disease() if reported_symptoms else None
        if prediction:
            self.responses['predicted_condition'] = prediction

        return severity, reported_symptoms

    def save_conversation(self):
        """Save the conversation history to a JSON file."""
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Create chats directory if it doesn't exist
        os.makedirs('chats', exist_ok=True)
        filename = os.path.join('chats', f'medical_chat_{timestamp}.json')
        
        with open(filename, 'w') as f:
            json.dump({
                'timestamp': timestamp,
                'conversation': self.conversation_history,
                'final_assessment': {
                    'severity': self.responses.get('severity', 'unknown'),
                    'reported_symptoms': self.responses.get('reported_symptoms', []),
                    'predicted_condition': self.responses.get('predicted_condition', None)
                }
            }, f, indent=2)
        
        print(f"{Fore.GREEN}Conversation saved to {filename}{Style.RESET_ALL}")

    def run(self):
        """Run the medical chatbot interaction."""
        self.display_and_speak("Hello! I'm your virtual health assistant. I'll ask you some questions to assess your health condition.", Fore.GREEN)
        self.display_and_speak("Please note: This is not a substitute for professional medical advice. If you're experiencing severe symptoms, please seek immediate medical attention.", Fore.YELLOW)
        
        # Ask questions
        self.ask_initial_questions()
        self.ask_symptom_questions()
        
        # Analyze and provide recommendation
        severity, reported_symptoms = self.analyze_symptoms()
        self.responses['severity'] = severity
        self.responses['reported_symptoms'] = reported_symptoms
        
        # Display summary
        self.display_and_speak("\nBased on your responses:", Fore.GREEN)
        if reported_symptoms:
            self.display_and_speak(f"You reported the following symptoms: {', '.join(reported_symptoms)}", Fore.YELLOW)
            
            # Display possible condition if available
            if 'predicted_condition' in self.responses and self.responses['predicted_condition']:
                self.display_and_speak(
                    f"\nBased on your symptoms and profile, you may have: {self.responses['predicted_condition']}",
                    Fore.CYAN
                )
                self.display_and_speak(
                    "Note: This is a preliminary assessment and should be verified by a healthcare professional.",
                    Fore.RED
                )
        else:
            self.display_and_speak("You haven't reported any major symptoms.", Fore.GREEN)
        
        # Display recommendation based on severity
        self.display_and_speak(f"\nRecommendation: {SEVERITY_LEVELS[severity]}", Fore.YELLOW)
        
        # Save conversation
        self.save_conversation()
        
        self.display_and_speak("\nThank you for using the medical chatbot. Take care!", Fore.GREEN)

if __name__ == "__main__":
    # Create and run the chatbot
    use_voice = input("Would you like to enable voice output? (yes/no): ").lower() in ['yes', 'y']
    chatbot = MedicalChatbot(use_voice=use_voice)
    chatbot.run() 