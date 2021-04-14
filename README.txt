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
  INPUT  : Command line interface
  OUTPUT : a CSV of book data.
      url
      book_id
      title
      award_count,
      author,
      avg_rating,
      num_reviews,
      num_ratings,
      num_pages,
      original_publish_year,
      series,
      genres,
      awards,
      place,minmax_norm_ratings,normalise_mean


  What does it do?
  It scrapes links to books, it then runs a second scrape on all of these individual books urls to get
  the book data listed in OUTPUT.


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

    ABOUT: command_line_interface()
      This function prompts the user to specify how much data they wish to scrape. The first question
      is a yes/no question asking if they want to scrape a range of book lists. Answering no defaults
      the scraper to search from a single list of 100 books where they can enter the specific pagination
      number they wish to scrape.
              [** INSERT IMAGE HERE **]

      If the user answers yes then they will be prompted to enter 2 numbers, the pagination number to start
      the scrape on and the pagination number to end it on.
              E.g. selecting '1' and '10' will scrape 10 lists of 100 books each.
              [** INSERT IMAGE HERE **]

    ABOUT: Terminal messages
      The first process of the scraper is to collect individual book links (see ABOUT: hundred_link_grabber()).
      As this function runs it will confirm that it has received the quantity of links it was looking for.










How to use: data_preprocessor.py

How to use: data_scraper.py
