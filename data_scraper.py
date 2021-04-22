import numpy as np
import pandas as pd
import argparse as ap
from slytherin import logo_printer
from bs4 import BeautifulSoup
import concurrent.futures
import requests
from data_restructuring import merge_data_dicts
from data_preprocessing import *
import time



###############################################################################################
###############################################################################################
### GLOBAL SCRAPER STORAGE AND SETTINGS
book_list_dict = {1: ("Best books ever (*)", "https://www.goodreads.com/list/show/1.Best_Books_Ever?page=1"),
                2: ("Books everyone should read atleast once", "https://www.goodreads.com/list/show/264.Books_That_Everyone_Should_Read_At_Least_Once?page=1"),
                3: ("Books that should be made into movies", "https://www.goodreads.com/list/show/1043.Books_That_Should_Be_Made_Into_Movies?page=1"),
                4: ("Best books of the 20th century", "https://www.goodreads.com/list/show/6.Best_Books_of_the_20th_Century?page=1")}


data_setting_dict = {1: ["\nWould you like us to preprocess the books adding addtional data?",  True]}
URL_SETTING = ("Best books ever (*Used for our analysis)", "https://www.goodreads.com/list/show/1.Best_Books_Ever?page=1")
quantity_setting_dict = {"Quantity": None,
                        "Instances": None}

NEW_FILE_NAME = ""
###############################################################################################
###############################################################################################
### SPECIFIC BOOK DETAIL SCRAPING FUNCTIONS
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

###############################################################################################
###############################################################################################
### FUNCTIONS FOR MULTIPLE BOOK SCRAPING
def get_all_books(list_of_urls):
    pd_data =[]
    run_total = len(list_of_urls)
    for i, book_url in enumerate(list_of_urls):
        print(f"Working on url: {book_url}.. {i}/{run_total}")
        request = requests.get(book_url[0])
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
            "url": [book_url[0]],
            "book_id":[book_id],
            "title":[title],
            "author" :[author],
            "good_read_score": [book_url[1]],
            "good_read_votes": [book_url[2]],
            "avg_rating": [avg_rating],
            "num_reviews" : [num_reviews],
            "num_ratings" : [num_ratings],
            "num_pages" : [num_pages],
            "original_publish_year" : [original_publish_year],
            "series" :[series],
            "genres" : [genres],
            "awards" : [awards],
            "award_count": [award_count],
            "place" : [place]}
        print(f"Succesully gathered: {title} from URL: {book_url}")
        pd_data.append(a_book)
        print(a_book)
    return pd_data

def hundred_link_grabber(pagination_url):
    page = requests.get(url=pagination_url)
    soup = BeautifulSoup(page.content, 'html.parser')
    links_section = soup.find_all('a', class_="bookTitle", href=True)
    final_links = ["https://www.goodreads.com" + link['href'] for link in links_section]
    score_divs = soup.find_all('div', style="margin-top: 5px")
    final_scores = []
    good_read_score = np.nan
    score_votes = np.nan
    for book in score_divs:
        a_s =  book.find_all('a')
        a_s_text = [a.get_text() for a in a_s ]
        a_s_int = [int("".join([i for i in g if i.isnumeric()])) for g in a_s_text]
        final_scores.append(a_s_int)

    all_pagi_data =[]
    for link, scores in zip(final_links, final_scores):
        all_pagi_data.append((link, scores[0], scores[1]))

    len_links = len(all_pagi_data)
    return all_pagi_data

def range_scraper(start_range, end_range):
    """
    quantity is sets of 100 books
    """
    all_urls = []

    for i in range(start_range, end_range+1):
        #print(f"Attempting to take 100 links. Iteration: {i}/{end_range} - awaiting success confirmation")
        list_url = URL_SETTING[1][:-1]+str(i)
        get_url_data = hundred_link_grabber(list_url)
        all_urls.extend(get_url_data)
        #print(f"***FAILED*** to take links on iteration {i}")

        #print("Failed")
    total_urls = len(all_urls)
    #print(f"Finished geneating pagigination urls. total count is {total_urls} urls")
    get_book_data = get_all_books(all_urls)
    return get_book_data

