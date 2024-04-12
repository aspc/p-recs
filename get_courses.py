import requests
import csv
import pandas as pd
import os
from data.encryption import encrypt_file
from ast import literal_eval
from get_courses import current_semester, term

import re
import openai
import numpy as np

api_key = os.environ.get("api_key")

openai.api_key = os.environ.get("openai_api_key")


# Creates list of all course areas offered at the 5Cs
course_areas = requests.get(f'http://jicsweb.pomona.edu/api/courseareas')
area_code_to_area_name = {}
for area_codes in course_areas.json():
    area_code_to_area_name[area_codes['Code']] = area_codes['Description']

# Generates url for all valid course areas of this semester and returns json
def get_area_course_info(code):
    payload = {}
    payload["api_key"] = api_key
    # current semester set in app.py
    api_url = "https://jicsweb.pomona.edu/api/Courses/"+ current_semester + "/" + code
    r = requests.get(
        api_url, params=payload)
    if r.status_code != 200:
        print(r)
        return None
    try:
        print(f"Getting courses for {code} this semester")
        return r.json()
    except Exception as e:
        print(f"No courses offered in course area {code} this semester", e)

# Parses course description for course prereqs
def get_course_prereqs(course_description):
    reqs = course_description.find("Prerequisite:")
    reqs1 = course_description.find("Prerequisites:")
    if reqs != -1:
        return course_description[reqs +
                                  len("Prerequisite:"):]
    elif reqs1 != -1:
        return course_description[reqs1 +
                                  len("Prerequisites:"):]
    return 'None'

# Returns instructors names
def get_course_faculty(course):
    course_faculty = []
    if not course["Instructors"]:
        return []
    for instructor in course['Instructors']:
        if instructor['Name'] == ', taff':
            course_faculty.append('Staff')
        else:
            course_faculty.append(instructor['Name'])
    return course_faculty

# returns (campus "SC Campus", time "02:45-05:30PM", weekdays "TR")
def get_course_sched(course):
    campus = []
    meet_time = []
    weekdays = []
    for schedule in course['Schedules']:
        campus.append(schedule['Campus'])
        meet_time.append(schedule['MeetTime'])
        weekdays.append(schedule['Weekdays'])
    return (campus, meet_time, weekdays)


# Writing data to CSV
header = ['CourseArea', 'CourseCode', 'Name', 'Description',
          'Faculty', 'Campus', 'MeetTime', 'Weekdays', 'Prereqs']

with open('data/all_courses.csv', 'a', encoding='UTF8', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(header)
    for area_code in area_code_to_area_name.keys():
        area_courses = get_area_course_info(area_code)
        if not area_courses:
            continue
        for course in area_courses:
            try:
                course_area = area_code_to_area_name[area_code]
                course_code = course['CourseCode']
                name = course['Name']
                description = str(course['Description'])
                prereqs = get_course_prereqs(description)
                faculty = get_course_faculty(course)
                campus, meet_time, weekdays = get_course_sched(course)
            except Exception as e:
                print("Expection:", e,
                      " \nInsufficient information on course ", course)
            data = [course_area, course_code, name, description,
                    faculty, campus, meet_time, weekdays, prereqs]
            writer.writerow(data)


# obtain word vectors from openai API
# if rate limit error, break up the list_str into chunks 
# calling get_embedding incrementally
def get_embedding(list_str):
    # list of word embeddings
    embedding_list = []

    # Embed a line of text
    for str in list_str:
        # Embed a line of text
        response = openai.Embedding.create(
            model= "text-embedding-ada-002",
            input = str
        )
        # Extract the AI output embedding as a list of floats
        nth_word = response.data[0]['embedding']
        embedding_list.append(nth_word)
    
    return embedding_list


# create pkl file with proper data types
def create_vector_file(all_courses: pd.DataFrame) -> pd.DataFrame:
    # convert string of area requirements -> list -> set
    all_courses['CourseArea'] = all_courses['CourseArea'].apply(lambda x: set(x.split(", ")))

    # get rid of extra spaces and tabs in course name 
    all_courses['Name'] = all_courses['Name'].apply(lambda x: re.sub(r"\s+", " ", x).strip())

    # innermost set(x) gets rid of duplicates in the list of weekdays (['TR', 'TR'] => {'TR'})
    # min(set(x)), convert {'TR'} => 'TR'
    # set() again => 'TR' => {'T', 'R'}
    all_courses['Weekday_set'] = all_courses['Weekdays'].apply(lambda x: set(min(set(x)))) 
    all_courses['Campus'] = all_courses['Campus'].apply(lambda x: set(x)) # convert list of campus -> set

    # get word vectors, append to df
    courses = all_courses.Name.to_list()
    vector_list = get_embedding(courses)
    all_courses['vector'] = vector_list

    return all_courses



# converters ensure Faculty, Campus, MeetTime, Weekdays are lists, not a string of a list
# try decrypted_courses_sp24.csv if all_courses.csv fails

df = pd.read_csv('decrypted_all_courses.csv', converters={'Faculty': literal_eval, 'Campus': literal_eval, 'MeetTime': literal_eval, 'Weekdays': literal_eval})

vector_df = create_vector_file(df)


vector_df.to_pickle(f'data/vectors_{term}_courses.pkl') 
# pkl file to preserve data types (csv can not do this)

encrypt_file(f'data/vectors_{term}_courses.pkl', f'data/encrypted_vectors_{term}_courses.pkl')

    
