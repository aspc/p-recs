
# render_template -  api uses to generate html 
# request - object we need for forms 
from flask import Flask, jsonify, request, redirect, render_template, flash
import pandas as pd 
import pickle
from data.get_recs import recommend_courses
from data.encryption import decrypt_file

app = Flask(__name__)
  
# decrypt_files
for file_name in ['data/encrypted_all_courses.csv', 'data/encrypted_courses.csv', 'data/encrypted_vectors_all_attributes.pkl']:
    decrypt_file(file_name)

with open("data/decrypted_vectors_all_attributes.pkl", "rb") as handle:
    vector_courses = pickle.load(handle)

@app.route('/')
def index():
    return render_template('index.html') 

@app.route('/rec',methods=['POST'])
def getvalue():
	try:
		query = request.form['search']
		# TODO: change filters
		# lowlvl = 'lowlvl' in request.form
		# dept_filter = 'dept_filter' in request.form
		df = recommend_courses(query, vector_courses)

		return render_template('result.html', tables = df, query = query)
	except Exception as e:
		error = "We are temporarily unable to process your request. Please contact product@aspc.pomona.edu."
		return render_template('index.html', error = error) 

if __name__ == '__main__':
    app.run(debug=True)
