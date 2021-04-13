# importing the main libraries
import requests
import pandas as pd
from bs4 import BeautifulSoup
import numpy as np
from logo import logo_printer

#############################################################################
## Functions for getting column data from a book webpage
"""
The following book data functions take the format:

input : page_soup - a BeautifulSoup object generated from a url of a book page

output: i)  str, int, float, boolean - a perfectly selected piece of data
        ii) np.nan - a missing piece of data
"""
def get_book_id(page_soup):
    try:
        book_id_section = page_soup.find('div', class_="asyncPreviewButtonContainer")
        book_id = book_id_section['data-book-id']
        ## Returns the author from the page
        return book_id
    except:
        print("Oh no get_book_id failed")
        return np.nan

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
        text = first_published_unclean.get_text()
        first_published = int(text.strip()[-6:-1])
        return first_published
    except:
        print("Oh no first attempt to get_first_published failed, trying route 2")
        try:
            # this handles a poorly formatted page option where the published year is not first found
            details_section = page_soup.find('div', id="details")
            first_published_unclean = details_section.find_all('div', class_="row")
            specifc_row = [divrow.get_text() for divrow in first_published_unclean if 'ublished' in divrow.get_text()][0].replace("\n"," ")
            split_row = specifc_row.split(" ")
            find_date = [element for element in split_row if element.isnumeric()][0]
            return int(find_date)
        except:
            print("Second get_first_published failed, giving nan value")
            return np.nan

# Is the book is part of series (True/False)
def get_is_series(page_soup):
    try:
        series_section = page_soup.find('h2', id="bookSeries")
        is_series = series_section.find('a').get_text()
        if "#" in is_series:
            return True
        else:
            return False
    except:
        print("Get series had no data- assuming False")
        return False

# List of awards recieved
def get_awards(page_soup):
    try:
        awards_section = page_soup.find('div', itemprop="awards")
        awards = awards_section.find_all('a', class_="award")
        main_awards = [award.get_text().strip() for award in awards]
        str_main_awards = ", ".join(main_awards)
        return str_main_awards

    except:
        print("Oh no get_awards failed- assuming 0 awards")
        return np.nan

## Get count of awards
def get_awards_count(page_soup):
    try:
        awards_section = page_soup.find('div', itemprop="awards")
        awards = awards_section.find_all('a', class_="award")
        main_awards = [award.get_text().strip() for award in awards]
        str_main_awards =len((", ".join(main_awards)).split(',')) #len(main_awards)
        print(str_main_awards)
        return str_main_awards
    except:
        print("Oh no get_awards_count failed - assuming 0")
        return 0


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
        place = []
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


#############################################################################
## Get links from the list of books
"""
[Scraping Stage 2 = Hundred link grabber]
input : list - containing a list of books from https://www.goodreads.com

output: list - containing the 100 books found on that page
"""
def hundred_link_grabber(all_books_url):
    page = requests.get(url=all_books_url)
    soup = BeautifulSoup(page.content, 'html.parser')
    links_section = soup.find_all('a', class_="bookTitle", href=True)
    final_links = ["https://www.goodreads.com" + link['href'] for link in links_section]
    len_links = len(final_links)
    print(f"Succesfully generated {len_links}")
    return final_links


