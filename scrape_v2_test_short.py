import unittest
import os
import csv
from scrape_v2 import scrape_books

class TesScrapeBooks(unittest.TestCase):

    def test1_finish_success(self):
        test_param = 'http://books.toscrape.com/catalogue/page-49.html'
        result = scrape_books(test_param)
        # if program is successful should return 'Program finished success.'
        self.assertEqual(result, 'Program finished success.')

    def test2_file_exists(self):
        # check is csv file was created and exists
        file_path = os.path.join(os.path.dirname(__file__), 'books.csv')
        self.assertTrue(os.path.exists(file_path))

    # decided to omit skipIf because cmd line output states that all 3 test were run even though one was actually skipped
    # this test will be skipped if the csv file does not exist
    # @unittest.skipIf(not os.path.exists(os.path.join(os.path.dirname(__file__), 'books.csv')), "CSV file does not exist")
    def test3_check_csv(self):
        with open('books.csv', 'r', encoding='utf-8') as csv_file:
            reader = csv.reader(csv_file)
            next(reader) #skip first row header
            row_count = sum(1 for row in reader) # count all remaining rows
            print('row count', row_count)
        # test1 should have scraped 2 pages, created a csv file and have 40 rows of results
        self.assertEqual(row_count, 40)

unittest.main()
