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
    for l in final_links:
        print(l)
    return final_links

hundred_link_grabber("https://www.goodreads.com/list/show/1.Best_Books_Ever?page=1")
#############################################################################
## Functions for getting data from all books
def get_author(page_url):
    request = requests.get(page_url)
    page_soup = BeautifulSoup(request.content, 'html.parser')
    author = page_soup.find('a', class_="authorName").get_text().strip()
    ## Returns the author from the page
    return author

def get_title(page_url):
    request = requests.get(page_url)
    page_soup = BeautifulSoup(request.content, 'html.parser')
    title = page_soup.find('h1', id="bookTitle").get_text().strip()
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
    first_published_unclean = details_section.find("nobr", class_="greyText")
    if first_published_unclean != None:
        text = first_published_unclean.get_text()
        first_published = int(text.strip()[-6:-1])
    else:
        return None
    return first_published

def get_is_series(page_url):
    request = requests.get(page_url)
    page_soup = BeautifulSoup(request.content, 'html.parser')
    series_section = page_soup.find('h2', id="bookSeries")
    if series_section!= None:
        section_text = series_section.find('a').get_text()
        if "#" in section_text:
            return True
        else:
            return False
    else:
        return np.nan

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

def get_place(page_url):
    request=requests.get(page_url)
    page_soup=BeautifulSoup(request.content,'html.parser')
    get_place=page_soup.select('a[href*="/places"]')
    place=[]
    for x in get_place:
        place.append(x.get_text())
    return ", ".join(place)

def get_number_of_ratings(page_url):
    request = requests.get(page_url)
    page_soup = BeautifulSoup(request.content, 'html.parser')
    number_of_ratings_unclean = page_soup.find('meta', itemprop="ratingCount")
    number_of_ratings = int(number_of_ratings_unclean['content'])
    return number_of_ratings

def get_all_books(list_of_urls):
    pd_data =[]
    for book_url in list_of_urls:
        url = book_url
        title = get_title(book_url)
        author = get_author(book_url)
        num_reviews = get_num_reviews(book_url)
        num_ratings = get_number_of_ratings(book_url)
        avg_rating = get_average_rating()
        num_pages = get_number_of_pages(book_url)
        original_publish_year = get_first_published(book_url)
        series = get_is_series(book_url)
        genres = get_genres(book_url)
        awards = get_awards(book_url)
        place = get_place(book_url)
        a_book = {
            "url": url,
            "title":title,
            "author" :author,
            "num_reviews" : num_ratings,
            "num_ratings" : num_ratings,
            "num_pages" : num_pages,
            "original_publish_year" : original_publish_year,
            "series" :series,
            "genres" : genres,
            "awards" : awards,
            "place" : place}
        pd_data.append(a_book)
    return pd_data

# def main_app():
#     list_of_urls = hundred_link_grabber("https://www.goodreads.com/list/show/1.Best_Books_Ever?page=1")
#     get_book_data = get_all_books(list_of_urls)
#     return get_book_data
#
#
# x = main_app()
#
# print(len(x))
# #
# for book in x:
#     print(book)
