import sqlite3
import numpy as np
import pandas as pd
from sklearn.metrics import pairwise_distances

# Load user data and visualizations from the database.
con = sqlite3.connect('../DDBB/DataWarehouse.db')
df_views = pd.read_sql_query("SELECT * FROM views", con)

# Create the array of users by viewed items (We use the OLAP Pivot operation)
user_matrix_elements = pd.pivot_table(df_views, values='avg_rating', index='user_id', columns='show_id')

def recommend_shows(user, user_matrix_elements, n):

    # Calculates the cosine similarity between users.
    user_matrix_elements = user_matrix_elements.fillna(0)
    user_similarity = 1 - pairwise_distances(user_matrix_elements, metric='cosine')

    # Find the most similar users
    user_indexes = user_matrix_elements.index
    user_index = np.where(user_indexes == user)[0][0]
    similarities = list(zip(user_indexes, user_similarity[user_index]))
    similarities.sort(key=lambda x: x[1], reverse=True)
    similar_users = [similarity[0] for similarity in similarities[1:]]

    # Finds the items the user has viewed
    viewed_items = user_matrix_elements.loc[user]
    viewed_items = viewed_items[~(viewed_items == 0)].index

    # Finds items that similar users have seen but the user has not seen.
    recommendations = {}
    for similar_user in similar_users:
        similar_viewed_items = user_matrix_elements.loc[similar_user]
        similar_viewed_items = similar_viewed_items[~(similar_viewed_items == 0)].index
        no_viewed_items = set(similar_viewed_items) - set(viewed_items)
        for item in no_viewed_items:
            if item in recommendations:
                recommendations[item] += similarities[similar_users.index(similar_user)][1]
            else:
                recommendations[item] = similarities[similar_users.index(similar_user)][1]

    # Sorts the recommendations by similarity and returns the first n
    sorted_recommendations = sorted(recommendations.items(), key=lambda x: x[1], reverse=True)[:n]
    return [recommendation[0] for recommendation in sorted_recommendations]


# Asks the user to enter the input data
user = int(input('Enter the user ID: '))
while user <= 0 or user > 300:
    user = int(input('The User ID must be between 1 and 300:'))

x = int(input('Enter the number of items to recommend (maximum 10): '))
while x <= 0 or x > 10:
    x = int(input('The number of items to be recommended must be between 1 and 10:'))

# Gets recommendations and prints them on the screen
recommendations = recommend_shows(user, user_matrix_elements, x)
sql_query = "SELECT title FROM show WHERE show_id IN ({})".format(','.join("'" + s + "'" for s in recommendations))
df_recommendations = pd.read_sql_query(sql_query, con)
print(df_recommendations)