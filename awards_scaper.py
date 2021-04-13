import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup
from requests import get


def hundred_link_grabber(all_books_url):
    page = requests.get(url=all_books_url)
    soup = BeautifulSoup(page.content, 'html.parser')
    links_section = soup.find_all('a', class_="bookTitle", href=True)
    final_links = ["https://www.goodreads.com" + link['href'] for link in links_section]
    len_links = len(final_links)
    print(f"Succesfully generated {len_links}")
    return final_links

def get_awards(page_soup):
    request=requests.get(page_soup)
    page_soup=BeautifulSoup(request.content,'html.parser')
    try:
        awards_section = page_soup.find('div', itemprop="awards")
        awards = awards_section.find_all('a', class_="award")
        main_awards = [award.get_text().strip() for award in awards]
        str_main_awards = ", ".join(main_awards)
        return str_main_awards
    except:
        print("Oh no get_awards failed")
        return np.nan
#test=get_awards("https://www.goodreads.com/book/show/2.Harry_Potter_and_the_Order_of_the_Phoenix")
#print(test)

def get_awards_count(page_soup):
    request=requests.get(page_soup)
    page_soup=BeautifulSoup(request.content,'html.parser')
    try:
        awards_section = page_soup.find('div', itemprop="awards")
        awards = awards_section.find_all('a', class_="award")
        main_awards = [award.get_text().strip() for award in awards]
        str_main_awards =len((", ".join(main_awards)).split(','))
        return str_main_awards
    except:
        print("Oh no get_awards failed")
        return np.nan
test=get_awards_count("https://www.goodreads.com/book/show/7260188-mockingjay")
print(test)


def get_all(list_of_urls):
    pd_data =[]
    for book_url in list_of_urls:
        print(f"Working on url: {book_url}")
        request = requests.get(book_url)
        page_soup = BeautifulSoup(request.content,'html.parser')
        list_of_awards = get_awards_list(page_soup)
        number_of_awards = get_awards_count(page_soup)
        a_book = {
            "url": [book_url],
            "list_of_awards":[list_of_awards],
            "number_of_awards" :[number_of_awards]}
        pd_data.append(a_book)
    return pd_data

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


books = main_app(1)
df = pd.DataFrame(merge_data_dicts(books))

df.to_csv('scraped_awards.csv', index = False, header=True)
