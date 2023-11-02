import requests
import csv
import pandas as pd
import os
from encryption import encrypt_file
from app import current_semester

api_key = os.environ.get("api_key")

# Creates list of all course areas offered at the 5Cs
course_areas = requests.get(f'http://jicsweb.pomona.edu/api/courseareas')
area_code_to_area_name = {}
for area_codes in course_areas.json():
    area_code_to_area_name[area_codes['Code']] = area_codes['Description']

# Generates url for all valid course areas of this semester and returns json
def get_area_course_info(code):
    payload = {}
    payload["api_key"] = api_key
    api_url = "https://jicsweb.pomona.edu/api/Courses/"+ current_semester + code
    r = requests.get(
        api_url, params=payload)
    if r.status_code != 200:
        print(r.content)
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

with open('data/all_courses.csv', 'w', encoding='UTF8', newline='') as f:
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

# remove duplicates courses from multiple course areas
df = pd.read_csv('data/all_courses.csv')
df['Course Area(s)'] = df['CourseArea']
duplicates = df.loc[df.duplicated(subset=['CourseCode'], keep=False), :]
print("duplicates=", duplicates)
for idx, row in duplicates.groupby('CourseCode')['CourseArea']:
    concat = ', '.join(row.values)
    df.loc[df['CourseCode'] == idx, 'Course Area(s)'] = concat
    df.drop_duplicates(subset=['CourseCode'], keep='first', inplace=True)

df.drop('CourseArea', axis=1, inplace=True)
df.to_csv('data/courses.csv', index=False)
    
for file_name, encrypted_file_name in [('data/courses.csv','data/encrypted_courses.csv'),('data/all_courses.csv','data/encrypted_all_courses.csv')]:
    encrypt_file(file_name, encrypted_file_name)

