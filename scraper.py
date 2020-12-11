from bs4 import BeautifulSoup
import requests
import collections


def get_review(link):
    source = requests.get(f"https://letterboxd.com{link}").text
    soup = BeautifulSoup(source, "lxml")
    return soup.find('div', class_=['review', 'body-text']).div.div.p.text


def get_user_reviews(user):
    source = requests.get(f"https://letterboxd.com/{user}/films/reviews/").text
    soup = BeautifulSoup(source, "lxml")
    reviews = []
    for review in soup.find('ul', class_='film-details-list').find_all('li'):
        reviews.append(get_review(review.a['href']))
    return reviews


def scrawl_user_reviews(user):
    next_link = f"/{user}/films/reviews/"
    reviews = []
    while (next_link is not None):
        source = requests.get(f"https://letterboxd.com{next_link}").text
        soup = BeautifulSoup(source, "lxml")
        next = soup.find_all('div', class_='paginate-nextprev')[1]
        for review in soup.find('ul', class_='film-details-list').find_all('li'):
            reviews.append(get_review(review.a['href']))
        next_link = soup.find('a', 'next')
        if next_link is not None:
            next_link = next_link['href']
    return reviews
