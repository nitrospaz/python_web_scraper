import unittest
import os
import csv
from scrape_v2 import scrape_books

class TesScrapeBooks(unittest.TestCase):

    def test1_finish_success(self):
        test_param = 'http://books.toscrape.com/'
        result = scrape_books(test_param)
        # if program is successful should return 'Program finished success.'
        self.assertEqual(result, 'Program finished success.')

    def test2_file_exists(self):
        # check is csv file was created and exists
        file_path = os.path.join(os.path.dirname(__file__), 'books.csv')
        self.assertTrue(os.path.exists(file_path))

    def test3_check_csv(self):
        with open('books.csv', 'r', encoding='utf-8') as csv_file:
            reader = csv.reader(csv_file)
            next(reader) #skip first row header
            row_count = sum(1 for row in reader) # count all remaining rows
            print('row count', row_count)
        # test1 should have scraped all pages, created a csv file and have 1000 rows of results
        self.assertEqual(row_count, 1000)

unittest.main()
