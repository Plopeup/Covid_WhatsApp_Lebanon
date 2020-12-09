import json
import string
from whatsapp import whatsapp_message
from flask import jsonify, request, send_file, Flask
from excel_extract import excel_villages, autocorrect
import pandas as pd
from difflib import get_close_matches

app = Flask(__name__)

@app.route('/')
def home():
    return 'Hello World!'

@app.route('/dynamicsay', methods=['POST'])
def dynamic_say():
    return send_file('dynamicsay.json')

@app.route('/collect',  methods=['POST'])
def collect():
    memory = json.loads(request.form.get('Memory'))

    answers = memory['twilio']['collected_data']['Covid19_Symptoms']['answers']

    short_breath = answers['Shortness of breath']['answer']
    fever = answers['Fever']['answer']
    chest_pain = answers['Chest Pain']['answer']
    cough = answers['Cough']['answer']
    blue_lips = answers['Bluish Lips']['answer']

    check_list = [short_breath, fever, chest_pain, cough, blue_lips]
    if "No" in check_list:
        message = ('You do not display the symptoms for Covid-19, but please excercise caution!')
        return jsonify(actions=[{'say': {'speech': message}}])
    else:
        message = ('You may have Covid-19, just answer these questions and we can help.')
        return jsonify(actions=[{"say": {"speech": message}}, {"redirect": "http://d029d817.ngrok.io/corona"}])

@app.route('/corona', methods = ['POST'])
def corona():
    return send_file('corona_suspect.json')

@app.route('/followup', methods = ['POST'])
def followup():
    memory = json.loads(request.form.get('Memory'))

    answers = memory['twilio']['collected_data']['Covid19_Support']['answers']

    age = answers['Age']['answer']
    conditions_yn = answers['Conditions']['answer']
    contact_yn = answers['Contact_YN']['answer']
    villages_yn = answers['Villages_YN']['answer']
    full_name = answers['First_Name']['answer'] + ' ' + answers['Last_Name']['answer']

    conditions_list = [conditions_yn, contact_yn, villages_yn]
    if "Yes" not in conditions_list:
        return jsonify(actions=[{"redirect": "http://d029d817.ngrok.io/final_questions"}])
    else:
        return jsonify(actions=[{"redirect": "http://d029d817.ngrok.io/conditions"}])

@app.route('/conditions', methods = ['POST'])
def conditions():
    memory = json.loads(request.form.get('Memory'))

    answers = memory['twilio']['collected_data']['Covid19_Support']['answers']
    conditions_yn = answers['Conditions']['answer']

    if conditions_yn == "No":
        return jsonify(actions=[{"redirect": "http://d029d817.ngrok.io/contact"}])
    else:
        return send_file('conditions.json')

@app.route('/contact', methods = ['POST'])
def contact():
    memory = json.loads(request.form.get('Memory'))

    answers = memory['twilio']['collected_data']['Covid19_Support']['answers']
    contact_yn = answers['Contact_YN']['answer']

    if contact_yn == "No":
        return jsonify(actions=[{"redirect": "http://d029d817.ngrok.io/villages"}])
    else:
        return send_file('contact.json')

@app.route('/contact_results', methods = ['POST'])
def contact_results():
      memory = json.loads(request.form.get('Memory'))

      answers = memory['twilio']['collected_data']['Covid19_Contact']['answers']
      phone_numbers = answers['Phone_Number']['answer']

      if ',' in phone_numbers:
          numbers = phone_numbers.split(',')
          filtered_numbers = []
          wrong_number = False
          for n in numbers:
              temp = ''.join(i for i in n if i.isdigit())
              if len(n) < 10:
                  wrong_number = True
              else:
                  whatsapp_message(temp)
          if wrong_number == True:
              message = "There were incorrect numbers, please reach out to these contacts yourself!"
              return jsonify(actions=[{"say": {"speech": message}}, {"redirect": "http://d029d817.ngrok.io/villages"}])
      else:
          number = ''.join(i for i in phone_numbers if i.isdigit())
          if len(number) < 10:
              return jsonify(actions=[{"say": {"speech": message}}, {"redirect": "http://d029d817.ngrok.io/villages"}])
          else:
              whatsapp_message(number)
      return jsonify(actions=[{"redirect": "http://d029d817.ngrok.io/villages"}])

@app.route('/villages', methods = ['POST'])
def villages():
    memory = json.loads(request.form.get('Memory'))

    answers = memory['twilio']['collected_data']['Covid19_Support']['answers']
    villages_yn = answers['Villages_YN']['answer']

    if villages_yn == "No":
        return jsonify(actions=[{"redirect": "http://d029d817.ngrok.io/final_questions"}])
    else:
        return send_file('villages.json')

@app.route('/final_questions', methods = ['POST'])
def final_questions():
    return send_file('final.json')

@app.route('/final_statement', methods = ['POST'])
def final_statement():
    return send_file('statement.json')
