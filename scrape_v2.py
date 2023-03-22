import sys
# this tells the interpreter to look for locally installed packages first, nonpersistant cmd
sys.path.insert(0, 'packages')
import csv
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from tqdm import tqdm

def scrape_books(url):
    # base_url needed for link references
    base_url = url
    print(f'URL to scrape: {base_url}')
    
    try:
        # Create a CSV file to store the data
        with open('books.csv', 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['Title', 'Link', 'Price', 'Availability']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            print('Starting scraping operations...')
            # start progress_bar so user knows its doing something... 
            # typically takes about 18-20 seconds total for these 50 pages
            # TODO_future_feature - determine the number of pages to be scraped and update this dynamically?
            progress_bar = tqdm(total=50)

            # Loop through each page and get books from that page
            while url:

                # Fetch the current page and parse it using BeautifulSoup
                try:
                    response = requests.get(url)
                    response.raise_for_status()
                    # update user on status
                    progress_bar.update()
                    soup = BeautifulSoup(response.text, 'html.parser')
                except requests.exceptions.RequestException as e:
                    print(f'An error occurred while fetching {url}: {e}')
                    break

                try:
                    # Find all books on the page
                    books = soup.find_all('article', class_='product_pod')
                    
                    for book in books:
                        title = book.find('h3').find('a')['title']
                        # links after the first page dont have the 'catalogue/' in the url thats why this is here
                        try:
                            next_page
                        except NameError:
                            not_first_page = False
                        else:
                            not_first_page = True
                        link = (base_url + 'catalogue/' + book.find('h3').find('a')['href']) if (not_first_page and (base_url == 'http://books.toscrape.com/')) else (base_url + book.find('h3').find('a')['href'])
                        price = book.find(class_='price_color').text[1:]
                        availability = book.find(class_='instock availability').text.strip()

                        # Write the data to the CSV file
                        writer.writerow({'Title': title, 'Link': link, 'Price': price, 'Availability': availability})

                except Exception as e:
                    print(f'An error occurred while parsing the page: {e}')
                    break

                # Check if there is a next page and update the URL accordingly
                next_page = soup.find(class_='next')
                url = urljoin(url, next_page.find('a')['href']) if next_page else None
            # close status bar
            progress_bar.close()
            print('URL scrape complete.')
            # if not running from cmd line it is helpful to the user to have a pause 
                # before closing the window so they know that its complete
            # input('URL scrape complete. Press enter to exit.')
        return 'Program finished success.'
    
    except Exception as e:
        print(f'An error occurred while trying to write to file: {e}')