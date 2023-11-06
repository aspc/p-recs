
# render_template -  api uses to generate html 
# request - object we need for forms 

from flask import Flask, jsonify, request, redirect, render_template, flash
import pandas as pd 
import pickle
from data.get_recs import recommend_courses, filter_course_area
from data.encryption import decrypt_file

app = Flask(__name__)
  
# decrypt_files


for file_name in ['data/encrypted_vectors_SP24_courses.pkl']:
    decrypt_file(file_name)
    

vector_courses = pd.read_pickle("data/decrypted_vectors_SP24_courses.pkl")


@app.route('/')
def index():
    return render_template('index.html') 

@app.route('/rec',methods=['POST'])
def getvalue():
	try:
		query = request.form['search']
		print(query)
                
		# TODO: change filters
		course_area = request.form['department']

		selected_days = request.form.getlist('days')  
		print(selected_days)  # return a list of days
                
		campus_list = request.form.getlist('campus')    

		print(campus_list) # return a list of campuses

		result_df = recommend_courses(query, courses_df = vector_courses,
									 course_area= course_area,
									 campus_list= campus_list, selected_days=selected_days)
                
		return render_template('result.html', tables = result_df, query = query)

	except Exception as e:
		print(e)
		error = "We are temporarily unable to process your request. Please contact product@aspc.pomona.edu."
		return render_template('index.html',  error = error) 

if __name__ == '__main__':
    app.run(debug=True)
