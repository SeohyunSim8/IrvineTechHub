import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.patches import Rectangle

def data():
    # Read csv file
    df = pd.read_csv('PetSupplies.csv')
    
    # Convert to numeric
    df['Price'] = pd.to_numeric(df['Price'])
    df['Reviews'] = pd.to_numeric(df['Reviews'], errors='coerce')
    df['Rating'] = pd.to_numeric(df['Rating'], errors='coerce')

    # Drop the column with no review and no rating
    df = df.dropna()

    df['Reviews'] = df['Reviews'].astype('int64')

    print(df)

    return df


# Create Recommendation column
def recommendation(df):
    df['Recommendation'] = 'N'

    rating_threshold = df['Rating'].quantile(0.7)
    review_threshold = df['Reviews'].quantile(0.7)
    print("\nTop 30% of Ratings: ", rating_threshold)
    print("Top 30% of the number of Reviews: ", review_threshold)

    df.loc[(df['Star Seller'] == 'Y') & (df['Etsy\'s Pick'] == 'Y') & (df['Reviews'] >= review_threshold) & (df['Rating'] >= rating_threshold), 'Recommendation'] = 'Y'

    print("\nCreate Recommendation column using Star Seller, Etsy’s Pick, the number of reviews and rating.\n", df)

    return df


# Histogram of the target variable (reviews)
def hist(df, title):
    data = df['Reviews'].to_numpy()
    print(max(data))
    plt.hist(data, bins=np.arange(min(data) // 100 * 100, 10000, 10000 // 15 //100 * 100), edgecolor='black')
    plt.title(title)
    plt.xlabel("Number of Reviews")
    plt.ylabel("Number of Items")
    plt.xticks(np.arange(min(data) // 100 * 100, 10000, 10000 // 15 //100 * 100))
    plt.grid(axis='y', linestyle='--', alpha=0.5)
    plt.show()


# Bar charts comparing the target variable across different categories
def bar(df):
    categories = np.arange(0, 5.5, 0.5)
    count = [len(df.loc[df['Rating'] == category]) for category in categories]

    fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True, gridspec_kw={'height_ratios': [1, 4]})

    ax1.bar(categories, count, align='center', width=0.3)
    ax1.set_title("Bar chart of Ratings")
    limit = max(count) // 5 * 5
    ax1.set_ylim(limit - 5, limit + 5)

    ax2.bar(categories, count, align='center', width=0.3)
    ax2.set_xticks(categories)
    ax2.set_xlabel("Rating")
    ax2.set_ylabel("Number of Items")
    count.sort()
    ax2.set_ylim(0, count[-2] // 5 * 5 + 10)

    plt.show()


# Scatter plot between 'Rating' and 'Reviews'
def scatter(df):
    categories = np.arange(min(df['Rating']), max(df['Rating']) + 0.5, 0.5)

    # Find best broken axis
    sort_reviews = df['Reviews'].sort_values().tolist()
    gap = np.array([sort_reviews[i] - sort_reviews[i - 1] for i in range(1, len(sort_reviews))])
    max_gap_index = np.argmax(gap)

    fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True, gridspec_kw={'height_ratios': [1, 10]})

    ax1.scatter(df['Rating'], df['Reviews'], alpha=0.1)
    ax1.set_title("Scatter plot between Rating and Reviews")
    limit = sort_reviews[max_gap_index + 1] // 5 * 5
    ax1.set_ylim(limit - 1000, limit + 1000)
    ax1.grid(axis='y', linestyle='--', alpha=0.5)

    ax2.scatter(df['Rating'], df['Reviews'], alpha=0.1)
    ax2.set_xticks(categories)
    ax2.set_xlabel("Rating")
    ax2.set_ylabel("Reviews")
    sort_reviews = [value for value in sort_reviews if value != max(sort_reviews)]
    ax2.set_ylim(0, sort_reviews[-1] // 5 * 5 + 3000)
    ax2.grid(axis='y', linestyle='--', alpha=0.5)

    plt.show()


# Dataset
df = data()

# Basic statistical measures
numeric_columns = ['Price', 'Reviews', 'Rating']

print("Mean\n", round(df[numeric_columns].mean(), 2))
print("\nMedian\n", round(df[numeric_columns].median(), 2))
print("\nStandard deviation\n", round(df[numeric_columns].std(), 2))

print("\nThe distribution of Star Seller\n", df['Star Seller'].value_counts())
print("\nThe distribution of Etsy's Pick\n", df['Etsy\'s Pick'].value_counts())
print("\nThe distribution of Free Shipping\n", df['Free Shipping'].value_counts())


# Create Recommendation column
recommendation(df)

print("\nThe distribution of Recommendation\n", df['Recommendation'].value_counts(), "\n")

rec_df = df.loc[df['Recommendation'] == 'Y']
print("\nPrint only recommendation products")
print(df.loc[df['Recommendation'] == 'Y', ['Product Name', 'Price', 'Star Seller', 'Etsy\'s Pick', 'Free Shipping', 'Reviews', 'Rating']])

# Visualization
hist(df, "Histogram of the number of reviews")
bar(df)
scatter(df)

hist(rec_df, "Histogram of the number of reviews of recommendation products")