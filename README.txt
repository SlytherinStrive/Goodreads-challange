    :__________________________________________________________________________________:
    :     ---_ ......._-_--.      :                                                    :
    :    (|\ /      / /| \  \     :      ____  _       _   _   A product by_TEAM...    :
    :    /  /     .'  -=-'   `.   :     / ___|| |_   _| |_| |__   ___ _ __(_)_ __      :
    :   /  /    .'             )  :     \___ \| | | | | __| '_ \ / _ \ '__| | '_ \     :
    : _/  /   .'        _.)   /   :      ___) | | |_| | |_| | | |  __/ |  | | | | |    :
    :/ o   o        _.-' /  .'    :  .. |____/|_|\__, |\__|_| |_|\___|_|  |_|_| |_|    :
    :\          _.-'    / .'*|    :              |___/                                 :
    :\______.-'//    .'.' \*|     :__Slytherin will help you on your way to greatness__:
    : \|  \ | //   .'.' _ |*|     :          [x] Data Acquisition specialists**        :
    :  `   \|//  .'.'_ _ _|*|     :              ** an any means necessary approach.   :
    :   .  .// .'.' | _ _ \*|     :              ** we get the data you need.          :
    :   \`-|\_/ /    \ _ _ \*\    :   [x] Expert Analysis made simple **               :
    :    `/'\__/      \ _ _ \*\   :       ** yeah our graphs look ******* awesome.     :
    :    /^|            \ _ _ \*  :       ** and we bring the hard facts too.          :
    :    '  `             \ _ _ \ : [x] See everything at                              :
    :                      \_     :    **https://https://github.com/SlytherinStrive    :
    :__________________________________________________________________________________

                  GOOD-READS GREATEST BOOKS DATA SCRAPER & ANALYSIS
                  -------------------------------------------------

The key motivation of this project was to answer a single question;
    -What really makes the greatest books of all time?

In doing so we created tools that have the potential to perform data analysis to confirm
or deny a multitude of hypothesis of what identifies a greatest book of all time.

Key components:
  For acquiring the necessary data: data_scraper.py
  For adding additional useful data-points: data_preprocessor.py
  For analysis & creating data visualizations: data_analyzer.py

Helper components:
  For restructuring CSV's and Python dictionaries: data_restructuring.py

A note about contribution:
  This is an open source project, if you wish to contribute view the contributions section at
  the end of this README. Throughout the README if you see a (*#*) notation there is a plan in place
  for future development by our team or a chance for you to add a meaningful contribution.


                HOW TO USE GOOD-READS GREATEST BOOKS DATA SCRAPER & ANALYSIS
                ------------------------------------------------------------

data_scraper.py
---------------
  INPUT: Command line interface
  OUTPUT : a CSV of book data;
      # Header                # Expected type   # What the data should look like
      url:                    type= string,     description= the url where the data came from
      book_id:                type= integer,    description= goodreads book identifying number
      title:                  type= string,     description= the title of the book
      award_count:            type= integer,    description= the count of awards the book has
      author:                 type= string,     description= the author of the book
      avg_rating:             type= float,      description= the average rating of the book
      num_reviews:            type= float,      description= the number of reviews the book has
      num_ratings:            type= float,      description= the number of ratings the books has
      num_pages:              type= float,      description= the number of pages in the book
      original_publish_year:  type= integer,    description= the orginal publishing date of the book
      series:                 type= boolean,    description= whether the book is part of series
      genres:                 type= string,     description= relevant genres of the book separated by commas
      awards:                 type= string,     description= a string of awards separated by commas
      place:                  type= string,     description= a comma separated list of locations in the book


  What does it do?
  ----------------
  It scrapes links to books, it then runs a second scrape on all of these individual books urls to get
  the book data listed in OUTPUT above.


  About the data source
    Data source: https://www.goodreads.com/
    Specific url: https://www.goodreads.com/list/show/1.Best_Books_Ever?page=1
    Example book page: https://www.goodreads.com/book/show/2767052-the-hunger-games


    This scraper is designed to work with the specified "Data source". To answer the question
    that motivated us to create this project it works on the example "Specific url". A user can edit
    this in the scraper to get data on any list at provided at the Data source. This is done by editing
    the data_scraper.py file variable "URL_SETTING":

    ABOUT: URL_SETTING = "https://www.goodreads.com/list/show/1.Best_Books_Ever?page=1"
      If you wish to scrape other lists you may change the URL_SETTING. It runs on lists of books that
      have a 'pagination' style. a valid url will end with "?page=i" where 'i' is the pagination number.(*1*)

    ABOUT: command_line_interface() (*2*)
      This function prompts the user to specify how much data they wish to scrape. The first question
      is a yes/no question asking if they want to scrape a range of book lists. Answering no defaults
      the scraper to search from a single list of 100 books where they can enter the specific pagination
      number they wish to scrape.
              [** INSERT IMAGE HERE **]

      If the user answers yes then they will be prompted to enter 2 numbers, the pagination number to start
      the scrape on and the pagination number to end it on.
              E.g. selecting '1' and '10' will scrape 10 lists of 100 books each.
              [** INSERT IMAGE HERE **]

    ABOUT: Command Line Interface Terminal messages
      The first process of the scraper is to collect individual book links (see ABOUT: hundred_link_grabber()).
      As this function runs it will confirm that it has received the quantity of links it was looking for.

      The second process of the scraper is to check individual books. If data is missing it will notify you in
      the terminal. Missing series, award & places data is expected. If other fields are commonly missing the
      web page has been restructured or the link you are using is incorrect. Please send us a message on github
      if you are using the original URL_SETTING and large amounts of data cannot be found.


    ABOUT: main_scraper(start_range, end_range=None)
      This is the main controller of the program. You can remove the command line interface(*) and run this
      instead however it will not output to CSV or save your data. It starts by creating a list of urls
      (see hundred_link_grabber()) and then passes them into
      INPUT:
        start_range: Is a mandatory int input: it will run a single book list pagination if end_range=None.
        end_range:   If an end range is entered it will get books lists from the start_range to end_range integers and
                     the pagination's in between.
      OUTPUT:
        python_list containing python dictionaries of book data, see example pseudo code below
        [{csv_headers:book_data}, {csv_headers:book_data}, {csv_headers:book_data}, {csv_headers:book_data}]

      (*) the command line interface automatically passes the output of main_scraper into a dictionary merger and then
      creates a CSV from the merged dictionaries (see data_restructuring merge_data_dicts())

    ABOUT: hundred_link_grabber(pagination_url):
        This function takes a single url and gets the html with requests. It then creates a BeautifulSoup(!) object and searches
        it for urls linking directly to books.
      INPUT: string; must be a complete url that goes to a page containing a list of books.
      OUPUT: list; a list of strings that are urls to individual book pages

    ABOUT: get_all_books(list_of_urls)
      This function gets scrapes data from a book page. It is mainly to be seen as a controller of the several 'get_data()'
      functions but handles a list of pages processing them individually. For each URL it will make a request for the html
      and turn it into a BeautifulSoup object(!). The Soup object is then passed into each get_data() function.(*3*)
      INPUT:
        list_of_urls: this will be a python list containing urls. This is generally generated by the main_scraper() functions
                use of the hundred_link_grabber().
      OUTPUT:
        python_list containing python dictionaries of book data, see example  pseudo code below
              [{csv_headers:book_data}, {csv_headers:book_data}, {csv_headers:book_data}, {csv_headers:book_data}]


















How to use: data_preprocessor.py

How to use: data_scraper.py
