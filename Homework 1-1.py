import csv
import requests
from bs4 import BeautifulSoup


# Function to scrape a dinary data
def binary_data(item, tag, class_val, value):
    element = item.find(tag, {'class': class_val})
    value = 'Y' if element and value in element.text else 'N'

    return value


# Function to scrape a rating 
def rating_data(item):
    rating = 'No rating'
    rating_element = item.find('div', {'class': ['sprite-img black-stars', 'stars-larger']})
    if (rating_element != None):
        rating = rating_element.get('aria-label').replace(' out of 5 stars', '')
        
    return rating


# Function to extract data from a single page
def extract_data(soup):
    items = soup.find_all('div', {'class': 'v2-listing-card__info'})
    data = []

    for item in items:

        # item name
        name_element = item.find('h3', {'class': ['wt-text-caption', 'v2-listing-card__title', 'wt-text-truncate']})
        name = name_element.get_text(strip=True) if name_element else 'No Title'
        
        # original_price_element = item.find('span', {'class': 'strike-through'})

        # price
        price_element = item.find('span', {'class': 'currency-value'})
        price = price_element.text.strip().replace(',', '') if price_element else 'No price'
    
        # star seller
        star_seller = binary_data(item, 'p', 'wt-text-caption-title wt-nudge-l-2 star-seller-badge-lavender-text-light', 'Star Seller')
            
        # free shipping
        free_shipping = binary_data(item, 'span', 'wt-badge wt-badge--small wt-badge--statusValue', 'FREE shipping')

        # esty's pick
        estys_pick = binary_data(item, 'span', 'wt-badge wt-badge--statusRecommendation wt-badge--small wt-mb-xs-1', 'Etsy’s Pick')

        # review count
        review_count_element = item.find('span', {'class': 'wt-text-caption wt-text-gray wt-display-inline-block wt-nudge-l-3 wt-pr-xs-1'})
        review_count = review_count_element.text.strip().replace('(', '').replace(')', '').replace(',', '') if review_count_element else 'No reviews'
            
        # rating
        rate = rating_data(item)

        data.append([name, price, star_seller, estys_pick, free_shipping, review_count, rate])

    return data
    

# Main function to scrape data
def scrape_etsy(url, pages):
    all_data = []
    for page in range(1, pages + 1):
        print(f'Scraping page {page}')
        response = requests.get(url + f'{page}')
        soup = BeautifulSoup(response.content, 'html.parser')
        page_data = extract_data(soup)
        all_data.extend(page_data)
    return all_data


# Scraping data
url = 'https://www.etsy.com/c/pet-supplies?ref=pagination&page='
page_num = 100

data = scrape_etsy(url, page_num)


# Save data to CSV
with open('PetSupplies.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Product Name', 'Price', 'Star Seller', 'Etsy\'s Pick', 'Free Shipping', 'Reviews', 'Rating'])
    writer.writerows(data)

print('\nComplete')