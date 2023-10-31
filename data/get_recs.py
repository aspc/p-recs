import numpy as np
from numpy import dot
from numpy.linalg import norm
import pandas as pd
import pickle
import openai
from openai.embeddings_utils import get_embedding, cosine_similarity
import os 

openai_api_key = os.environ.get("openai_api_key")
openai.api_key = openai_api_key

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
