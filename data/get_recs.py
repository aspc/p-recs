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



def filter_attributes(all_courses, courses_df, course_area, campus_list, selected_days):
    # def filter_course_area(course_area):
    #     return all_courses['CourseArea'] == course_area

    # def filter_campus(campus_list):
    #     all_courses['Campus'].isin(campus_list)
    campus_list = campus_list
    course_area = course_area

    def filter_days(selected_days):
        all_courses["Weekdays_Str"] = all_courses.Weekdays.apply(lambda a: "".join(a))

        selected_days_set = set(selected_days)  
        filtered_courses = all_courses[all_courses["Weekdays_Str"].apply(lambda weekdays: set(weekdays).issubset(selected_days_set))]
        return filter_days
    
    all_courses = filter_days(all_courses)
    filter_courses = all_courses.query("Campus in @campus_list and CourseArea in @course_area")
    course_recs = filter_courses["CourseCode"].unique().tolist()

    return courses_df.query('CourseCode == @course_recs')


def get_embedding(list_str):
    
    # Embed a line of text
    response = openai.Embedding.create(
        model= "text-embedding-ada-002",
        input = list_str
    )
    
    # Extract the AI output embedding as a list of floats
    embedding = response["data"]
    
    return embedding[0]['embedding']

def recommend_courses(query, courses_df, number_of_courses=10):
    # Get the embeddings of the query string
    query_embedding = get_embedding(query)

    # calculate the similarity between thr query_embedding and the courses_df['vector] column
    courses_df['similarity'] = courses_df['vector'].apply(lambda x: cosine_similarity(query_embedding, x))
    
    # Sort the courses by similarity and return the top 5
    recommended_courses = courses_df.sort_values('similarity', ascending=False).head(number_of_courses)
    
    return recommended_courses
