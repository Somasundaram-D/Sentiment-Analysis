from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import matplotlib.pyplot as plt
import pandas as pd

# Initialize VADER sentiment analyzer
analyzer = SentimentIntensityAnalyzer()

# Read social media posts from CSV file using pandas
def read_posts(filename, column_name='text'):
    df = pd.read_csv(filename)

    # Check if the column exists
    if column_name not in df.columns:
        raise ValueError(f"Column '{column_name}' not found in the dataset.")

    # Step 1: Remove duplicate records
    df = df.drop_duplicates(subset=column_name)

    # Step 2: Drop missing (null) values
    df = df[column_name].dropna()

    # Step 3: Convert to string format and return as a list
    posts = df.astype(str).tolist()

    print(f"Total posts loaded: {len(posts)}")
    return posts

# Decode sentiment score to emotion
def decode_emotion(score):
    if score >= 0.5:
        return "Positive"
    elif score <= -0.5:
        return "Negative"
    else:
        return "Neutral"

# Analyze sentiments
def analyze_posts(posts):
    results = {'Positive': 0, 'Neutral': 0, 'Negative': 0}
    for post in posts:
        score = analyzer.polarity_scores(post)['compound']
        emotion = decode_emotion(score)
        results[emotion] += 1
        print(f"{post}\n-> {emotion} (Score: {score})\n")
    return results

# Display pie chart
def show_pie_chart(results):
    labels = results.keys()
    sizes = results.values()
    colors = ['green', 'gray', 'red']
    plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=140)
    plt.title("Emotion Distribution in Social Media Posts")
    plt.axis('equal')
    plt.show()

# Main execution
filename = input("Enter the filename (CSV) containing social media posts: ")
column_name = input("Enter the column name that contains the text posts (e.g., text): ")
posts = read_posts(filename, column_name)
results = analyze_posts(posts)
show_pie_chart(results)
