"""
continue finding next book and its author until hit the target number
"""
import sys

import json
import requests
from bs4 import BeautifulSoup
from elements import webscraper_book
from elements import webscraper_author
import database


class Loop:
    """
    continue finding next book and its author until hit the target number
    """
    def __init__(self, num_books=0, num_authors=0):
        """
        initial all variables
        :param num_books: the number of books
        :param num_authors: the number of authors
        """
        self.num_books = num_books
        self.num_authors = num_authors
        self.books_list = []
        self.author_list = []
        self.output_books_list = []
        self.output_authors_list = []

    def find_author_url(self, book_url):
        """
        find current book's author url
        :param book_url: current book's url
        :return: current book's author url
        """
        page = requests.get(book_url)
        soup = BeautifulSoup(page.content, "html.parser")
        contents = soup.find('div', class_="leftContainer")
        author_name = self.find_author_name(contents)
        if author_name not in self.author_list:
            if author_name != "":
                self.author_list.append(author_name)
                author_url = contents.find('div', id="bookAuthors").find("a")['href']
                return author_url
        return None

    def find_next_book(self, book_url):
        """
        find next book
        :param book_url: current book's url
        :return: next book's url
        """
        page = requests.get(book_url)
        soup = BeautifulSoup(page.content, "html.parser")
        books = soup.find('div', class_="rightContainer").find('div', class_="carouselRow").findAll("a")
        for book in books:
            next_book_url = book['href']
            next_book_name = self.find_book_name(next_book_url)
            if next_book_name not in self.books_list:
                # print(next_book_name)
                if next_book_name != "":
                    self.books_list.append(next_book_name)
                    return next_book_url
        return next_book_url

    @staticmethod
    def find_author_name(contents):
        """
        find current author's name
        :param contents: content of the web page
        :return: current author's name
        """
        author = contents.find('div', id="bookAuthors").find("a").find("span").text.strip()
        return author

    @staticmethod
    def find_book_name(book_url):
        """
        find current book's name
        :param book_url: url of the web page
        :return: current book's name
        """
        page = requests.get(book_url)
        soup = BeautifulSoup(page.content, "html.parser")
        contents = soup.find('div', class_="leftContainer")
        title = contents.find('div', id='bookDataBox').findAll('div', class_="infoBoxRowItem")[0].text.strip()
        return title

    def get_data(self):
        """
        start from the given url https://www.goodreads.com/book/show/3735293-clean-code.
        Scrape current book page and its author page.
        Move to next book page
        Keep doing until hit the target number
        At the end, upload json files to Mongo database
        :return: required info in json format
        """
        url = 'https://www.goodreads.com/book/show/3735293-clean-code'
        book_name = self.find_book_name(url)
        self.books_list.append(book_name)
        print(self.books_list)
        while self.num_books != 0 or self.num_authors != 0:
            info_book = webscraper_book.WebScraperBook()
            info_book.get_info(url)
            curr_book = info_book.store_data()
            self.output_books_list.append(curr_book)
            # print(self.books_list)
            if self.num_books != 0:
                self.num_books = self.num_books - 1
            print(self.num_books)
            author_url = self.find_author_url(url)
            info_author = webscraper_author.WebScraperAuthor()
            info_author.get_info(author_url)
            curr_author = info_author.store_data()
            self.output_authors_list.append(curr_author)
            # print(self.author_list)
            if self.num_authors != 0:
                self.num_authors = self.num_authors - 1
            print(self.num_authors)
            url = self.find_next_book(url)
        json_object_book = json.dumps(self.output_books_list, indent=4)
        with open('books.json', 'w') as file:
            file.write(json_object_book)
        json_object_author = json.dumps(self.output_authors_list, indent=4)
        with open('authors.json', 'w') as file:
            file.write(json_object_author)
        information = database.PyMongo()
        information.upload_to_database()
        information.download_from_database()


def main(argv):
    """
    read input from terminal
    :param argv: input from terminal
    :return: initialize Loop and return nothing
    """
    if len(argv) != 3:
        print("""give wrong number of parameters""")
        return
    if len(argv) == 3:
        if int(argv[1]) > 2000 or int(argv[2]) > 2000:
            print("""exceed max number""")
            return
        loop = Loop(int(argv[1]), int(argv[2]))
        loop.get_data()
        return


if __name__ == "__main__":
    print("Start")
    main(sys.argv)
    print("Finished")
