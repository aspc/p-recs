
# render_template -  api uses to generate html 
# request - object we need for forms 
from data.modify_data import clean_course_info
from flask import Flask, jsonify, request, redirect, render_template, flash
import pandas as pd 
import pickle
from data.get_recs import recommend_courses
from data.encryption import decrypt_file
from filters import get_filters
import traceback

app = Flask(__name__)

current_semester = '2023;FA'
  
# decrypt_files


for file_name in ['data/encrypted_vectors_SP24_courses.pkl']:
    decrypt_file(file_name)
    
vector_courses = pd.read_pickle("data/decrypted_vectors_SP24_courses.pkl")

# modify course data (note: could be done before encryption)
clean_course_info(vector_courses)

@app.route('/')
def index():
    return render_template('index.html', current_semester = current_semester) 

@app.route('/rec',methods=['POST'])
def getvalue():
	try:
		query = request.form['search']

		course_area = request.form['department']

		selected_days = request.form.getlist('days')  
        
		campus_list = request.form.getlist('campus')    

		df = recommend_courses(query, courses_df = vector_courses,
									 course_area= course_area,
									 campus_list= campus_list, selected_days=selected_days)
  
		filters = get_filters(course_area, campus_list, selected_days)

		return render_template('result.html', tables = df, query = query, current_semester = current_semester, is_empty = df.empty, filters=filters)
        
	except Exception as e:
		traceback.print_exc()  # Print the error traceback
		error = "We are temporarily unable to process your request. Please contact product@aspc.pomona.edu."
		return render_template('index.html',  error = error) 

if __name__ == '__main__':
    app.run(debug=True)
