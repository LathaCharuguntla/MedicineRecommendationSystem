from flask import Flask, request, render_template
import pandas as pd
import numpy as np
from src.components.disease_prediction import get_predicted_disease, recommendation
import ast




app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method=='GET':
       return render_template('index.html')
    
    else:
        symptoms = request.form.get('symptoms')
        print('Entered symptoms : ', symptoms)

        disease = get_predicted_disease(symptoms)
        print('Predicted Disease: ', disease)
        description, precautions, medications_str, diets_str, workouts = recommendation(disease)
        print('Description: ', description)
        print('Precautions: ', precautions)
        print('Medications: ', medications_str)
        print('Diets : ', diets_str)
        print('Workouts: ', workouts)
        
        medications = ast.literal_eval(medications_str[0])
        diets = ast.literal_eval(diets_str[0])
        
        my_precautions = []
        for i in precautions[0]:
          my_precautions.append(i)

       
        
        return render_template('index.html', disease=disease, description=description, my_precautions=my_precautions, medications=medications, diets=diets, workouts=workouts)
    



if __name__=='__main__':
    app.run(debug=True)