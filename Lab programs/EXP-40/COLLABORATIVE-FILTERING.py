# Experiment 40: Recommendation System using Collaborative Filtering

import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

# User-Item Rating Matrix (Rows: Users U1-U4, Columns: Movies M1-M5)
# 0 represents unrated movie
ratings = np.array([
    [5, 4, 0, 1, 0],  # User 1
    [4, 0, 0, 1, 2],  # User 2
    [1, 1, 0, 5, 4],  # User 3
    [0, 0, 4, 4, 5]   # User 4
])

# Compute User Similarity Matrix using Cosine Similarity
user_sim = cosine_similarity(ratings)

def predict_rating(user_id, item_id):
    sim_scores = user_sim[user_id]
    item_ratings = ratings[:, item_id]
    
    # Filter users who have rated the item
    rated_idx = item_ratings > 0
    if not np.any(rated_idx):
        return 0.0
    
    weighted_sum = np.dot(sim_scores[rated_idx], item_ratings[rated_idx])
    sum_sim = np.sum(sim_scores[rated_idx])
    return weighted_sum / sum_sim if sum_sim != 0 else 0.0

print("=== COLLABORATIVE FILTERING RECOMMENDER SYSTEM ===")
print("User-Item Ratings Matrix (4 Users x 5 Movies):")
print(ratings)

target_user = 0 # User 1
print(f"\nPredictions for User {target_user + 1}:")
for movie_id in range(ratings.shape[1]):
    if ratings[target_user, movie_id] == 0:
        predicted = predict_rating(target_user, movie_id)
        print(f"  Movie M{movie_id+1}: Predicted Rating = {predicted:.2f} / 5.0")
