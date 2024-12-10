
# Instagram Hashtag and Engagement Analysis Project

## Project Description
This project analyzes Instagram engagement metrics based on hashtags, comments, likes, and sentiment scores. 
The analysis focuses on various insights such as:
- Sentiment analysis of comments
- Top hashtags and their performance
- Comparison between Reels and IGTV content
- Engagement analysis of fitness-related challenges and collaborations

## Files Included
1. **project.py**: 
   - Python script for data cleaning, preprocessing, visualization, and sentiment analysis.
   - Key components:
     - Sentiment analysis using TextBlob
     - Visualization of top hashtags and likes distribution
     - Predictive modeling using Random Forest, Linear Regression, and SVR
     - User engagement classification (Low, Medium, High)
     - Recommendations based on predicted engagement.

2. **web_scrap.ipynb**:
   - Jupyter Notebook for web scraping Instagram data based on hashtags.

## Key Functionalities
- **Data Preprocessing**: Cleans text comments, removes stopwords, and processes likes.
- **Sentiment Analysis**: Calculates sentiment polarity scores for comments.
- **Visualization**:
  - Likes distribution histogram
  - Pie chart for hashtag-based likes
  - Engagement trends for Reels, IGTV, and collaborations
- **Model Training**:
  - Predictive models: Random Forest, Linear Regression, Support Vector Regression
  - Classification of engagement into Low, Medium, and High categories.
- **User Recommendations**:
  - Suggests whether a user's content is efficient to follow based on engagement.

## Requirements
Install the necessary libraries before running the scripts:
```bash
pip install pandas matplotlib seaborn nltk textblob scikit-learn
```

## Instructions
1. Ensure the dataset file (`final dataset.csv`) is available in the same directory.
2. Run the `project.py` script for analysis and visualization.
3. Use `web_scrap.ipynb` to scrape Instagram data based on hashtags.
4. Follow the prompts in the terminal to get user recommendations.

## Output
The project generates insights such as:
- Top performing hashtags
- Engagement metrics for fitness challenges and collaborations
- Sentiment analysis of user comments
- Recommendations for user content.

---
### Example Usage
Run the project script:
```bash
python project.py
```
Check recommendations for a user:
```text
Enter a username to check recommendation: username_here
Can be followed for fitness connect as 1200 likes predicted.
```

## Contributors
- **Your Name**

---
