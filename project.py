# -*- coding: utf-8 -*-
"""project.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1CP9SXrkoryctEZIrqeYcXevzTPlQWrs_
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
df = pd.read_csv('final dataset.csv',encoding='latin1')
print(df.head())
print(df.columns)

# Check for missing values
print(df.isnull().sum())

# Preview unique values in 'hashtags'
print(df['hashtags'].unique())

df['comments'].fillna('', inplace=True)
df['hashtags'].fillna('', inplace=True)
print(df.isnull().sum())

import re
import nltk
from nltk.corpus import stopwords

# Download the stopwords dataset if not already downloaded
nltk.download('stopwords')
stop_words = set(stopwords.words('english'))

# Function to clean the text
def preprocess_text(text):
    # Remove special characters, punctuation, and numbers
    text = re.sub(r'[^A-Za-z\s]', '', text)  # Keep only letters and spaces
    # Convert to lowercase
    text = text.lower()
    # Remove stopwords
    text = ' '.join([word for word in text.split() if word not in stop_words])
    return text

# Apply text preprocessing to the comments column
df['cleaned_comments'] = df['comments'].apply(preprocess_text)

# Preview the cleaned comments
print(df[['comments', 'cleaned_comments']].head())

# Clean the 'likes' column: remove commas and invalid characters, and convert to numeric
df.loc[:, 'likes'] = df['likes'].astype(str).str.replace(',', '', regex=True)  # Remove commas
df.loc[:, 'likes'] = pd.to_numeric(df['likes'], errors='coerce')  # Convert to numeric, invalid values become NaN

# Drop rows with NaN likes (invalid entries)
df = df.dropna(subset=['likes'])

# Ensure 'likes' is of integer type
df.loc[:, 'likes'] = df['likes'].astype(int)

# Generate a sequential timeline for posts based on their order in the dataset
df['post_index'] = range(1, len(df) + 1)  # Create a synthetic 'post_index' column

# Group posts into "months" or periods based on index (e.g., batches of 30 for months)
df['month'] = (df['post_index'] - 1) // 30  # Each 30 posts = 1 month

# Calculate the average likes for each "month"
monthly_likes = df.groupby('month')['likes'].mean()

# Plot a histogram for the distribution of likes
plt.figure(figsize=(10, 6))
plt.hist(df['likes'], bins=30, color='skyblue', edgecolor='black')
plt.title('Distribution of Likes')
plt.xlabel('Number of Likes')
plt.ylabel('Frequency')
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.show()

from collections import Counter
df['hashtags'] = df['hashtags'].fillna('')  # Replace NaN with empty strings
all_hashtags = [hashtag.strip() for hashtags in df['hashtags'] for hashtag in hashtags.split(',') if hashtag]

# Count occurrences of each hashtag
hashtag_counts = Counter(all_hashtags)
# Print hashtags and their counts line by line
for hashtag, count in hashtag_counts.items():
    print(f"{hashtag}: {count}")

# Get the top 10 hashtags and their counts
top_10_hashtags = hashtag_counts.most_common(10)
top_10_labels, top_10_values = zip(*top_10_hashtags)
print(top_10_labels)
print(top_10_values)

# Calculate the distribution of likes for the top 5 hashtags
likes_by_top_hashtags = {tag: 0 for tag in top_10_labels}
for _, row in df.iterrows():
    post_hashtags = [tag.strip() for tag in row['hashtags'].split(',') if tag]
    for tag in post_hashtags:
        if tag in top_10_labels:
            likes_by_top_hashtags[tag] += row['likes']
likes_by_top_hashtags = {tag: likes for tag, likes in likes_by_top_hashtags.items() if likes > 0}
for hashtag, likes in likes_by_top_hashtags.items():
    print(f"{hashtag}: {likes}")

plt.figure(figsize=(8, 8))
plt.pie(likes_by_top_hashtags.values(), labels=top_10_labels, autopct='%1.1f%%', startangle=140, colors=plt.cm.Paired.colors)
plt.title('Distribution of Likes Among Top 10 Hashtags')
plt.show()

# Check for rows matching the keywords
workout_keywords = ['#workout', '#challenge', '#transformation', '#30DayChallenge', '#fitnessstory']
igtv_keywords = ['longworkout', 'tutorial', 'IGTV']
matched_posts = df[df['hashtags'].str.contains('|'.join(workout_keywords), case=False)]
matched_posts1 = df[df['hashtags'].str.contains('|'.join(igtv_keywords), case=False)]
print(f"Number of matched posts: {len(matched_posts)}")
print(f"Number of matched posts: {len(matched_posts1)}")

from textblob import TextBlob

# Function to calculate sentiment score using TextBlob
def sentiment_analysis(text):
    blob = TextBlob(text)
    # The sentiment polarity is between -1 (negative) and 1 (positive)
    return blob.sentiment.polarity

# Apply sentiment analysis to the cleaned comments
df['sentiment_score'] = df['cleaned_comments'].apply(sentiment_analysis)

# Preview the sentiment scores
print(df[['cleaned_comments', 'sentiment_score']].head())

# 1. Workout Posts and Challenges: Evaluate the popularity of daily workout routines, fitness challenges, and transformation posts. Analyze reach from sharing motivational fitness stories, before-and-after transformations, and workout challenges (e.g., #30DayChallenge).

# Filter posts related to workouts and challenges using hashtags
df['hashtags'] = df['hashtags'].astype(str)
workout_keywords = ['#workout', '#challenge', '#transformation', '#30DayChallenge', '#fitnessstory']
workout_posts = df[df['hashtags'].str.contains('|'.join(workout_keywords), case=False)]

# Calculate average likes and average sentiment score of comments
avg_likes_workout = workout_posts['likes'].mean()
avg_sentiment_score_workout = workout_posts['sentiment_score'].mean()*10000  # Average sentiment score of comments

# Display insights
print(f"Average likes for workout/challenge posts: {avg_likes_workout}")
print(f"Average sentiment score for workout/challenge posts: {avg_sentiment_score_workout}")

import matplotlib.pyplot as plt

# Bar chart for average likes and sentiment scores
categories = ['Likes', 'Sentiment Score']
values = [avg_likes_workout, avg_sentiment_score_workout]  # Replace with actual variables for sentiment scores

plt.bar(categories, values, color=['skyblue', 'orange'])
plt.title('Engagement on Workout/Challenge Posts')
plt.ylabel('Average Value')
plt.show()

#2. Engagement Rate: Measure likes, comments, and saves on workout tutorials, fitness tips, and nutritional advice. Compare the performance of Reels showcasing quick workouts or form corrections with long-format IGTV sessions.
# Categorize posts based on hashtags for Reels and IGTV
reel_keywords = ['quickworkout', 'formcorrection', 'reels']
igtv_keywords = ['longworkout', 'tutorial', 'IGTV']

# Filter posts for Reels and IGTV
reel_posts = df[df['hashtags'].str.contains('|'.join(reel_keywords), case=False)]
igtv_posts = df[df['hashtags'].str.contains('|'.join(igtv_keywords), case=False)]

# Calculate engagement metrics
avg_likes_reels = reel_posts['likes'].mean()
avg_sentiment_reels = reel_posts['sentiment_score'].mean()*10000

avg_likes_igtv = igtv_posts['likes'].mean()
avg_sentiment_igtv = igtv_posts['sentiment_score'].mean()*10000

# Display insights
print(f"Reels: Average likes = {avg_likes_reels}, Average comment length = {avg_sentiment_reels}")
print(f"IGTV: Average likes = {avg_likes_igtv}, Average comment length = {avg_sentiment_igtv}")

#3.Hashtag Strategy. Track engagement through fitness-related hashtags (e.g., #FitLife, #GymGoals, #FitnessMotivation). Differentiate performance between general fitness hashtags and niche ones (e.g. #CrossFit, #Yogainspiration).
# Define general and niche fitness hashtags
general_fitness_hashtags = ['FitLife', 'GymGoals', 'FitnessMotivation']
niche_fitness_hashtags = ['CrossFit', 'Yogainspiration']

# Filter posts for general and niche hashtags
general_posts = df[df['hashtags'].str.contains('|'.join(general_fitness_hashtags), case=False)]
niche_posts = df[df['hashtags'].str.contains('|'.join(niche_fitness_hashtags), case=False)]

# Calculate engagement for general and niche hashtags
avg_likes_general = general_posts['likes'].mean()
avg_likes_niche = niche_posts['likes'].mean()

# Display insights
print(f"General fitness hashtags: Average likes = {avg_likes_general}")
print(f"Niche fitness hashtags: Average likes = {avg_likes_niche}")

# Bar chart for hashtag engagement
categories = ['General Fitness', 'Niche Fitness']
values = [avg_likes_general, avg_likes_niche]

plt.bar(categories, values, color=['green', 'purple'])
plt.title('Engagement by Hashtag Type')
plt.ylabel('Average Likes')
plt.show()

#4.Collaborations with Fitness Brands: Analyze the impact of product sponsorships or partnerships with fitness brands (e.g., gym apparel, equipment). Evaluate the effectiveness of posts featuring fitness challenges in collaboration with trainers or gyms.
# Define keywords for collaborations
collab_keywords = ['sponsorship', 'partnership', 'brand', 'trainer', 'gym', 'apparel', 'equipment']

# Filter posts related to collaborations
collab_posts = df[df['hashtags'].str.contains('|'.join(collab_keywords), case=False)]

# Calculate engagement metrics for collaboration posts
avg_likes_collab = collab_posts['likes'].mean()
avg_sentiment_collab = collab_posts['sentiment_score'].mean()*10000

# Display insights
print(f"Collaboration posts: Average likes = {avg_likes_collab}, Average sentiment score = {avg_sentiment_collab}")

# Pie chart for collaborations
collab_count = len(collab_posts)
non_collab_count = len(df) - collab_count

labels = ['Collaborations', 'Non-Collaborations']
sizes = [collab_count, non_collab_count]
colors = ['gold', 'lightgray']
explode = (0.1, 0)  # Slightly explode the first slice

plt.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%', startangle=140)
plt.title('Collaboration vs Non-Collaboration Posts')
plt.axis('equal')
plt.show()

# Count the number of hashtags in each row
df['hashtags'] = df['hashtags'].fillna('').apply(lambda x: len(x.split(',')) if x else 0)

# Group by username and sum the hashtag counts
hashtag_counts = df.groupby('username')['hashtags'].sum().reset_index()

# Sort by hashtag count for better visualization
hashtag_counts = hashtag_counts.sort_values(by='hashtags', ascending=False)

# Print the username and the total count of hashtags
for index, row in hashtag_counts.iterrows():
    print(f"Username: {row['username']}, Total Hashtag Count: {row['hashtags']}")

print(hashtag_counts)  # Check if it contains the expected key-value pairs

import matplotlib.pyplot as plt

# Ensure the 'hashtags' column is of string type, then calculate total hashtag count for each username
df['hashtags'] = df['hashtags'].astype(str)

# Calculate the total hashtag count for each post by splitting the string based on commas
df['hashtags_count'] = df['hashtags'].apply(lambda x: len(x.split(',')) if x != 'nan' else 0)  # Handle non-string values

# Group by username and sum up the hashtag count
username_hashtag_count = df.groupby('username')['hashtags_count'].sum().reset_index()

# Sort by the total hashtag count in descending order and select the top 25
top_50_usernames = username_hashtag_count.sort_values(by='hashtags_count', ascending=False).head(50)

# Plotting the bar chart for the top 25 usernames
plt.figure(figsize=(12, 6))
plt.bar(top_50_usernames['username'], top_50_usernames['hashtags_count'], color='skyblue')
plt.xticks(rotation=45, ha='right')
plt.xlabel('Username')
plt.ylabel('Total Hashtag Count')
plt.title('Top 50 Usernames by Total Hashtag Count')
plt.tight_layout()
plt.show()

from textblob import TextBlob

# Function to calculate sentiment score using TextBlob
def sentiment_analysis(text):
    blob = TextBlob(text)
    # The sentiment polarity is between -1 (negative) and 1 (positive)
    return blob.sentiment.polarity

# Apply sentiment analysis to the cleaned comments
df['sentiment_score'] = df['cleaned_comments'].apply(sentiment_analysis)

# Preview the sentiment scores
print(df[['cleaned_comments', 'sentiment_score']].head())

import nltk
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

# Assuming df['cleaned_comments'] contains your cleaned comments
# You can calculate sentiment scores using TextBlob or any method as discussed earlier

from textblob import TextBlob

# Function to calculate sentiment score using TextBlob
def sentiment_analysis(text):
    blob = TextBlob(text)
    return blob.sentiment.polarity  # Returns a sentiment polarity score between -1 and 1

# Apply sentiment analysis to the cleaned comments
df['sentiment_score'] = df['cleaned_comments'].apply(sentiment_analysis)

# Convert continuous sentiment scores into binary labels (0 for negative, 1 for positive)
df['sentiment_label'] = df['sentiment_score'].apply(lambda x: 1 if x > 0 else 0)

# Prepare data for training
X = df['cleaned_comments']  # Text data
y = df['sentiment_label']   # Sentiment labels (binary)

# Split the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# TF-IDF Vectorization
tfidf_vectorizer = TfidfVectorizer(max_features=5000)  # Limiting to top 5000 features (words)
X_train_tfidf = tfidf_vectorizer.fit_transform(X_train)
X_test_tfidf = tfidf_vectorizer.transform(X_test)

# Train a Logistic Regression classifier
clf = LogisticRegression()
clf.fit(X_train_tfidf, y_train)

# Predict sentiment on the test set
y_pred = clf.predict(X_test_tfidf)

# Evaluate the model
accuracy = accuracy_score(y_test, y_pred)
print(f'Accuracy: {accuracy}')

# Apply the trained model to predict sentiment on the entire dataset
df['predicted_sentiment'] = clf.predict(tfidf_vectorizer.transform(df['cleaned_comments']))

# Preview the predicted sentiments
print(df[['cleaned_comments', 'predicted_sentiment']].head())

df['comments_count'] = df['comments'].apply(lambda x: len(str(x).split()))

# Convert 'likes' and 'comments_count' to strings first, then remove commas
df['likes'] = df['likes'].astype(str).str.replace(',', '')
df['comments_count'] = df['comments_count'].astype(str).str.replace(',', '')

# Convert to numeric (this will convert invalid parsing to NaN, which can be filled)
df['likes'] = pd.to_numeric(df['likes'], errors='coerce')
df['comments_count'] = pd.to_numeric(df['comments_count'], errors='coerce')
df['likes'].fillna('', inplace=True)
df['comments_count'].fillna('', inplace=True)
print(df[['likes', 'comments_count']].head())

# Ensure the 'likes' column is treated as a string before replacing commas
df['likes'] = pd.to_numeric(df['likes'].astype(str).str.replace(',', ''), errors='coerce')

# Ensure the 'comments_count' column is treated as a string before replacing commas
df['comments_count'] = pd.to_numeric(df['comments_count'].astype(str).str.replace(',', ''), errors='coerce')

# Fill any NaN values with 0
df.fillna(0, inplace=True)

print(df.dtypes)

# Define the input features (X) and target (y)
X = df[['hashtags_count', 'sentiment_score']]  # Features
y = df['likes']  # Target variable

# Split the data into training and testing sets
from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Check the shapes of the training and testing sets
print("X_train shape:", X_train.shape)
print("y_train shape:", y_train.shape)

from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.svm import SVR
from sklearn.metrics import mean_squared_error

# Dictionary to store model results
results = {}

# Function to train and evaluate a model
def train_and_evaluate_model(model, X_train, y_train, X_test, y_test, model_name):
    # Train the model
    model.fit(X_train, y_train)

    # Predict on the test set
    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    results[model_name] = mse
    # Return the predictions for comparison
    return y_pred

# 1. Random Forest Regressor
rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
rf_predictions = train_and_evaluate_model(rf_model, X_train, y_train, X_test, y_test, "Random Forest")

# 2. Linear Regression
lr_model = LinearRegression()
lr_predictions = train_and_evaluate_model(lr_model, X_train, y_train, X_test, y_test, "Linear Regression")

# 3. Support Vector Regressor (SVR)
svr_model = SVR(kernel='rbf')  # Using RBF kernel
svr_predictions = train_and_evaluate_model(svr_model, X_train, y_train, X_test, y_test, "Support Vector Regressor")

# Print the comparison of MSE for all models
print("\nModel Comparison (Mean Squared Error):")
for model_name, mse in results.items():
    print(f"{model_name}: {mse}")

from sklearn.metrics import classification_report
import numpy as np

# Define a function to categorize engagement into classes
def categorize_engagement(values, thresholds=[1000, 10000]):
    """
    Categorizes engagement into 3 classes:
    0 - Low, 1 - Medium, 2 - High
    """
    categories = []
    for val in values:
        if val < thresholds[0]:
            categories.append(0)  # Low engagement
        elif thresholds[0] <= val < thresholds[1]:
            categories.append(1)  # Medium engagement
        else:
            categories.append(2)  # High engagement
    return np.array(categories)

# Apply categorization to actual test values
y_test_class = categorize_engagement(y_test)

# Function to train, evaluate, and generate classification report
def train_evaluate_classification(model, X_train, y_train, X_test, y_test, model_name):
    # Train the model
    model.fit(X_train, y_train)

    # Predict on the test set
    y_pred = model.predict(X_test)

    # Categorize the predictions
    y_pred_class = categorize_engagement(y_pred)

    # Get the unique classes present in the true test set
    unique_classes = np.unique(np.concatenate((y_test_class, y_pred_class)))
    target_names = ['Low', 'Medium', 'High'][:len(unique_classes)]

    # Generate classification report
    report = classification_report(y_test_class, y_pred_class, labels=unique_classes, target_names=target_names, zero_division=0)
    print(f"\n{model_name} - Classification Report:\n")
    print(report)

    return y_pred_class

# 1. Random Forest Regressor
rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
rf_pred_class = train_evaluate_classification(rf_model, X_train, y_train, X_test, y_test, "Random Forest")

# 2. Linear Regression
lr_model = LinearRegression()
lr_pred_class = train_evaluate_classification(lr_model, X_train, y_train, X_test, y_test, "Linear Regression")

# 3. Support Vector Regressor (SVR)
svr_model = SVR(kernel='rbf')
svr_pred_class = train_evaluate_classification(svr_model, X_train, y_train, X_test, y_test, "Support Vector Regressor")

# Create a plot to compare actual vs predicted values for all models
plt.figure(figsize=(10, 6))

# Scatter plot for Random Forest predictions
plt.scatter(y_test, rf_predictions, label='Random Forest', color='blue')

# Scatter plot for Linear Regression predictions
plt.scatter(y_test, lr_predictions, label='Linear Regression', color='green')

# Scatter plot for SVR predictions
plt.scatter(y_test, svr_predictions, label='SVR', color='red')
plt.plot([min(y_test), max(y_test)], [min(y_test), max(y_test)], color='black', linestyle='--')

# Labels
plt.xlabel('Actual Likes')
plt.ylabel('Predicted Likes')
plt.title('Model Predictions Comparison')
plt.legend()
plt.show()

# Choose the predictions of the specific model (e.g., Linear Regression)
comparison = pd.DataFrame({'Actual': y_test, 'Predicted': lr_predictions})
print(comparison.head())
plt.scatter(y_test, lr_predictions)
plt.xlabel('Actual Likes')
plt.ylabel('Predicted Likes')
plt.title('Actual vs Predicted Likes (Linear Regression)')
plt.show()

# Choose the predictions of the specific model (e.g., Random forest)
comparison = pd.DataFrame({'Actual': y_test, 'Predicted': rf_predictions})
print(comparison.head())
plt.scatter(y_test, rf_predictions)
plt.xlabel('Actual Likes')
plt.ylabel('Predicted Likes')
plt.title('Actual vs Predicted Likes (Random Forest)')
plt.show()

# Choose the predictions of the specific model (e.g., SVR Regression)
comparison = pd.DataFrame({'Actual': y_test, 'Predicted': svr_predictions})
print(comparison.head())
plt.scatter(y_test, svr_predictions)
plt.xlabel('Actual Likes')
plt.ylabel('Predicted Likes')
plt.title('Actual vs Predicted Likes (Support Vector Machine))')
plt.show()

df_grouped = df.groupby('username').agg({'hashtags_count': 'sum', 'sentiment_score': 'mean'}).reset_index()
print(df_grouped.head())

from sklearn.linear_model import LinearRegression

svr_model = SVR(kernel='rbf')
svr_model.fit(X_train, y_train)
df_grouped['predicted_likes'] = lr_model.predict(df_grouped[['hashtags_count', 'sentiment_score']])

# Assign recommendations such that half get "Can be followed" and half get "Content is not efficient"
mid_index = len(df_grouped) // 2  # Find the midpoint index

# Dynamically format the predicted likes within the recommendation
df_grouped['recommendation'] = [
    f"Can be followed for fitness connect as {round(row['predicted_likes'])} likes predicted"
    if i < mid_index
    else f"Content is not efficient to follow as only {round(row['predicted_likes'])} likes predicted"
    for i, row in df_grouped.iterrows()
]

# Select and print the recommendation dataframe
recommendation_df = df_grouped[['username', 'recommendation']]
print(recommendation_df.to_string())

def get_user_recommendation(username):
    user_info = recommendation_df[recommendation_df['username'] == username]
    if not user_info.empty:
        # If the user exists in the dataset, print their recommendation
        recommendation = user_info['recommendation'].values[0]
        print(f"{recommendation}")
    else:
        print(f"Username '{username}' not found in the dataset.")

# Example usage: Enter a specific username to get a recommendation
user_input = input("Enter a username to check recommendation: ")
get_user_recommendation(user_input)