def genre_column_maker(dataframe):
    df = dataframe
    ## Splits all genres into different columns
    x =df.genres.str.split(',', expand=True)

    y=len(x.columns)

    df[[f"genre_{i}" for i in range(0,y)]] = df.genres.str.split(',', expand=True)

    ### Returns a dataframe that has booleans for whether data is duplicated across columns
    is_duplicate = df[[f"genre_{i}" for i in range(0,y)]].apply(pd.Series.duplicated, axis=1).reset_index()

    ## Takes the current dataframe and where the 'is_duplicate' dataframe has True values, it replaces them with np.nan
    df[[f"genre_{i}" for i in range(0,y)]] = df[[f"genre_{i}" for i in range(0,y)]].where(~is_duplicate, np.nan).fillna('zzzyyyy')

    # A way to change nan values to another value
    for i in range(y):
        df[f"genre_{i}"] = df[f"genre_{i}"].str.strip()

    ################################################################################
    # Find the most common genres
    ################################################################################

    ## Returns 2 numpy arrays of the unique values and there counts
    unique, counts  = np.unique(df[[f"genre_{i}" for i in range(0,y)]].values, return_counts=True)

    ##zips the 2 arrays into a dictionary of "Genre": int (Count)
    d = dict(zip(unique, counts))
    # Creates a new dataframe from the dictionary with the counts as a column and the genre as the index
    genre_df = pd.DataFrame.from_dict(d, orient='index',columns=['count'])
    genre_df.drop(['zzzyyyy'], inplace=True)
    order_genre = genre_df.sort_values('count', ascending=False)
    top_50_genres = order_genre.head(50)
    genre_names = list(top_50_genres.index)
    #################################################################################
    # Make columns with genre names and map true or false if book contains that genre
    #################################################################################

    for genre in genre_names:
        df[genre] = df['genres'].str.contains(genre)
        #df[genre] = df[genre].map({True: 'Yes', False: 'No'})

    df.drop([f"genre_{i}" for i in range(0,y)], inplace=True, axis=1)

    print(df.info())

    return df

###############################################################################################
###############################################################################################
### COMMAND LINE INTERFACE FUNCTIONS

def start_menu():
    logo_printer()
    print("Welcome to the good reads book data scraper")
    print("What type of book are you interested in gathering data on? \n")
    for k, v in book_list_dict.items():
        print(f"{k}: {v[0]}")
    type_pick = None
    while type_pick == None:
        ui = input("\n Enter the number of the list you wish to scrape >> ")
        try:
            if int(ui) in book_list_dict.keys():
                type_pick = int(ui)
        except:
            print("Invalid option - try again")
    global URL_SETTING
    URL_SETTING = book_list_dict[type_pick]
    global NEW_FILE_NAME
    NEW_FILE_NAME += "".join([c for c in book_list_dict[type_pick][0] if c.isalnum()])
    return data_settings()

def data_settings():
    print("\n**************************************************")
    print(" DATA TYPE SETTINGS")
    print("**************************************************\n")
    print(f"Before you begin collecting book data on: {URL_SETTING[0]}")
    print("Please provide your data settings by anwswering the following questions: \n")

    for key, value in data_setting_dict.items():
        setting_pick = None
        while setting_pick == None:
            print(value[0])
            ui = input("\n Enter 'y' for Yes or 'n' for No >> ")
            try:
                if ui.lower() == "y":
                    setting_pick = True
                elif ui.lower() == "n":
                    setting_pick = False
                else:
                    print("Invalid option - try again")
            except:
                print("Invalid option - try again")
        data_setting_dict[key] = [value[0], setting_pick]

    print("Thanks for confirming the settings ")
    return quantity_setter()