#############################################################################
## Get data from individual book pages
"""
[Scraping Stage 3 = Get_all_books_data]
input : str - a url that is a page on from https://www.goodreads.com that contains a list of books

output: list - containing dictionaries with the books data from each url inputted

"""
def get_all_books(list_of_urls):
    pd_data =[]
    run_total = len(list_of_urls)
    for i, book_url in enumerate(list_of_urls[0:2]):
        print(f"Working on url: {book_url}.. {i}/{run_total}")
        request = requests.get(book_url)
        page_soup = BeautifulSoup(request.content,'html.parser')
        book_id = get_book_id(page_soup)
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
        award_count = get_awards_count(page_soup)
        place = get_place(page_soup)
        a_book = {
            "url": [book_url],
            "book_id":[book_id],
            "title":[title],
            "award_count": [award_count],
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
## Generates the intital links for lists of books
"""
[Scraping STAGE 1 = main_scraper]
args  : start_range - an int between 1-99
                    the page number you wish to scrape 1-99

kwargs: end_range - defaults to None
                    if an int is entered between 2-101
                    the start_range becomes the start of a range
                    and the end_range becomes the end of the range

output: list - containing dictionaries with the books data from each url inputted

Scraping stages...
This runs the other 2 functions in order
firstly grabs the amount of links as specificed by the inputs
secondly grabs the data from those books

"""
def main_scraper(start_range, end_range=None):
    """
    quantity is sets of 100 books
    """
    all_urls = []
    if end_range:
        for i in range(start_range, end_range):
            try:
                print(f"Attempting to take 100 links. Iteration: {i} - awaiting success confirmation")
                list_url = f"https://www.goodreads.com/list/show/1.Best_Books_Ever?page={i}"
                get_url_data = hundred_link_grabber(list_url)
                all_urls.extend(get_url_data)
            except:
                print(f"***FAILED*** to take links on iteration {i}")
    else:
        try:
            print(f"Attempting to take 100 links. from pagination {start_range}- awaiting success confirmation")
            list_url = f"https://www.goodreads.com/list/show/1.Best_Books_Ever?page={start_range}"
            get_url_data = hundred_link_grabber(list_url)
            all_urls.extend(get_url_data)
        except:
            print(f"***FAILED*** to take links on pagination {start_range}")

    total_urls = len(all_urls)
    print(f"Finished geneating pagigination urls. total count is {total_urls} urls")
    get_book_data = get_all_books(all_urls)
    return get_book_data


#############################################################################
## Used for merging all the book dictionaries into one for easy dataframe creation
"""
args  : list_of_dictionaries - a list of dictionaries containing
                                book data.

output: dictionary - all of the dictionary values merged into lists
"""
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


#############################################################################
## THIS IS TERMINAL INTERFACE FOR SELECTING HOW MUCH TO SCRAPE
def command_line_page_enter():
    logo_printer()
    ## Check if user wishes for a single list of books (100) or a range of lists (1-100)
    check_input = None
    while check_input == None:
        print("\n     Welcome to the great reads book scraper for the best books of all time..")
        print("\n     To begin scraping please set your parameters for the quantity of books you need.")
        print("\n     Each book list contains 100 books and we can search upto 100 lists.")
        print("\n     You can scrape a specific list from 100 book lists they offer by entering the relative number.")
        print("\n     Alternatively if you need upto 10,000 books can enter a range of book list pages from 1-100")
        print("\n   Would you like to enter a range of book list pages?")
        user_input = input("\n>>> Enter 'y' for Yes or a 'n' for No:  ")

    ## Validation for two entries: Must be a "y" or "n"
        ## "y" will ask you to enter a range of book lists,
        if user_input == "y":
            start_input = None
            end_input = None

            ## Loop that runs until a valid start and end of range has been entered
            while start_input == None and end_input == None:
                start_check = input("\n>>> start of range (from 1 to 99):  ")
                end_check = input("\n>>> Enter end of range from (2 to 100):  ")

                ## Validate the start choice, making sure it is between the correct range
                if start_check.isnumeric():
                    if int(start_check) in range(1,100):
                        start_input = int(start_check)
                    else:
                        print("\nYou need to enter a start input between 1 & 99:  ")
                        start_input = None

                # Validate the end choice, making sure it is between the correct range
                if end_check.isnumeric():
                    if int(end_check) in range(2,101):
                        end_input = int(end_check)
                    else:
                        print("\nYou need to enter an end input between 2 & 100:  ")
                        end_input = None

            ## After all validations is complete, runs the scraper with the desired range of book lists
            books = main_scraper(start_input, end_input + 1)
            df = pd.DataFrame(merge_data_dicts(books))
            df.to_csv(f'data/10kscraped_range{start_input}_to_{end_input}.csv', index = False, header=True)
            break

        # if valid n is selected do the following for a single page
        elif user_input == "n":
            page_input = None
            while page_input == None:
                page_check = input("\n>>> Enter book list number (from 1 to 100):  ")
                if page_check.isnumeric():
                    if int(page_check) in range(1,101):
                        page_input= int(page_check)
                else:
                    page_input = None

            # scrape data from the single page
            books = main_app(page_input)
            df = pd.DataFrame(merge_data_dicts(books))
            df.to_csv(f'data/10kscrapedpages_{page_input}.csv', index = False, header=True)
            break
        else:
            print("\n You must enter a 'y' or a 'n' to continue")
            user_input = None



### RUNS THE CLI
if __name__ == "__main__":
    command_line_page_enter()


### Helper functions
def debugger_help(book_url):
    request = requests.get(book_url)
    page_soup = BeautifulSoup(request.content,'html.parser')
    return page_soup
