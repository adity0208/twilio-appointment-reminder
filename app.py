import json
from flask import Flask, request, jsonify
from twilio.rest import Client
import spacy
import requests

app = Flask(__name__)

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

# Load config and user data
with open("config.json", "r") as f:
    config = json.load(f)

# Twilio configuration
twilio_config = {
    "account_sid": "your_account_sid",
    "auth_token": "your_auth_token",
    "twilio_number": "your_twilio_number"
}

client = Client(twilio_config['account_sid'], twilio_config['auth_token'])

def translate_text(text, target_language):
    api_url = "https://libretranslate.com/translate"
    headers = {
        'Content-type': 'application/json'
    }
    body = {
        'q': text,
        'source': 'auto',
        'target': target_language
    }
    response = requests.post(api_url, headers=headers, json=body)
    return response.json()['translatedText']

def personalize_message(user, message_template):
    return message_template.format(name=user['name'], time=user['appointment_time'])

@app.route('/handle-voice-response', methods=['POST'])

def handle_voice_response():
    response = request.form['SpeechResult']
    user_language = config['users'][0]['preferred_language']
    translated_response = translate_text(response, 'en')
    
    doc = nlp(translated_response.lower())
    if "yes" in translated_response or "confirm" in translated_response:
        action = "confirm"
    elif "no" in translated_response or "cancel" in translated_response:
        action = "cancel"
    elif "reschedule" in translated_response:
        action = "reschedule"
    else:
        action = "unknown"
    
    return jsonify({"action": action})

@app.route('/make-call', methods=['POST'])
def make_call():
    data = request.get_json()
    user = config['users'][0]
    message_template = "Hello {name}, this is a reminder for your appointment at {time}."
    personalized_message = personalize_message(user, message_template)
    translated_message = translate_text(personalized_message, user['preferred_language'])
    
    call = client.calls.create(
        twiml=f'<Response><Say>{translated_message}</Say></Response>',
        to=user['phone_number'],
        from_=twilio_config['twilio_number']
    )
    return jsonify({"status": "call initiated", "call_sid": call.sid})

if __name__ == '__main__':
    print("Running Flask server...")
    app.run(host='0.0.0.0', port=5000, debug=True)