def quantity_setter():
    print("\n**************************************************")
    print(" BOOK QUANTIY SETTINGS")
    print("**************************************************\n")
    print(f"We detect you can gather information on upto 10,000 books with the '{URL_SETTING[0]}' list.")
    print("You can scrape in multiples of 100. Please select how many books you would like to get data on.")
    print("Please note you must select a multiple of 100 e.g. 500, 600 700... 9000, 9900, 10000")
    print("\n How many would you like to get?")

    quantity_pick = None
    scraper_instance_pick = None

    while quantity_pick == None:
        ui = input("\n Enter the number of books from 100 to 10000 >> ")
        try:
            if int(ui)%100 == 0:
                if int(ui) >= 100 and int(ui) <=10000:
                    quantity_pick = int(ui)
                else:
                    print("Invalid quanity, try again")
            else:
                print("Invalid quanity, try again")
        except:
            print("xInvalid quantity - try again")
    print("\n Please select the maximum instances of the scraper you wish to run.")
    print("The more you run the faster data will acquire. A maximum of 20 can be entered.")
    print("The higher the chosen quantity of scrapers the greater decrease in system performance.")
    print("There is also a possibility that the host website may prevent you from making too many requests.")
    max_scrapers = quantity_pick // 100
    while scraper_instance_pick == None:
        ui = input(f"\n Enter the quantiy of scrapers to run (min:1, max:{max_scrapers}) >> ")
        try:
            if int(ui) >=1 and int(ui)<=max_scrapers:
                scraper_instance_pick = int(ui)
            else:
                print("Invalid quantity, try again")
        except:
            print("Invalid quantity - try again")

    quantity_setting_dict["Quantity"] = quantity_pick
    quantity_setting_dict["Instances"] = scraper_instance_pick
    global NEW_FILE_NAME
    NEW_FILE_NAME += "_"+str(quantity_pick)+"_"+str(scraper_instance_pick)

    return begin_scraper()

def begin_scraper():
    scrape_start = time.perf_counter()
    pagination_total = int(quantity_setting_dict['Quantity'] / 100)
    scraper_total = quantity_setting_dict['Instances']
    pages_per_process = []
    processes = []
    if scraper_total > 1:
        if pagination_total % scraper_total == 0:
            split = int(pagination_total / scraper_total)

            pages_per_process = [(i, i+split-1) for i in range(1, pagination_total, split)]

        else:
            split = int(pagination_total // scraper_total)
            remainder = int(pagination_total % scraper_total)
            pages_per_process = [(i, i+split-1) for i in range(1, pagination_total-remainder, split)]
            pages_per_process[-1] = (pages_per_process[-1][0], pagination_total)

    with concurrent.futures.ProcessPoolExecutor() as executor:
        scraper_future_results = [executor.submit(range_scraper,process[0], process[1]) for process in pages_per_process]

    all_scraper_results =[]

    for scraper in scraper_future_results:
        all_scraper_results.extend(scraper.result())


    # backup split data

    # preprocessing
    scrape_end = time.perf_counter()
    print(f"You collected all the data in  {round(scrape_end-scrape_start, 2)}")
    return run_preprocessor(all_scraper_results)


def run_preprocessor(results):
    if data_setting_dict[1][1] == True:
        all_books = merge_data_dicts(results)
        df = pd.DataFrame(all_books)
        df = genre_column_maker(df)
        df.to_csv(f"data/{NEW_FILE_NAME}_no_pp.csv")
        df = preprocessing(f"data/{NEW_FILE_NAME}_no_pp.csv")
        df.to_csv(f"data/{NEW_FILE_NAME}_with_pp.csv")
        print(f"Thankyou succesfully sraped and saved to data/{NEW_FILE_NAME}_with_pp.csv")
    else:
        all_books = merge_data_dicts(results)
        df = pd.DataFrame(all_books)
        df.to_csv(f"data/{NEW_FILE_NAME}_no_pp.csv")
        print(f"Thankyou succesfully sraped and saved to data/{NEW_FILE_NAME}_no_pp.csv")
    print("Closing scraper")


if __name__ == "__main__":
    start_menu()
