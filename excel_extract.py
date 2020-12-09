import pandas as pd
from difflib import get_close_matches
import json
import string
from flask import jsonify, request, send_file, Flask


def excel_villages():
    read = pd.read_excel("lbn_villages.xlsx", sheet_name = "Locations")
    labels = read["Location_Name_En"].tolist()
    return labels

def autocorrect(village, labels):
    if village in labels:
        return(village)
    else:
        correct = get_close_matches(village, labels)
        while True:
            if correct == []:
                auto_json(correct, village)
                memory = json.loads(request.form.get('Memory'))
                answers = memory['twilio']['collected_data']['Covid19_Response']['answers']
                village = answers['Villages']['answer']
                if village in labels:
                    return village
                else:
                    correct = get_close_matches(village, labels)
            else:
                if correct[0].upper() == village.upper():
                    return(correct[0])
                else:
                    auto_json(correct, village)
                    memory = json.loads(request.form.get('Memory'))
                    answers = memory['twilio']['collected_data']['Covid19_Response']['answers']
                    village = answers['Villages']['answer']
                    if village in labels:
                        return(village)

def auto_json(village_options, village):
    if village_options == []:
        return jsonify(actions = [{"collect":{"name":"Covid19_Response","questions":[{"question":f"No village was found under {village} please type it a different way or try a different name.","name":"Villages"}]}}])
    else:
        return jsonify(actions = [{"collect":{"name":"Covid19_Response","questions":[{"question":f"No village was found under {village}, here are similar villages. {village_options} Type the village if it is in the options or retype it a different way or a different name.","name":"Villages"}]}}])
