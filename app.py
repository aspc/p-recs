
# render_template -  api uses to generate html 
# request - object we need for forms 
from flask import Flask, jsonify, request, redirect, render_template, flash
import pandas as pd 
import pickle
from scipy import spatial
import os 
import json
from cryptography.fernet import Fernet
import config 
# from recommend_GloVe.recommend_GloVe_average import recommend

app = Flask(__name__)

configuration = config.Config('keys.py')

def decrypt_csv(file_name):
	fernet = Fernet(configuration["csv_encryption_key"])
	
	with open(file_name, 'rb') as enc_file:
		encrypted = enc_file.read()
	
	decrypted = fernet.decrypt(encrypted)
 
	new_file_name = file_name.replace('encrypted', 'decrypted')
	
	with open(new_file_name, 'wb') as dec_file:
		dec_file.write(decrypted)
  
# decrypt_files
for file_name in ['data/encrypted_all_courses.csv', 'data/encrypted_courses.csv']:
    decrypt_csv(file_name)


@app.route('/')
def index():
    return render_template('index.html') 

@app.route('/rec',methods=['POST'])
def getvalue():
	try:
		coursename = request.form['search'].split(" ")[0]
		lowlvl = 'lowlvl' in request.form
		dept_filter = 'dept_filter' in request.form
		df = []

		return render_template('result.html', tables = df, course = coursename)
	except Exception as e:
		error = "Invalid Course ID. Please Try Again"
		return render_template('index.html', error = error) 

if __name__ == '__main__':
    app.run(debug=True)
