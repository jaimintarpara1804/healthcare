# Symptom Checker Feature

## Overview
A comprehensive symptom checker that helps users identify possible health conditions based on their symptoms and provides recommendations.

## Features

### 1. **18 Common Symptoms**
Users can select from:
- Fever, Cough, Headache, Fatigue
- Body Ache, Sore Throat, Runny Nose
- Shortness of Breath, Nausea, Dizziness
- Chest Pain, Stomach Pain, Diarrhea
- Constipation, Rash, Joint Pain
- Back Pain, Insomnia

### 2. **Smart Analysis**
- Matches symptoms to 30+ possible conditions
- Ranks conditions by symptom match count
- Shows top 5 most likely conditions

### 3. **Urgency Detection**
- Flags urgent symptoms (chest pain, shortness of breath)
- Displays urgent banner for immediate attention

### 4. **Specialist Recommendations**
Suggests the right specialist based on conditions:
- General Physician
- Cardiologist
- Pulmonologist
- Neurologist
- Gastroenterologist
- And more...

### 5. **Home Care Tips**
Provides immediate self-care advice:
- Hydration recommendations
- Rest guidelines
- Symptom-specific remedies
- When to seek help

### 6. **Next Steps**
Guides users on:
- Booking appointments
- Tracking symptoms
- Preparing for doctor visits

## How to Use

1. Navigate to **Symptom Checker** from the home page
2. Select all symptoms you're experiencing
3. Click **Check Symptoms**
4. Review the analysis and recommendations
5. Book a consultation if needed

## Technical Details

- **Route**: `/symptom_checker`
- **Template**: `templates/symptom_checker.html`
- **Method**: GET/POST
- **Authentication**: Required (login needed)

## Integration Points

- Links from Home page
- Links from Dashboard navigation
- Direct link to Consultation booking
- Session tracking ready (can be added)

## Future Enhancements

- Save symptom history
- Track symptom progression over time
- AI-powered symptom analysis
- Integration with medical databases
- Multi-language support
- Symptom severity levels
