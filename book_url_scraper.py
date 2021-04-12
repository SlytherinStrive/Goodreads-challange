import requests
import pandas as pd
from bs4 import BeautifulSoup
import numpy as np


##### Get links from the list of books
def hundred_link_grabber(all_books_url):
    page = requests.get(url=all_books_url)
    soup = BeautifulSoup(page.content, 'html.parser')
    links_section = soup.find_all('a', class_="bookTitle", href=True)
    final_links = ["https://www.goodreads.com" + link['href'] for link in links_section]
    ## Returns a list of 100 book links
    return final_links


#############################################################################
## Functions for getting data from all books
def get_author(page_url):
    request = requests.get(page_url)
    page_soup = BeautifulSoup(request.content, 'html.parser')
    author = page_soup.find('a', class_="authorName").get_text()
    ## Returns the author from the page
    return author

def get_title(page_url):
    request = requests.get(page_url)
    page_soup = BeautifulSoup(request.content, 'html.parser')
    title = page_soup.find('h1', id="bookTitle").get_text()
    return title

def get_number_of_pages(page_url):
    request = requests.get(page_url)
    page_soup = BeautifulSoup(request.content, 'html.parser')
    number_of_pages_unclean = page_soup.find('span', itemprop="numberOfPages").get_text()
    number_of_pages = int("".join([char for char in number_of_pages_unclean if char.isnumeric()]))
    return number_of_pages

def get_number_of_ratings(page_url):
    request = requests.get(page_url)
    page_soup = BeautifulSoup(request.content, 'html.parser')
    number_of_ratings_unclean = page_soup.find('meta', itemprop="ratingCount")
    number_of_ratings = int(number_of_ratings_unclean['content'])
    return number_of_ratings

def get_first_published(page_url):
    request = requests.get(page_url)
    page_soup = BeautifulSoup(request.content, 'html.parser')
    details_section = page_soup.find('div', id="details")
    first_published_unclean = details_section.find("nobr", class_="greyText").get_text()
    first_published = int(first_published_unclean.strip()[-6:-1])
    return first_published

def get_is_series(page_url):
    request = requests.get(page_url)
    page_soup = BeautifulSoup(request.content, 'html.parser')
    series_section = page_soup.find('h2', id="bookSeries")
    section_text = series_section.find('a').get_text()
    if "#" in section_text:
        return True
    else:
        return False

def get_awards(page_url):
    request = requests.get(page_url)
    page_soup = BeautifulSoup(request.content, 'html.parser')
    awards_section = page_soup.find('div', itemprop="awards")
    awards = awards_section.find_all('a', class_="award")
    main_awards = [award.get_text().strip() for award in awards]
    str_main_awards = ", ".join(main_awards)
    return str_main_awards

def get_genres(page_url):
    request = requests.get(page_url)
    page_soup = BeautifulSoup(request.content, 'html.parser')
    genre_list_unclean = page_soup.find_all('a', class_="actionLinkLite bookPageGenreLink")
    genre_list = [genre.get_text() for genre in genre_list_unclean]
    str_genre_list = ", ".join(genre_list)
    return str_genre_list





x = get_genres("https://www.goodreads.com/book/show/2657.To_Kill_a_Mockingbird")
print(x)
