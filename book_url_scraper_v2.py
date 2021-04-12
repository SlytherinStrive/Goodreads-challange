#importing the main libraries

import requests
import pandas as pd
from bs4 import BeautifulSoup
import numpy as np

#############################################################################
## Get links from the list of books
def hundred_link_grabber(all_books_url):
    page = requests.get(url=all_books_url)
    soup = BeautifulSoup(page.content, 'html.parser')
    links_section = soup.find_all('a', class_="bookTitle", href=True)
    final_links = ["https://www.goodreads.com" + link['href'] for link in links_section]
    len_links = len(final_links)
    print(f"Succesfully generated {len_links}")
    return final_links


#############################################################################
## Functions for getting data from all books

## Function to get the author
def get_author(page_soup):
    try:
        author = page_soup.find('a', class_="authorName").get_text().strip()
        ## Returns the author from the page
        return author
    except:
        print("Oh no get_author failed")
        return np.nan

## Function to get the book title
def get_title(page_soup):
    try:
        title = page_soup.find('h1', id="bookTitle").get_text().strip()
        return title
    except:
        print("Oh no get_title failed")
        return np.nan

def get_number_of_pages(page_soup):
    # Missing data probelem
    try:
        number_of_pages_unclean = page_soup.find('span', itemprop="numberOfPages").get_text()
        number_of_pages = int("".join([char for char in number_of_pages_unclean if char.isnumeric()]))
        return number_of_pages
    except:
        print("Oh no get_number_of_pages failed")
        return np.nan

# Number of ratings
def get_number_of_ratings(page_soup):
    try:
        number_of_ratings_unclean = page_soup.find('meta', itemprop="ratingCount")
        number_of_ratings = int(number_of_ratings_unclean['content'])
        return number_of_ratings
    except:
        print("Oh no get_number_of_ratings failed")
        return np.nan

# First publication year
def get_first_published(page_soup):
    try:
        details_section = page_soup.find('div', id="details")
        first_published_unclean = details_section.find("nobr", class_="greyText")
        if first_published_unclean != None:
            text = first_published_unclean.get_text()
            first_published = int(text.strip()[-6:-1])
        else:
            return None
        return first_published
    except:
        print("Oh no get_first_published failed")
        return np.nan

# Is the book is part of series (True/False)
def get_is_series(page_soup):
    try:
        series_section = page_soup.find('h2', id="bookSeries")
        section_text = series_section.find('a')
        if series_section != None:
            check_if_series = series_section.find('a').get_text()
            if "#" in check_if_series:
                return True
            else:
                return False
        else:
            return np.nan
    except:
        print("Oh no get_is_series failed")
        return np.nan

# List of awards recieved
def get_awards(page_soup):
    try:
        awards_section = page_soup.find('div', itemprop="awards")
        awards = awards_section.find_all('a', class_="award")
        main_awards = [award.get_text().strip() for award in awards]
        str_main_awards = ", ".join(main_awards)
        return str_main_awards
    except:
        print("Oh no get_awards failed")
        return np.nan

# Genre of the book
def get_genres(page_soup):
    try:
        genre_list_unclean = page_soup.find_all('a', class_="actionLinkLite bookPageGenreLink")
        genre_list = [genre.get_text() for genre in genre_list_unclean]
        str_genre_list = ", ".join(genre_list)
        return str_genre_list
    except:
        print("Oh no get_genres failed")
        return np.nan

# Place (Setting)
def get_place(page_soup):
    try:
        get_place=page_soup.select('a[href*="/places"]')
        place=[]
        for x in get_place:
            place.append(x.get_text())
        return ", ".join(place)
    except:
        print("Oh no get_place failed")
        return np.nan

# Getting number of reviews
def get_num_reviews(page_soup):
    try:
        get_num_unclean=page_soup.find('meta',itemprop="reviewCount")
        get_num_reviews=int(get_num_unclean['content'])
        return get_num_reviews
    except:
        print("Oh no get_num_reviews failed")
        return np.nan

#Getting average score
def get_avg(page_soup):
    try:
        get_avg=float(page_soup.find('span',itemprop="ratingValue").get_text())
        return get_avg
    except:
        print("Oh no get avg failed")
        return np.nan

# Creation of the dictionary
def get_all_books(list_of_urls):
    pd_data =[]
    for book_url in list_of_urls:
        print(f"Working on url: {book_url}")
        request = requests.get(book_url)
        page_soup = BeautifulSoup(request.content,'html.parser')
        title = get_title(page_soup)
        author = get_author(page_soup)
        num_reviews = get_num_reviews(page_soup)
        num_ratings = get_number_of_ratings(page_soup)
        avg_rating = get_avg(page_soup)
        num_pages = get_number_of_pages(page_soup)
        original_publish_year = get_first_published(page_soup)
        series = get_is_series(page_soup)
        genres = get_genres(page_soup)
        awards = get_awards(page_soup)
        place = get_place(page_soup)
        a_book = {
            "url": [book_url],
            "title":[title],
            "author" :[author],
            "avg_rating": [avg_rating],
            "num_reviews" : [num_ratings],
            "num_ratings" : [num_ratings],
            "num_pages" : [num_pages],
            "original_publish_year" : [original_publish_year],
            "series" :[series],
            "genres" : [genres],
            "awards" : [awards],
            "place" : [place]}
        pd_data.append(a_book)
    return pd_data

#############################################################################
## Functions for getting all data
def main_app(quantity):
    """
    quantity is sets of 100 books
    """
    all_urls =[]
    if quantity < 55:
        for i in range(quantity):
            try:
                print(f"Attempting to take 100 links. Iteration: {i} - awaiting success confirmation")
                list_url = f"https://www.goodreads.com/list/show/1.Best_Books_Ever?page={i}"
                get_url_data = hundred_link_grabber(list_url)
                all_urls.append(get_url_data)
            except:
                print(f"***FAILED*** to take links on iteration {i}")

    else:
        return "Selected too many books"
    total_urls = len(all_urls)
    print(f"Finished geneating pagigination urls. total count is {total_urls} urls")
    get_book_data = get_all_books(all_urls)
    return get_book_data

# Debugger function
def debugger_help(book_url):
    request = requests.get(book_url)
    page_soup = BeautifulSoup(request.content,'html.parser')
    return page_soup

# Used for merging all the book dictionaries into one for easy dataframe creation
def merge_data_dicts(list_of_dictionaries):
    all_data = {}
    for dict in list_of_dictionaries:
        for key, value in dict.items():
            if key in all_data.keys():
                current_data = all_data[key]
                combined_data = current_data + value
                all_data[key] = combined_data
            else:
                all_data[key] = value
    return all_data


books = main_app(40)
df = pd.DataFrame(merge_data_dicts(books))

df.to_csv('scraped_alot_of_movies.csv', index = False, header=True)



# merge_books = merge_data_dicts(books)
#
# df = pd.DataFrame(merge_books)
