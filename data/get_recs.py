import numpy as np
from numpy import dot
from numpy.linalg import norm
import pandas as pd
import pickle
import openai
from openai.embeddings_utils import get_embedding, cosine_similarity
import config 

configuration = config.Config('keys.py')
openai.api_key = configuration["openai_api_key"]


# note: all_courses is same df as courses_df
def filter_course_area(all_courses, course_area = [], campus_list = [], selected_days = [], faculty_list = []):

    course_area = [course_area]
    
    # if no filtering is needed
    if (len(course_area) == 0) & (len(campus_list) == 0) & (len(selected_days) == 0) & (len(faculty_list) == 0):
        return all_courses

    filtered_courses = all_courses

    # fiter by department
    if len(course_area) > 0: 
        selected_areas_set = set(course_area)  
        # we want the query to be a subset of entries
        filtered_courses =  filtered_courses[filtered_courses["CourseArea"].apply(lambda x: selected_areas_set.issubset(x))]

    # filter selected days
    if len(selected_days) > 0: 
        selected_days = set(selected_days)

        # get rid of empty sets
        filtered_courses = filtered_courses[filtered_courses["Weekdays"].apply(lambda x: bool(x))]

        # we want the entry to be a subset of query entered
        filtered_courses = filtered_courses[filtered_courses["Weekdays"].apply(lambda x: x.issubset(selected_days))]

    # filter campus
    if len(campus_list) > 0:
        selected_campus = set(campus_list)

        # get rid of empty sets
        filtered_courses = filtered_courses[filtered_courses["Campus"].apply(lambda x: bool(x))]

        # we want entry to be a subset of query entered
        filtered_courses = filtered_courses[filtered_courses["Campus"].apply(lambda x: x.issubset(selected_campus))]

    if len(faculty_list) > 0:
        selected_faculty = set(faculty_list)

        # get rid of empty sets
        filtered_courses = filtered_courses[filtered_courses["Faculty"].apply(lambda x: bool(x))]

        # we want the query to be a subset of entries
        filtered_courses = filtered_courses[filtered_courses["Faculty"].apply(lambda x: x.issubset(selected_faculty))]

    return filtered_courses


def get_embedding(list_str):
    
    # Embed a line of text
    response = openai.Embedding.create(
        model= "text-embedding-ada-002",
        input = list_str
    )
    
    # Extract the AI output embedding as a list of floats
    embedding = response["data"]
    
    return embedding[0]['embedding']

def recommend_courses(query, courses_df, course_area = [], campus_list = [], selected_days = [], faculty_list = [], number_of_courses=10):
    # Get the embeddings of the query string

    courses_df = filter_course_area(courses_df, course_area, campus_list, selected_days, faculty_list)
    
    if query is None:
        return courses_df.head(10)

    query_embedding = get_embedding(query)

    # calculate the similarity between thr query_embedding and the courses_df['vector] column
    courses_df['similarity'] = courses_df['vectors'].apply(lambda x: cosine_similarity(query_embedding, x))
    
    # Sort the courses by similarity and return the top 5
    recommended_courses = courses_df.sort_values('similarity', ascending=False).head(number_of_courses)
    
    return recommended_courses
