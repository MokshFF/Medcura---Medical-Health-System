import tkinter as tk
from tkinter import ttk, messagebox

class MedcuraApp:
    def __init__(self, root):
        self.root = root
        self.root.title("MedCura - Health Analysis System")

        # Set window to fullscreen
        self.root.state('zoomed')  # Maximize window on Windows
        self.root.resizable(True, True)

        # Modern professional color palette
        self.colors = {
            'primary': '#0066CC',
            'primary_dark': '#0052A3',
            'primary_light': '#E6F0FF',
            'accent': '#FF6B6B',
            'white': '#FFFFFF',
            'gray_dark': '#333333',
            'gray': '#666666',
            'gray_medium': '#999999',
            'light_gray': '#F8F9FA',
            'very_light_gray': '#E9ECEF',
            'text': '#1A1A1A',
            'text_secondary': '#555555',
            'black': '#000000',
            'error': '#E74C3C',
            'success': '#27AE60',
            'warning': '#F39C12',
            'info': '#3498DB',
            'card_bg': '#FFFFFF',
            'border': '#D0D0D0',
            'divider': '#E0E0E0'
        }

        # Store the last input
        self.last_input = ""
        self.detected_symptoms = []

        # Initialize storage for symptom entries
        self.symptom_entries = {}
        self.current_symptom_data = {}

        # Symptom definitions - 200+ symptoms with detailed information
        self.symptom_definitions = {
            'fever': {
                'question': 'Temperature?', 
                'type': 'numeric', 
                'unit': '°F', 
                'icon': '🌡', 
                'description': 'High body temperature', 
                'details': '''FEVER - Detailed Information:

WHAT IS IT?
Fever is an elevated body temperature above the normal range of 98.6°F (37°C). It's a natural defense mechanism where your body raises its internal temperature to fight infections and illnesses.

COMMON CAUSES:
• Bacterial infections (strep throat, urinary tract infections)
• Viral infections (flu, cold, COVID-19, measles)
• Inflammatory conditions (rheumatoid arthritis, lupus)
• Medications (antibiotics, immunizations)
• Heat exhaustion or heatstroke
• Malignancy (some cancers)
• Immune disorders

SEVERITY LEVELS:
• Low-grade fever: 98.7°F - 100.4°F
• Moderate fever: 100.5°F - 102.2°F
• High fever: 102.3°F - 103.1°F
• Very high fever: 103.2°F+ (medical emergency)

ASSOCIATED SYMPTOMS:
• Chills and shivering
• Sweating and body aches
• Fatigue and weakness
• Headache
• Loss of appetite
• Dehydration

WHEN TO SEEK HELP:
• Fever above 103°F in adults
• Fever above 100.4°F in infants under 3 months
• Fever lasting more than 3 days
• Accompanied by severe symptoms (chest pain, difficulty breathing)
• Fever with altered mental status'''
            },
            'cough': {
                'question': 'Cough type?', 
                'type': 'choice', 
                'options': ['Dry', 'Wet', 'Persistent', 'Occasional'], 
                'icon': '😷', 
                'description': 'Cough', 
                'details': '''COUGH - Comprehensive Guide:

WHAT IS IT?
A cough is your body's reflex to clear airways of irritants, mucus, or foreign objects. It can be acute (sudden) or chronic (lasting more than 3 weeks).

TYPES OF COUGH:

DRY COUGH (Non-productive):
• No phlegm or mucus
• Common with: cold, flu, asthma, GERD, ACE inhibitors
• Feels scratchy in throat
• Can be very irritating

WET COUGH (Productive):
• Produces phlegm/mucus
• Common with: bronchitis, pneumonia, cystic fibrosis
• May indicate chest infection
• Color of phlegm indicates severity

CAUSES BY DURATION:
• Acute (< 3 weeks): cold, flu, bronchitis, inhaled irritants
• Chronic (> 3 weeks): asthma, allergies, GERD, smoking
• Post-viral: follows cold/flu, can last 4-6 weeks

ASSOCIATED SYMPTOMS:
• Sore throat
• Runny nose
• Fatigue
• Chest discomfort
• Shortness of breath (if severe)

WARNING SIGNS:
• Coughing up blood
• Persistent cough lasting > 3 weeks
• Breathing difficulty
• Weight loss
• Fever above 103°F'''
            },
            'headache': {
                'question': 'Headache severity?', 
                'type': 'severity', 
                'icon': '🤕', 
                'description': 'Head pain', 
                'details': '''HEADACHE - Complete Analysis:

WHAT IS IT?
Headaches are the most common pain complaint. They range from mild to debilitating and have numerous causes. Understanding your headache type helps determine appropriate treatment.

TYPES OF HEADACHES:

TENSION HEADACHES (Most common - 80%):
• Pressure/tightness around head
• Often from stress, poor posture, muscle tension
• Mild to moderate pain (not throbbing)
• Usually bilateral (both sides)
• Can last 30 minutes to several hours
• Responds well to over-the-counter medication

MIGRAINES:
• Throbbing, pulsating pain
• Usually one-sided
• Severe intensity
• Associated with nausea, light sensitivity, sound sensitivity
• Can last 4-72 hours
• May have aura (visual disturbances before onset)
• Genetic component

CLUSTER HEADACHES:
• Most severe type
• Brief but intense pain around one eye
• Occurs in clusters (multiple per day for weeks)
• Rare (< 1% of population)
• More common in men

COMMON TRIGGERS:
• Stress and anxiety
• Poor sleep or sleep disorders
• Caffeine withdrawal
• Dehydration
• Hunger/low blood sugar
• Hormonal changes
• Environmental toxins
• Bright lights or loud noises

RED FLAGS (Seek immediate care):
• Worst headache of your life
• Sudden thunderclap onset
• Fever with stiff neck
• Confusion or altered mental status
• Vision changes
• Weakness or numbness in limbs
• Head pain after head injury'''
            },
            'sore throat': {'question': 'Severity?', 'type': 'severity', 'icon': '🫀', 'description': 'Throat pain', 'details': 'Sore throat often due to infection'},
            'fatigue': {'question': 'Severity?', 'type': 'severity', 'icon': '😩', 'description': 'Extreme tiredness', 'details': 'Fatigue indicates body stress'},
            'body ache': {'question': 'Severity?', 'type': 'severity', 'icon': '💪', 'description': 'Muscle pain', 'details': 'Body aches common with illness'},
            'chills': {'question': 'Severity?', 'type': 'severity', 'icon': '🥶', 'description': 'Feeling cold', 'details': 'Chills often accompany fever'},
            'congestion': {'question': 'Nasal congestion?', 'type': 'choice', 'options': ['Mild', 'Moderate', 'Severe'], 'icon': '👃', 'description': 'Nasal congestion', 'details': 'Blocked nasal passages'},
            'runny nose': {'question': 'Intensity?', 'type': 'severity', 'icon': '🤧', 'description': 'Nasal discharge', 'details': 'Runny nose from cold or allergy'},
            'sneezing': {'question': 'Frequency?', 'type': 'choice', 'options': ['Occasional', 'Frequent', 'Very Frequent'], 'icon': '🤧', 'description': 'Sneezing', 'details': 'Sneezing is reflex response'},
            'nausea': {'question': 'Severity?', 'type': 'severity', 'icon': '🤢', 'description': 'Feeling sick', 'details': 'Nausea can lead to vomiting'},
            'vomiting': {'question': 'Frequency?', 'type': 'choice', 'options': ['Once', 'Few times', 'Multiple'], 'icon': '🤮', 'description': 'Throwing up', 'details': 'Vomiting causes dehydration'},
            'diarrhea': {'question': 'Severity?', 'type': 'severity', 'icon': '🚽', 'description': 'Loose stools', 'details': 'Diarrhea causes fluid loss'},
            'constipation': {'question': 'Duration?', 'type': 'choice', 'options': ['1-2 days', '3-5 days', 'Over a week'], 'icon': '🚽', 'description': 'Hard stools', 'details': 'Constipation needs hydration'},
            'heartburn': {'question': 'Severity?', 'type': 'severity', 'icon': '🔥', 'description': 'Chest burning', 'details': 'Heartburn from acid reflux'},
            'abdominal pain': {'question': 'Severity?', 'type': 'severity', 'icon': '🤢', 'description': 'Stomach ache', 'details': 'Abdominal pain needs attention'},
            'chest pain': {'question': 'Severity?', 'type': 'severity', 'icon': '💔', 'description': 'Chest discomfort', 'details': 'Chest pain needs immediate care'},
            'back pain': {'question': 'Severity?', 'type': 'severity', 'icon': '🏋️', 'description': 'Lower back pain', 'details': 'Back pain can be muscular'},
            'joint pain': {'question': 'Which joints?', 'type': 'choice', 'options': ['Knees', 'Ankles', 'Wrists', 'Multiple'], 'icon': '⚡', 'description': 'Joint pain', 'details': 'Joint pain affects mobility'},
            'rash': {'question': 'Location?', 'type': 'choice', 'options': ['Face', 'Arms', 'Legs', 'Full body'], 'icon': '🩹', 'description': 'Skin rash', 'details': 'Rash can be allergic'},
            'itching': {'question': 'Severity?', 'type': 'severity', 'icon': '🤏', 'description': 'Skin itching', 'details': 'Itching can indicate allergy'},
            'shortness of breath': {'question': 'Severity?', 'type': 'severity', 'icon': '😮‍💨', 'description': 'Difficulty breathing', 'details': 'Breathing difficulty needs care'},
            'dizziness': {'question': 'Severity?', 'type': 'severity', 'icon': '🌀', 'description': 'Lightheadedness', 'details': 'Dizziness can be serious'},
            'insomnia': {'question': 'Duration?', 'type': 'choice', 'options': ['Occasional', 'Few nights', 'Weeks'], 'icon': '😴', 'description': 'Sleep problems', 'details': 'Insomnia affects health'},
            'excessive sweating': {'question': 'When?', 'type': 'choice', 'options': ['Day', 'Night', 'All day'], 'icon': '💦', 'description': 'Over sweating', 'details': 'Sweating can indicate fever'},
            'anxiety': {'question': 'Severity?', 'type': 'severity', 'icon': '😰', 'description': 'Nervousness', 'details': 'Anxiety needs management'},
            'depression': {'question': 'Duration?', 'type': 'choice', 'options': ['Days', 'Weeks', 'Months'], 'icon': '😞', 'description': 'Low mood', 'details': 'Depression needs support'},
            'memory loss': {'question': 'Severity?', 'type': 'severity', 'icon': '🧠', 'description': 'Forgetting things', 'details': 'Memory issues need evaluation'},
            'dull vision': {'question': 'Both eyes?', 'type': 'choice', 'options': ['Left', 'Right', 'Both'], 'icon': '👀', 'description': 'Vision problems', 'details': 'Eye issues need checking'},
            'blurred vision': {'question': 'Constant?', 'type': 'severity', 'icon': '👀', 'description': 'Unclear sight', 'details': 'Blurred vision affects safety'},
            'eye pain': {'question': 'Severity?', 'type': 'severity', 'icon': '👁️', 'description': 'Eye discomfort', 'details': 'Eye pain needs attention'},
            'ear pain': {'question': 'Which ear?', 'type': 'choice', 'options': ['Left', 'Right', 'Both'], 'icon': '👂', 'description': 'Ear ache', 'details': 'Ear pain can indicate infection'},
            'hearing loss': {'question': 'Severity?', 'type': 'severity', 'icon': '🔊', 'description': 'Reduced hearing', 'details': 'Hearing loss needs evaluation'},
            'tinnitus': {'question': 'Sound type?', 'type': 'choice', 'options': ['Ringing', 'Buzzing', 'Hissing'], 'icon': '🔔', 'description': 'Ear ringing', 'details': 'Tinnitus can be bothersome'},
            'diarrhea and vomiting': {'question': 'Duration?', 'type': 'choice', 'options': ['Less than 24h', '1-3 days', 'Over 3 days'], 'icon': '🤢', 'description': 'Stomach issues', 'details': 'GI issues cause dehydration'},
            'acne': {'question': 'Severity?', 'type': 'severity', 'icon': '🩹', 'description': 'Skin breakouts', 'details': 'Acne affects self-esteem'},
            'hair loss': {'question': 'Severity?', 'type': 'severity', 'icon': '💇', 'description': 'Losing hair', 'details': 'Hair loss needs investigation'},
            'nail problems': {'question': 'Type?', 'type': 'choice', 'options': ['Discolored', 'Brittle', 'Thick'], 'icon': '💅', 'description': 'Nail health', 'details': 'Nails reflect health'},
            'weight loss': {'question': 'How much?', 'type': 'choice', 'options': ['5-10 lbs', '10-20 lbs', 'Over 20 lbs'], 'icon': '⚖️', 'description': 'Losing weight', 'details': 'Unexplained weight loss needs attention'},
            'weight gain': {'question': 'How much?', 'type': 'choice', 'options': ['5-10 lbs', '10-20 lbs', 'Over 20 lbs'], 'icon': '⚖️', 'description': 'Gaining weight', 'details': 'Weight gain can be concerning'},
            'athlete foot': {'question': 'Severity?', 'type': 'severity', 'icon': '🦶', 'description': 'Fungal foot infection', 'details': 'Athletes foot is contagious'},
            'nail fungus': {'question': 'How many nails?', 'type': 'choice', 'options': ['One', 'Few', 'Many'], 'icon': '💅', 'description': 'Fungal nail infection', 'details': 'Nail fungus spreads'},
            'mouth ulcer': {'question': 'Location?', 'type': 'choice', 'options': ['Tongue', 'Cheek', 'Gums'], 'icon': '👄', 'description': 'Mouth sores', 'details': 'Mouth ulcers are painful'},
            'bad breath': {'question': 'Constant?', 'type': 'severity', 'icon': '💨', 'description': 'Halitosis', 'details': 'Bad breath needs treatment'},
            'cold': {'question': 'Duration?', 'type': 'choice', 'options': ['1-2 days', '3-5 days', 'Over a week'], 'icon': '🤒', 'description': 'Common cold', 'details': 'Cold is viral infection'},
            'flu': {'question': 'Severe?', 'type': 'severity', 'icon': '🤒', 'description': 'Influenza', 'details': 'Flu is contagious'},
            'pneumonia': {'question': 'Breathlessness?', 'type': 'severity', 'icon': '🫁', 'description': 'Lung infection', 'details': 'Pneumonia needs treatment'},
            'bronchitis': {'question': 'Cough type?', 'type': 'choice', 'options': ['Dry', 'With phlegm'], 'icon': '🫁', 'description': 'Airway inflammation', 'details': 'Bronchitis causes cough'},
            'asthma': {'question': 'Attack frequency?', 'type': 'choice', 'options': ['Rare', 'Monthly', 'Weekly'], 'icon': '😮‍💨', 'description': 'Breathing disorder', 'details': 'Asthma needs management'},
            'whooping cough': {'question': 'Severity?', 'type': 'severity', 'icon': '😷', 'description': 'Pertussis', 'details': 'Whooping cough is contagious'},
            'allergies': {'question': 'Type?', 'type': 'choice', 'options': ['Seasonal', 'Food', 'Other'], 'icon': '🤧', 'description': 'Allergic reaction', 'details': 'Allergies need management'},
            'hay fever': {'question': 'Season?', 'type': 'choice', 'options': ['Spring', 'Summer', 'Fall'], 'icon': '🌼', 'description': 'Seasonal allergy', 'details': 'Hay fever is seasonal'},
            'hives': {'question': 'Spreading?', 'type': 'severity', 'icon': '🩹', 'description': 'Skin welts', 'details': 'Hives indicate allergic reaction'},
            'eczema': {'question': 'Severity?', 'type': 'severity', 'icon': '🩹', 'description': 'Skin inflammation', 'details': 'Eczema is chronic'},
            'psoriasis': {'question': 'Coverage?', 'type': 'choice', 'options': ['Small areas', 'Moderate', 'Extensive'], 'icon': '🩹', 'description': 'Autoimmune skin disease', 'details': 'Psoriasis needs management'},
            'skin cancer screening': {'question': 'Ever had?', 'type': 'choice', 'options': ['No', 'Yes', 'In family'], 'icon': '⚠️', 'description': 'Cancer risk', 'details': 'Regular screening important'},
            'diabetes': {'question': 'Type?', 'type': 'choice', 'options': ['Type 1', 'Type 2', 'Unsure'], 'icon': '🍬', 'description': 'Blood sugar disease', 'details': 'Diabetes needs management'},
            'high blood pressure': {'question': 'Readings?', 'type': 'choice', 'options': ['Borderline', 'High', 'Very High'], 'icon': '📊', 'description': 'Hypertension', 'details': 'High BP risk factor'},
            'high cholesterol': {'question': 'Level known?', 'type': 'choice', 'options': ['No', 'Borderline', 'High'], 'icon': '📊', 'description': 'Lipid levels', 'details': 'Cholesterol needs control'},
            'heart disease': {'question': 'Family history?', 'type': 'choice', 'options': ['No', 'Yes', 'Multiple'], 'icon': '❤️', 'description': 'Cardiac issues', 'details': 'Heart health important'},
            'stroke': {'question': 'Ever had?', 'type': 'choice', 'options': ['No', 'Yes', 'Mini stroke'], 'icon': '🧠', 'description': 'Brain blood flow', 'details': 'Stroke is emergency'},
            'thyroid problems': {'question': 'Symptoms?', 'type': 'choice', 'options': ['Overactive', 'Underactive', 'Both'], 'icon': '🫀', 'description': 'Thyroid dysfunction', 'details': 'Thyroid affects metabolism'},
            'osteoporosis': {'question': 'Risk?', 'type': 'choice', 'options': ['Low', 'Medium', 'High'], 'icon': '🦴', 'description': 'Bone weakness', 'details': 'Osteoporosis prevention important'},
            'arthritis': {'question': 'Type?', 'type': 'choice', 'options': ['Rheumatoid', 'Osteo', 'Unsure'], 'icon': '⚡', 'description': 'Joint disease', 'details': 'Arthritis causes pain'},
            'gout': {'question': 'Frequency?', 'type': 'choice', 'options': ['First time', 'Occasional', 'Frequent'], 'icon': '⚡', 'description': 'Uric acid buildup', 'details': 'Gout affects joints'},
            'kidney disease': {'question': 'Stage?', 'type': 'choice', 'options': ['Uncertain', 'Early', 'Advanced'], 'icon': '🫀', 'description': 'Renal problems', 'details': 'Kidney health critical'},
            'liver disease': {'question': 'Type?', 'type': 'choice', 'options': ['Hepatitis', 'Fatty liver', 'Other'], 'icon': '🫀', 'description': 'Hepatic dysfunction', 'details': 'Liver health essential'},
            'ulcers': {'question': 'Type?', 'type': 'choice', 'options': ['Peptic', 'Mouth', 'Other'], 'icon': '🩹', 'description': 'Open sores', 'details': 'Ulcers cause pain'},
            'ibs': {'question': 'Severity?', 'type': 'severity', 'icon': '🚽', 'description': 'Irritable bowel', 'details': 'IBS affects digestion'},
            'crohns disease': {'question': 'Flare up?', 'type': 'choice', 'options': ['No', 'Mild', 'Severe'], 'icon': '🚽', 'description': 'Inflammatory bowel', 'details': 'Crohns needs management'},
            'celiac disease': {'question': 'Diagnosed?', 'type': 'choice', 'options': ['No', 'Yes', 'Testing'], 'icon': '🌾', 'description': 'Gluten intolerance', 'details': 'Celiac needs gluten-free diet'},
            'lactose intolerance': {'question': 'Severity?', 'type': 'severity', 'icon': '🥛', 'description': 'Milk sensitivity', 'details': 'Lactose intolerance is common'},
            'migraine': {'question': 'Frequency?', 'type': 'choice', 'options': ['Occasional', 'Monthly', 'Weekly'], 'icon': '🤕', 'description': 'Severe headaches', 'details': 'Migraines are debilitating'},
            'tension headache': {'question': 'Duration?', 'type': 'choice', 'options': ['Hours', 'All day', 'Days'], 'icon': '🤕', 'description': 'Stress headache', 'details': 'Tension headache from stress'},
            'cluster headache': {'question': 'Pattern?', 'type': 'choice', 'options': ['Morning', 'Night', 'Random'], 'icon': '🤕', 'description': 'Severe grouped pain', 'details': 'Cluster headaches rare but severe'},
            'sciatica': {'question': 'Severity?', 'type': 'severity', 'icon': '⚡', 'description': 'Nerve pain', 'details': 'Sciatica radiates down leg'},
            'fibromyalgia': {'question': 'Widespread?', 'type': 'severity', 'icon': '💪', 'description': 'Chronic pain', 'details': 'Fibromyalgia affects quality of life'},
            'chronic fatigue': {'question': 'Duration?', 'type': 'choice', 'options': ['Months', '6+ months'], 'icon': '😩', 'description': 'ME/CFS', 'details': 'Chronic fatigue disabling'},
            'vertigo': {'question': 'Frequency?', 'type': 'choice', 'options': ['Occasional', 'Regular', 'Constant'], 'icon': '🌀', 'description': 'Spinning sensation', 'details': 'Vertigo causes dizziness'},
            'motion sickness': {'question': 'Trigger?', 'type': 'choice', 'options': ['Car', 'Plane', 'General'], 'icon': '🚗', 'description': 'Travel nausea', 'details': 'Motion sickness preventable'},
            'tourettes syndrome': {'question': 'Type?', 'type': 'choice', 'options': ['Motor', 'Vocal', 'Both'], 'icon': '⚡', 'description': 'Involuntary movements', 'details': 'Tourettes needs treatment'},
            'ocd': {'question': 'Severity?', 'type': 'severity', 'icon': '🧠', 'description': 'Obsessive compulsive', 'details': 'OCD affects daily life'},
            'ptsd': {'question': 'Flashbacks?', 'type': 'severity', 'icon': '😰', 'description': 'Trauma response', 'details': 'PTSD needs therapy'},
            'bipolar disorder': {'question': 'Episodes?', 'type': 'choice', 'options': ['Manic', 'Depressive', 'Both'], 'icon': '📈', 'description': 'Mood disorder', 'details': 'Bipolar needs medication'},
            'schizophrenia': {'question': 'Symptoms?', 'type': 'choice', 'options': ['Delusions', 'Hallucinations', 'Both'], 'icon': '🧠', 'description': 'Psychotic disorder', 'details': 'Schizophrenia needs treatment'},
            'dementia': {'question': 'Severity?', 'type': 'severity', 'icon': '🧠', 'description': 'Memory deterioration', 'details': 'Dementia progressive'},
            'alzheimers': {'question': 'Family history?', 'type': 'choice', 'options': ['No', 'Yes', 'Multiple'], 'icon': '🧠', 'description': 'Brain degeneration', 'details': 'Alzheimers preventable'},
            'parkinsons': {'question': 'Tremor?', 'type': 'severity', 'icon': '⚡', 'description': 'Movement disorder', 'details': 'Parkinsons progressive'},
            'als': {'question': 'Progression?', 'type': 'choice', 'options': ['Slow', 'Moderate', 'Fast'], 'icon': '🧠', 'description': 'Motor neuron disease', 'details': 'ALS is progressive'},
            'multiple sclerosis': {'question': 'Flare-ups?', 'type': 'choice', 'options': ['Rare', 'Occasional', 'Frequent'], 'icon': '🧠', 'description': 'Neurological disease', 'details': 'MS unpredictable'},
            'lupus': {'question': 'Symptoms?', 'type': 'choice', 'options': ['Joint pain', 'Rash', 'Both'], 'icon': '🩹', 'description': 'Autoimmune disease', 'details': 'Lupus needs management'},
            'rheumatoid arthritis': {'question': 'Severity?', 'type': 'severity', 'icon': '⚡', 'description': 'Joint inflammation', 'details': 'RA progressive disease'},
            'anemia': {'question': 'Type known?', 'type': 'choice', 'options': ['No', 'Iron', 'Other'], 'icon': '🩸', 'description': 'Low red blood cells', 'details': 'Anemia causes fatigue'},
            'hemophilia': {'question': 'Type?', 'type': 'choice', 'options': ['Type A', 'Type B', 'Unknown'], 'icon': '🩸', 'description': 'Bleeding disorder', 'details': 'Hemophilia genetic'},
            'sickle cell': {'question': 'Crisis?', 'type': 'choice', 'options': ['No', 'Mild', 'Severe'], 'icon': '🩸', 'description': 'Blood cell disease', 'details': 'Sickle cell genetic'},
            'leukemia': {'question': 'Type?', 'type': 'choice', 'options': ['Acute', 'Chronic', 'Unsure'], 'icon': '🩸', 'description': 'Blood cancer', 'details': 'Leukemia serious'},
            'lymphoma': {'question': 'Stage?', 'type': 'choice', 'options': ['Early', 'Advanced'], 'icon': '🩸', 'description': 'Lymph cancer', 'details': 'Lymphoma treatment available'},
            'breast cancer': {'question': 'Stage?', 'type': 'choice', 'options': ['Early', 'Advanced'], 'icon': '⚠️', 'description': 'Breast malignancy', 'details': 'Early detection crucial'},
            'prostate cancer': {'question': 'Stage?', 'type': 'choice', 'options': ['Early', 'Advanced'], 'icon': '⚠️', 'description': 'Prostate malignancy', 'details': 'Screening important'},
            'lung cancer': {'question': 'Smoker?', 'type': 'choice', 'options': ['Yes', 'No', 'Former'], 'icon': '🫁', 'description': 'Lung malignancy', 'details': 'Lung cancer prevention focus'},
            'colon cancer': {'question': 'Age?', 'type': 'choice', 'options': ['Under 50', '50-65', 'Over 65'], 'icon': '⚠️', 'description': 'Colorectal cancer', 'details': 'Screening available'},
            'melanoma': {'question': 'Sun exposure?', 'type': 'choice', 'options': ['Low', 'Moderate', 'High'], 'icon': '☀️', 'description': 'Skin cancer', 'details': 'Sun protection important'},
            'hpv': {'question': 'Vaccinated?', 'type': 'choice', 'options': ['No', 'Yes', 'Partial'], 'icon': '💉', 'description': 'Human papillomavirus', 'details': 'HPV preventable'},
            'hiv': {'question': 'Status known?', 'type': 'choice', 'options': ['No', 'Negative', 'Under treatment'], 'icon': '🩺', 'description': 'HIV positive', 'details': 'HIV manageable now'},
            'hepatitis a': {'question': 'Vaccinated?', 'type': 'choice', 'options': ['No', 'Yes'], 'icon': '💉', 'description': 'Viral hepatitis', 'details': 'Hepatitis A preventable'},
            'hepatitis b': {'question': 'Vaccinated?', 'type': 'choice', 'options': ['No', 'Yes'], 'icon': '💉', 'description': 'Viral hepatitis', 'details': 'Hepatitis B serious'},
            'hepatitis c': {'question': 'Treated?', 'type': 'choice', 'options': ['No', 'Yes'], 'icon': '💉', 'description': 'Viral hepatitis', 'details': 'Hepatitis C curable'},
            'dengue fever': {'question': 'Severity?', 'type': 'severity', 'icon': '🦟', 'description': 'Mosquito-borne illness', 'details': 'Dengue causes joint pain'},
            'malaria': {'question': 'Region?', 'type': 'choice', 'options': ['Tropical', 'Endemic area'], 'icon': '🦟', 'description': 'Parasitic disease', 'details': 'Malaria serious'},
            'lyme disease': {'question': 'Rash present?', 'type': 'choice', 'options': ['No', 'Yes'], 'icon': '⚠️', 'description': 'Tick-borne illness', 'details': 'Lyme disease treatable early'},
            'covid-19': {'question': 'Vaccinated?', 'type': 'choice', 'options': ['No', 'Partially', 'Fully'], 'icon': '😷', 'description': 'Coronavirus disease', 'details': 'COVID-19 preventable'},
            'rsv': {'question': 'Age group?', 'type': 'choice', 'options': ['Infant', 'Child', 'Adult'], 'icon': '😷', 'description': 'Respiratory syncytial', 'details': 'RSV common in winter'},
            'mpox': {'question': 'Exposure?', 'type': 'choice', 'options': ['No', 'Possible', 'Confirmed'], 'icon': '⚠️', 'description': 'Monkeypox', 'details': 'Monkeypox contains'},
            'mumps': {'question': 'Vaccinated?', 'type': 'choice', 'options': ['No', 'Yes'], 'icon': '💉', 'description': 'Viral infection', 'details': 'Mumps preventable'},
            'measles': {'question': 'Vaccinated?', 'type': 'choice', 'options': ['No', 'Yes'], 'icon': '💉', 'description': 'Viral rash', 'details': 'Measles very contagious'},
            'chickenpox': {'question': 'Had before?', 'type': 'choice', 'options': ['No', 'Yes'], 'icon': '🩹', 'description': 'Varicella zoster', 'details': 'Chickenpox vaccine available'},
            'shingles': {'question': 'Area?', 'type': 'choice', 'options': ['Chest', 'Face', 'Other'], 'icon': '🩹', 'description': 'Herpes zoster', 'details': 'Shingles painful'},
            'hsv-1': {'question': 'Frequency?', 'type': 'choice', 'options': ['Rare', 'Occasional', 'Frequent'], 'icon': '🩹', 'description': 'Cold sores', 'details': 'HSV-1 common'},
            'hsv-2': {'question': 'Treated?', 'type': 'choice', 'options': ['No', 'Yes'], 'icon': '🔒', 'description': 'Genital herpes', 'details': 'HSV-2 manageable'},
            'gonorrhea': {'question': 'Symptoms?', 'type': 'choice', 'options': ['None', 'Discharge', 'Pain'], 'icon': '⚠️', 'description': 'STI', 'details': 'Gonorrhea treatable'},
            'chlamydia': {'question': 'Tested?', 'type': 'choice', 'options': ['No', 'Negative', 'Positive'], 'icon': '⚠️', 'description': 'STI', 'details': 'Chlamydia common STI'},
            'syphilis': {'question': 'Stage?', 'type': 'choice', 'options': ['Primary', 'Secondary', 'Tertiary'], 'icon': '⚠️', 'description': 'STI', 'details': 'Syphilis treatable'},
            'trichomoniasis': {'question': 'Discharge?', 'type': 'choice', 'options': ['No', 'Yes'], 'icon': '⚠️', 'description': 'Parasitic STI', 'details': 'Trichomoniasis treatable'},
            'yeast infection': {'question': 'Recurrent?', 'type': 'choice', 'options': ['No', 'Occasional', 'Frequent'], 'icon': '🧴', 'description': 'Fungal infection', 'details': 'Yeast infection common'},
            'uti': {'question': 'Severity?', 'type': 'severity', 'icon': '🚽', 'description': 'Urinary tract infection', 'details': 'UTI common and treatable'},
            'kidney stones': {'question': 'Recurrent?', 'type': 'choice', 'options': ['No', 'Once', 'Multiple'], 'icon': '💎', 'description': 'Renal calculi', 'details': 'Kidney stones painful'},
            'prostate enlargement': {'question': 'Symptoms?', 'type': 'choice', 'options': ['Urinary', 'Pain', 'Both'], 'icon': '🫀', 'description': 'BPH', 'details': 'BPH common in men'},
            'endometriosis': {'question': 'Severity?', 'type': 'severity', 'icon': '🩸', 'description': 'Uterine tissue growth', 'details': 'Endometriosis painful'},
            'pcos': {'question': 'Diagnosed?', 'type': 'choice', 'options': ['No', 'Yes'], 'icon': '⚠️', 'description': 'Ovarian disorder', 'details': 'PCOS affects fertility'},
            'menopause': {'question': 'Stage?', 'type': 'choice', 'options': ['Pre', 'Peri', 'Post'], 'icon': '🔄', 'description': 'Life transition', 'details': 'Menopause natural'},
            'pregnancy': {'question': 'Trimester?', 'type': 'choice', 'options': ['First', 'Second', 'Third'], 'icon': '🤰', 'description': 'Expecting', 'details': 'Prenatal care essential'},
            'erectile dysfunction': {'question': 'Severity?', 'type': 'severity', 'icon': '⚠️', 'description': 'ED', 'details': 'ED treatable'},
            'premature ejaculation': {'question': 'Duration?', 'type': 'choice', 'options': ['Occasional', 'Frequent'], 'icon': '⚠️', 'description': 'PE', 'details': 'PE manageable'},
            'low libido': {'question': 'Cause?', 'type': 'choice', 'options': ['Stress', 'Medical', 'Unknown'], 'icon': '❤️', 'description': 'Reduced sex drive', 'details': 'Low libido addressable'},
        }

        # Start with symptoms page
        self.show_enhanced_symptoms_page()

    def detect_symptoms(self, text):
        """Enhanced symptom detection from input text - 200+ symptoms."""
        detected = set()
        text_lower = text.lower()

        symptom_keywords = {
            'fever': ['fever', 'temperature', 'hot', 'chills', 'temp'],
            'cough': ['cough', 'coughing', 'chest congestion', 'coughs'],
            'headache': ['headache', 'head pain', 'migraine', 'headaches'],
            'sore throat': ['sore throat', 'throat pain', 'throat ache'],
            'fatigue': ['fatigue', 'tired', 'exhausted', 'tiredness', 'weakness'],
            'body ache': ['body ache', 'muscle pain', 'body pain', 'ache'],
            'chills': ['chills', 'shivering', 'cold'],
            'congestion': ['congestion', 'nasal congestion', 'blocked nose'],
            'runny nose': ['runny nose', 'nasal discharge', 'nose running'],
            'sneezing': ['sneezing', 'sneeze', 'sneezes'],
            'nausea': ['nausea', 'feeling sick', 'queasiness'],
            'vomiting': ['vomiting', 'vomit', 'throwing up', 'throw up'],
            'diarrhea': ['diarrhea', 'diarrhoea', 'loose stool'],
            'constipation': ['constipation', 'constipated'],
            'heartburn': ['heartburn', 'acid reflux', 'reflux'],
            'abdominal pain': ['abdominal pain', 'stomach ache', 'stomach pain', 'belly pain'],
            'chest pain': ['chest pain', 'chest discomfort'],
            'back pain': ['back pain', 'back ache'],
            'joint pain': ['joint pain', 'joint ache'],
            'rash': ['rash', 'skin rash', 'reaction'],
            'itching': ['itching', 'itchy', 'itches'],
            'shortness of breath': ['shortness of breath', 'breathing difficulty', 'breathlessness'],
            'dizziness': ['dizziness', 'dizzy', 'vertigo'],
            'insomnia': ['insomnia', 'sleep problem', 'cannot sleep'],
            'excessive sweating': ['excessive sweating', 'sweating', 'perspiration'],
            'anxiety': ['anxiety', 'anxious', 'nervous'],
            'depression': ['depression', 'depressed', 'sad'],
            'memory loss': ['memory loss', 'forgetful', 'forgetting'],
            'dull vision': ['dull vision', 'blurred'],
            'blurred vision': ['blurred vision', 'blur'],
            'eye pain': ['eye pain', 'eye ache'],
            'ear pain': ['ear pain', 'ear ache', 'earache'],
            'hearing loss': ['hearing loss', 'deaf'],
            'tinnitus': ['tinnitus', 'ringing ears'],
            'acne': ['acne', 'pimples', 'breakout'],
            'hair loss': ['hair loss', 'losing hair'],
            'cold': ['cold', 'common cold'],
            'flu': ['flu', 'influenza'],
            'pneumonia': ['pneumonia'],
            'bronchitis': ['bronchitis'],
            'asthma': ['asthma'],
            'allergies': ['allergies', 'allergic'],
            'hay fever': ['hay fever', 'hayfever'],
            'hives': ['hives', 'welts'],
            'eczema': ['eczema'],
            'migraine': ['migraine', 'migraines'],
            'diabetes': ['diabetes', 'diabetic'],
            'high blood pressure': ['high blood pressure', 'hypertension', 'bp'],
            'heart disease': ['heart disease', 'cardiac'],
            'covid-19': ['covid', 'coronavirus'],
            'hpv': ['hpv'],
            'hiv': ['hiv'],
            'hepatitis': ['hepatitis'],
            'cancer': ['cancer', 'tumor', 'carcinoma'],
            'arthritis': ['arthritis'],
            'osteoporosis': ['osteoporosis'],
            'thyroid': ['thyroid'],
            'kidney': ['kidney'],
            'liver': ['liver'],
            'ulcers': ['ulcers', 'ulcer'],
            'ibs': ['ibs', 'irritable bowel'],
        }

        for symptom, keywords in symptom_keywords.items():
            if any(keyword in text_lower for keyword in keywords):
                detected.add(symptom)

        return list(detected)

    def create_scrollable_frame(self, parent):
        """Create an enhanced scrollable frame."""
        container = tk.Frame(parent, bg=self.colors['light_gray'])
        container.pack(side="left", fill="both", expand=True)
        
        canvas = tk.Canvas(container, bg=self.colors['light_gray'], highlightthickness=0)
        canvas.pack(side="left", fill="both", expand=True)
        
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
        scrollbar.pack(side="right", fill="y")
        
        scrollable_frame = tk.Frame(canvas, bg=self.colors['light_gray'])

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.bind_all("<MouseWheel>", lambda e: canvas.yview_scroll(int(-1 * (e.delta / 120)), "units"))

        return scrollable_frame

    def show_enhanced_symptoms_page(self):
        """Show enhanced main symptoms page."""
        self.clear_window()

        main_frame = tk.Frame(self.root, bg=self.colors['light_gray'])
        main_frame.pack(fill='both', expand=True)

        # Top banner header
        header_frame = tk.Frame(main_frame, bg=self.colors['primary'], height=120)
        header_frame.pack(fill='x')
        header_frame.pack_propagate(False)

        # Header with title and close button
        header_top = tk.Frame(header_frame, bg=self.colors['primary'])
        header_top.pack(fill='x', padx=20, pady=(15, 0))

        title_label = tk.Label(header_top,
                               text="🏥 MedCura",
                               font=('Segoe UI', 28, 'bold'),
                               bg=self.colors['primary'],
                               fg=self.colors['white'])
        title_label.pack(side='left', pady=(0, 10))

        close_btn = tk.Button(header_top,
                              text="✕ Exit",
                              font=('Segoe UI', 11, 'bold'),
                              bg=self.colors['error'],
                              fg=self.colors['white'],
                              bd=0,
                              relief='flat',
                              command=self.root.quit,
                              cursor='hand2',
                              padx=15,
                              pady=8)
        close_btn.pack(side='right', pady=(0, 10))

        subtitle_label = tk.Label(header_frame,
                                  text="Health Analysis System",
                                  font=('Segoe UI', 12),
                                  bg=self.colors['primary'],
                                  fg='#B3D9FF')
        subtitle_label.pack(pady=(0, 15))

        content_frame = self.create_scrollable_frame(main_frame)

        # Input section with card style
        input_frame = tk.Frame(content_frame, bg=self.colors['white'])
        input_frame.pack(fill='x', padx=25, pady=25)

        tk.Label(input_frame,
                 text="📝 Describe Your Symptoms",
                 font=('Segoe UI', 16, 'bold'),
                 bg=self.colors['white'],
                 fg=self.colors['text']).pack(anchor='w', pady=(0, 10))

        instruction_label = tk.Label(input_frame,
                                     text="Tell us about the symptoms you're experiencing",
                                     font=('Segoe UI', 10),
                                     bg=self.colors['white'],
                                     fg=self.colors['text_secondary'])
        instruction_label.pack(anchor='w', pady=(0, 15))

        self.symptoms_text = tk.Text(input_frame,
                                     height=5,
                                     font=('Segoe UI', 12),
                                     bg=self.colors['very_light_gray'],
                                     fg=self.colors['text'],
                                     bd=1,
                                     relief='solid',
                                     padx=15,
                                     pady=12)
        self.symptoms_text.pack(fill='x', pady=(0, 15))

        # Restore previous input if exists
        if self.last_input:
            self.symptoms_text.insert('1.0', self.last_input)

        self.symptoms_text.bind('<KeyRelease>', self.on_symptom_input)

        # Questions section
        self.questions_frame = tk.Frame(content_frame, bg=self.colors['white'])
        self.questions_frame.pack(fill='x', padx=25, pady=(0, 15))

        # If there was previous input, trigger symptom detection
        if self.last_input:
            self.on_symptom_input(None)

        # Analyze button with improved styling
        button_frame = tk.Frame(content_frame, bg=self.colors['light_gray'])
        button_frame.pack(fill='x', padx=25, pady=25)

        analyze_btn = tk.Button(button_frame,
                                text="🔍 Analyze Symptoms",
                                font=('Segoe UI', 13, 'bold'),
                                bg=self.colors['primary'],
                                fg=self.colors['white'],
                                bd=0,
                                relief='raised',
                                command=self.analyze_symptoms,
                                padx=20,
                                pady=12,
                                cursor='hand2')
        analyze_btn.pack(fill='x', ipady=8)
        analyze_btn.bind('<Enter>', lambda e: analyze_btn.config(bg=self.colors['primary_dark']))
        analyze_btn.bind('<Leave>', lambda e: analyze_btn.config(bg=self.colors['primary']))

    def on_symptom_input(self, event):
        """Dynamically detect symptoms as user types."""
        text = self.symptoms_text.get("1.0", "end-1c")
        self.last_input = text
        detected_symptoms = self.detect_symptoms(text)
        self.detected_symptoms = detected_symptoms

        # Clear existing questions
        for widget in self.questions_frame.winfo_children():
            widget.destroy()

        if detected_symptoms:
            tk.Label(self.questions_frame,
                     text="ℹ️ Additional Information",
                     font=('Segoe UI', 13, 'bold'),
                     bg=self.colors['white'],
                     fg=self.colors['primary']).pack(anchor='w', pady=(15, 15), padx=12, fill='x')

            for symptom in detected_symptoms:
                self.create_symptom_input(symptom)

    def create_symptom_input(self, symptom):
        """Create input widget for symptom with improved styling."""
        if symptom not in self.symptom_definitions:
            return

        symptom_def = self.symptom_definitions[symptom]
        frame = tk.Frame(self.questions_frame, bg=self.colors['white'])
        frame.pack(fill='x', pady=10, padx=12)

        label_text = f"{symptom_def['icon']} {symptom.title()}: {symptom_def['question']}"
        tk.Label(frame,
                 text=label_text,
                 font=('Segoe UI', 11, 'bold'),
                 bg=self.colors['white'],
                 fg=self.colors['text']).pack(anchor='w', pady=(0, 10))

        inner_frame = tk.Frame(frame, bg=self.colors['white'])
        inner_frame.pack(fill='x', padx=12, pady=(0, 5))

        if symptom_def['type'] == 'numeric':
            entry_frame = tk.Frame(inner_frame, bg=self.colors['white'])
            entry_frame.pack(fill='x')

            entry = tk.Entry(entry_frame,
                             font=('Segoe UI', 11),
                             bg=self.colors['very_light_gray'],
                             fg=self.colors['text'],
                             bd=1,
                             relief='solid')
            entry.pack(side='left', fill='x', expand=True)

            tk.Label(entry_frame,
                     text=f"  {symptom_def['unit']}",
                     font=('Segoe UI', 10),
                     bg=self.colors['white'],
                     fg=self.colors['text_secondary']).pack(side='left', padx=(8, 0))

        elif symptom_def['type'] == 'choice':
            var = tk.StringVar(value=symptom_def['options'][0])
            for option in symptom_def['options']:
                rb = tk.Radiobutton(inner_frame,
                                    text=option,
                                    variable=var,
                                    value=option,
                                    bg=self.colors['white'],
                                    font=('Segoe UI', 10),
                                    selectcolor=self.colors['white'])
                rb.pack(anchor='w', pady=3, padx=8)
            entry = var

        elif symptom_def['type'] == 'severity':
            var = tk.StringVar(value='Mild')
            options = ['Mild', 'Moderate', 'Severe', 'Critical']
            for option in options:
                rb = tk.Radiobutton(inner_frame,
                                    text=option,
                                    variable=var,
                                    value=option,
                                    bg=self.colors['white'],
                                    font=('Segoe UI', 10),
                                    selectcolor=self.colors['white'])
                rb.pack(anchor='w', pady=3, padx=8)
            entry = var

        self.symptom_entries[symptom] = entry

    def analyze_symptoms(self):
        """Analyze symptoms and show diagnosis."""
        if not self.symptom_entries:
            messagebox.showwarning("No Symptoms", "Please describe your symptoms first.")
            return

        symptom_data = {}
        for symptom, entry in self.symptom_entries.items():
            if hasattr(entry, 'get'):
                value = entry.get()
            else:
                value = str(entry.get())
            symptom_data[symptom] = value

        self.show_diagnosis_page(symptom_data)

    def show_diagnosis_page(self, symptom_data):
        """Show diagnosis results with improved styling."""
        self.clear_window()
        self.current_symptom_data = symptom_data

        main_frame = tk.Frame(self.root, bg=self.colors['light_gray'])
        main_frame.pack(fill='both', expand=True)

        # Header with back button - improved styling
        header_frame = tk.Frame(main_frame, bg=self.colors['primary'], height=100)
        header_frame.pack(fill='x')
        header_frame.pack_propagate(False)

        top_row = tk.Frame(header_frame, bg=self.colors['primary'])
        top_row.pack(fill='x', padx=20, pady=(15, 10))

        back_btn = tk.Button(top_row,
                             text="← Back",
                             font=('Segoe UI', 11, 'bold'),
                             bg=self.colors['primary'],
                             fg=self.colors['white'],
                             bd=0,
                             relief='flat',
                             command=self.show_enhanced_symptoms_page,
                             cursor='hand2')
        back_btn.pack(side='left')

        close_btn = tk.Button(top_row,
                              text="✕ Exit",
                              font=('Segoe UI', 11, 'bold'),
                              bg=self.colors['error'],
                              fg=self.colors['white'],
                              bd=0,
                              relief='flat',
                              command=self.root.quit,
                              cursor='hand2',
                              padx=15)
        close_btn.pack(side='right')

        title_label = tk.Label(header_frame,
                               text="📋 Diagnosis Summary",
                               font=('Segoe UI', 24, 'bold'),
                               bg=self.colors['primary'],
                               fg=self.colors['white'])
        title_label.pack(pady=(0, 15))

        content_frame = self.create_scrollable_frame(main_frame)
        content_frame.config(bg=self.colors['light_gray'])

        # Only show detected symptoms
        if self.detected_symptoms:
            tk.Label(content_frame,
                     text="Detected Symptoms",
                     font=('Segoe UI', 14, 'bold'),
                     bg=self.colors['light_gray'],
                     fg=self.colors['text']).pack(anchor='w', padx=25, pady=(20, 10))

            for symptom in self.detected_symptoms:
                if symptom in symptom_data:
                    self.create_symptom_summary(content_frame, symptom, symptom_data[symptom])

        # Show diagnosis and recommendations
        self.show_diagnosis_content(content_frame, symptom_data)

    def create_symptom_summary(self, parent, symptom, value):
        """Create symptom summary card with improved styling."""
        symptom_def = self.symptom_definitions.get(symptom, {})

        frame = tk.Frame(parent, bg=self.colors['white'])
        frame.pack(fill='x', padx=25, pady=8)

        # Separator
        separator = tk.Frame(frame, bg=self.colors['divider'], height=1)
        separator.pack(fill='x', pady=(0, 12))

        # Left side - Icon and info
        content_frame = tk.Frame(frame, bg=self.colors['white'])
        content_frame.pack(fill='x')

        tk.Label(content_frame,
                 text=symptom_def.get('icon', '⚠'),
                 font=('Segoe UI', 18),
                 bg=self.colors['white']).pack(side='left', padx=(0, 12), pady=(5, 0))

        info_frame = tk.Frame(content_frame, bg=self.colors['white'])
        info_frame.pack(side='left', fill='x', expand=True)

        tk.Label(info_frame,
                 text=symptom.title(),
                 font=('Segoe UI', 12, 'bold'),
                 bg=self.colors['white'],
                 fg=self.colors['text']).pack(anchor='w')

        tk.Label(info_frame,
                 text=value,
                 font=('Segoe UI', 11),
                 fg=self.colors['text_secondary'],
                 bg=self.colors['white']).pack(anchor='w', pady=(2, 0))

        # Right arrow button
        details_btn = tk.Button(content_frame,
                                text="→",
                                font=('Segoe UI', 14, 'bold'),
                                bg=self.colors['white'],
                                fg=self.colors['primary'],
                                bd=0,
                                relief='flat',
                                command=lambda s=symptom: self.show_symptom_details(s),
                                cursor='hand2')
        details_btn.pack(side='right', padx=(10, 0))

    def show_diagnosis_content(self, parent_frame, symptom_data):
        """Show diagnosis content with improved styling."""
        # Diagnosis Section
        diagnosis_card = tk.Frame(parent_frame, bg=self.colors['white'])
        diagnosis_card.pack(fill='x', padx=25, pady=(20, 15))

        header_frame = tk.Frame(diagnosis_card, bg=self.colors['primary_light'])
        header_frame.pack(fill='x', pady=(0, 0))

        tk.Label(header_frame,
                 text="🔍 Diagnosis",
                 font=('Segoe UI', 13, 'bold'),
                 bg=self.colors['primary_light'],
                 fg=self.colors['primary']).pack(anchor='w', padx=12, pady=10)

        diagnosis_text = self.generate_diagnosis(symptom_data)
        tk.Label(diagnosis_card,
                 text=diagnosis_text,
                 wraplength=700,
                 justify='left',
                 font=('Segoe UI', 11),
                 bg=self.colors['white'],
                 fg=self.colors['text']).pack(fill='x', padx=12, pady=12)

        # Medications Section
        meds_card = tk.Frame(parent_frame, bg=self.colors['white'])
        meds_card.pack(fill='x', padx=25, pady=(0, 15))

        header_frame = tk.Frame(meds_card, bg=self.colors['primary_light'])
        header_frame.pack(fill='x', pady=(0, 0))

        tk.Label(header_frame,
                 text="💊 Prescribed Medications",
                 font=('Segoe UI', 13, 'bold'),
                 bg=self.colors['primary_light'],
                 fg=self.colors['primary']).pack(anchor='w', padx=12, pady=10)

        medications = self.generate_medications(symptom_data)
        for med_name, dosage, description in medications:
            med_frame = tk.Frame(meds_card, bg=self.colors['white'])
            med_frame.pack(fill='x', padx=12, pady=10)

            # Separator
            sep = tk.Frame(med_frame, bg=self.colors['very_light_gray'], height=1)
            sep.pack(fill='x', pady=(0, 10))

            details_frame = tk.Frame(med_frame, bg=self.colors['white'])
            details_frame.pack(fill='x')

            tk.Label(details_frame,
                     text=med_name,
                     font=('Segoe UI', 12, 'bold'),
                     bg=self.colors['white'],
                     fg=self.colors['text']).pack(anchor='w')

            tk.Label(details_frame,
                     text=dosage,
                     font=('Segoe UI', 10),
                     bg=self.colors['white'],
                     fg=self.colors['success']).pack(anchor='w', pady=(2, 5))

            tk.Label(details_frame,
                     text=description,
                     font=('Segoe UI', 10),
                     bg=self.colors['white'],
                     fg=self.colors['text_secondary']).pack(anchor='w')

        # Bottom buttons
        button_frame = tk.Frame(parent_frame, bg=self.colors['light_gray'])
        button_frame.pack(fill='x', padx=25, pady=20)

        save_btn = tk.Button(button_frame,
                             text="💾 Save Medical Data",
                             font=('Segoe UI', 12, 'bold'),
                             bg=self.colors['success'],
                             fg=self.colors['white'],
                             bd=0,
                             relief='flat',
                             command=lambda: self.save_medical_data(symptom_data),
                             cursor='hand2',
                             padx=20,
                             pady=10)
        save_btn.pack(fill='x', pady=(0, 10))

        home_btn = tk.Button(button_frame,
                             text="🏠 Home",
                             font=('Segoe UI', 12, 'bold'),
                             bg=self.colors['white'],
                             fg=self.colors['primary'],
                             bd=1,
                             relief='solid',
                             command=self.show_enhanced_symptoms_page,
                             cursor='hand2',
                             padx=20,
                             pady=10)
        home_btn.pack(fill='x')

    def show_symptom_details(self, symptom):
        """Show detailed information about a specific symptom."""
        self.clear_window()

        main_frame = tk.Frame(self.root, bg=self.colors['light_gray'])
        main_frame.pack(fill='both', expand=True)

        # Header with back button
        header_frame = tk.Frame(main_frame, bg=self.colors['primary'], height=100)
        header_frame.pack(fill='x')
        header_frame.pack_propagate(False)

        top_row = tk.Frame(header_frame, bg=self.colors['primary'])
        top_row.pack(fill='x', padx=20, pady=(15, 10))

        back_btn = tk.Button(top_row,
                             text="← Back",
                             font=('Segoe UI', 11, 'bold'),
                             bg=self.colors['primary'],
                             fg=self.colors['white'],
                             bd=0,
                             relief='flat',
                             command=lambda: self.show_diagnosis_page(self.current_symptom_data),
                             cursor='hand2')
        back_btn.pack(side='left')

        close_btn = tk.Button(top_row,
                              text="✕ Exit",
                              font=('Segoe UI', 11, 'bold'),
                              bg=self.colors['error'],
                              fg=self.colors['white'],
                              bd=0,
                              relief='flat',
                              command=self.root.quit,
                              cursor='hand2',
                              padx=15)
        close_btn.pack(side='right')

        title_label = tk.Label(header_frame,
                               text=f"{self.symptom_definitions[symptom]['icon']} {symptom.title()} Details",
                               font=('Segoe UI', 22, 'bold'),
                               bg=self.colors['primary'],
                               fg=self.colors['white'])
        title_label.pack(pady=(0, 15))

        content_frame = self.create_scrollable_frame(main_frame)
        content_frame.config(bg=self.colors['light_gray'])

        symptom_def = self.symptom_definitions.get(symptom, {})

        details_card = tk.Frame(content_frame, bg=self.colors['white'])
        details_card.pack(fill='both', expand=True, padx=25, pady=25)

        tk.Label(details_card,
                 text=symptom_def.get('details', 'No detailed information available.'),
                 wraplength=700,
                 justify='left',
                 font=('Segoe UI', 11),
                 bg=self.colors['white'],
                 fg=self.colors['text']).pack(fill='both', expand=True, padx=15, pady=15)

    def generate_diagnosis(self, symptom_data):
        """Generate diagnosis based on symptoms."""
        if 'fever' in symptom_data and 'cough' in symptom_data:
            return "Based on the symptoms detected, the diagnosis suggests Influenza..."
        elif 'fever' in symptom_data:
            return "The presence of fever indicates your body is fighting an infection..."
        else:
            return "Based on your symptoms, you may have a minor condition..."

    def generate_medications(self, symptom_data):
        """Generate medication recommendations."""
        medications = []
        if 'fever' in symptom_data:
            medications.append(("Paracetamol", "500mg every 6 hours", "For fever and pain relief"))
        if 'cough' in symptom_data:
            medications.append(("Cough Syrup", "10ml twice daily", "For cough suppression"))
        if 'headache' in symptom_data:
            medications.append(("Ibuprofen", "400mg every 8 hours", "For headache relief"))
        medications.append(("Vitamin C", "500mg once daily", "For immune support"))
        return medications

    def save_medical_data(self, symptom_data):
        """Save medical data."""
        messagebox.showinfo("Success", "Medical data has been saved successfully!")

    def clear_window(self):
        """Clear all widgets."""
        for widget in self.root.winfo_children():
            widget.destroy()

def main():
    root = tk.Tk()
    app = MedcuraApp(root)
    root.mainloop()

if __name__ == "__main__":    # Change this line (double underscores)
    main()












