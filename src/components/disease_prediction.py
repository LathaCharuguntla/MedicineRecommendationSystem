from src.utilis.common import load_csv_data
from pathlib import Path
from src.logger import logging
from src.exception import CustomException
import pandas as pd
import numpy as np
import joblib
import sys
import json
from rapidfuzz import process


root_dir = Path(__file__).resolve().parents[2]
description = load_csv_data(root_dir/'artifacts/data_ingestion/description.csv')
diets = load_csv_data(root_dir/'artifacts/data_ingestion/diets.csv')
medications = load_csv_data(root_dir/'artifacts/data_ingestion/medications.csv')
precautions = load_csv_data(root_dir/'artifacts/data_ingestion/precautions.csv')
workout = load_csv_data(root_dir/'artifacts/data_ingestion/workout.csv')

import json
import os

def load_json_file(file_path):
    """Load a JSON file and return its content."""
    if not os.path.exists(file_path):
        print(f"Error: The file {file_path} does not exist.")
        return None

    try:
        with open(file_path, 'r') as f:
            return json.load(f)

    except Exception as e:
        logging.error(f"An error occurred while loading the file {file_path}: {e}")
        raise CustomException(e, sys)

# Load symptoms and disease lists
symptoms_list = load_json_file(root_dir/'artifacts/symptoms_list/symptoms.json')
disease_list = load_json_file(root_dir/'artifacts/disease_list/disease.json')


model = joblib.load(root_dir/'artifacts/model/model.joblib')

logging.info(f'Symptoms List: {symptoms_list}')
logging.info(f'Disease List: {disease_list}')
logging.info(f'Model Loaded: {model}')


def recommendation(disease):
    desc = description[description['Disease']==disease]['Description']
    desc = desc.iloc[0]

    pre = precautions[precautions['Disease']==disease][['Precaution_1', 'Precaution_2', 'Precaution_3', 'Precaution_4']]
    pre = [val for val in pre.values]

    medi = medications[medications['Disease']==disease]['Medication']
    medi = [val for val in medi.values]

    die = diets[diets['Disease']==disease]['Diet']
    die = [val for val in die.values]

    work = workout[workout['disease']==disease]['workout']
    work = [val for val in work.values]

    return desc, pre, medi, die, work

def get_matched_symptoms(user_symptoms, symptoms_dict, threshold=80):
    matched_symptoms = []
    for symptom in user_symptoms:
        cleaned_symptom = ''.join([char for char in symptom if char.isalpha()])
        match, score,_ = process.extractOne(cleaned_symptom, symptoms_dict.keys())
        if score >= threshold:
            matched_symptoms.append(match)
        else:
            print(f"The symptom {cleaned_symptom} didnt match. Enter the correct symptoms")
    return matched_symptoms

def get_predicted_disease(symptoms):
    print(symptoms)
    input_vector = np.zeros(len(symptoms_list))
    symptoms = [symp.strip() for symp in symptoms.strip(',')]
    symptoms = [s.strip("[]' ") for s in symptoms]
    symptoms = get_matched_symptoms(symptoms, symptoms_list)    
    for item in symptoms:
        input_vector[symptoms_list[item]]=1
    predicted = model.predict([input_vector])[0]
    predicted = str(predicted)
    print('Predicted number', predicted)
    return disease_list[predicted]



if __name__=='__main__':
    dec, pre, medi, die, work = recommendation('Fungal infection')
    disease = get_predicted_disease(['itching','backpain', 'fever'])
    print('Disease: ', disease)
    

