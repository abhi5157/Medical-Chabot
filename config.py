SYMPTOMS = {
    'fever': {
        'name': 'Fever',
        'follow_up_questions': ['chills', 'body_aches', 'fatigue'],
        'severity': 'medium'
    },
    'cough': {
        'name': 'Cough',
        'follow_up_questions': ['chest_pain', 'shortness_of_breath', 'sputum'],
        'severity': 'medium'
    },
    'headache': {
        'name': 'Headache',
        'follow_up_questions': ['vision_changes', 'nausea', 'sensitivity_to_light'],
        'severity': 'medium'
    },
    'chest_pain': {
        'name': 'Chest Pain',
        'follow_up_questions': ['shortness_of_breath', 'sweating', 'radiating_pain'],
        'severity': 'high'
    }
}

QUESTIONS = {
    'initial': [
        {
            'id': 'age',
            'text': 'What is your age?',
            'type': 'number',
            'validation': lambda x: 0 <= int(x) <= 120
        },
        {
            'id': 'chronic_conditions',
            'text': 'Do you have any chronic conditions? (yes/no)',
            'type': 'boolean'
        }
    ],
    'symptoms': [
        {
            'id': 'fever',
            'text': 'Do you have a fever? (yes/no)',
            'type': 'boolean'
        },
        {
            'id': 'cough',
            'text': 'Are you experiencing cough? (yes/no)',
            'type': 'boolean'
        },
        {
            'id': 'headache',
            'text': 'Do you have a headache? (yes/no)',
            'type': 'boolean'
        }
    ],
    'follow_up': {
        'chills': 'Are you experiencing chills? (yes/no)',
        'body_aches': 'Do you have body aches? (yes/no)',
        'fatigue': 'Are you feeling unusually tired? (yes/no)',
        'chest_pain': 'Are you experiencing chest pain? (yes/no)',
        'shortness_of_breath': 'Do you have difficulty breathing? (yes/no)',
        'sputum': 'Are you coughing up any mucus? (yes/no)',
        'vision_changes': 'Have you noticed any changes in your vision? (yes/no)',
        'nausea': 'Do you feel nauseous? (yes/no)',
        'sensitivity_to_light': 'Are you sensitive to light? (yes/no)',
        'sweating': 'Are you experiencing unusual sweating? (yes/no)',
        'radiating_pain': 'Does the pain radiate to other areas? (yes/no)'
    }
}

SEVERITY_LEVELS = {
    'low': 'Your symptoms appear to be mild. Monitor your condition and rest.',
    'medium': 'Your symptoms suggest you should consult with a healthcare provider soon.',
    'high': 'Your symptoms require immediate medical attention. Please seek emergency care.'
} 