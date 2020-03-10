"""
do web scraper for a book page
"""
import requests
from bs4 import BeautifulSoup
import numpy as geek


class WebScraperBook:
    """
    do web scraper for a book page
    """
    def __init__(self):
        """
        initial all variables
        """
        self.book_url = ""
        self.title = ""
        self.book_id = ""
        self.isbn = ""
        self.author_url = ""
        self.author = ""
        self.rating = ""
        self.rating_count = ""
        self.review_count = ""
        self.image_url = ""
        self.sim_books = []

    @staticmethod
    def get_title(contents):
        """
        get title of the book
        :param contents: content of the web page
        :return: title of the book
        """
        try:
            title = contents.find('h1', id='bookTitle').text.strip()
        except:
            title = ""
        return title

    @staticmethod
    def get_book_id(url):
        """
        get id of the book
        :param url: url of the web page
        :return: book id
        """
        try:
            book_id = ""
            for character in url[36:]:
                if not character.isdigit():
                    break
                book_id += character
        except:
            book_id = ""
        return book_id

    @staticmethod
    def get_isbn(contents):
        """
        get isbn of the book
        :param contents: content of the web page
        :return: isbn of the book
        """
        try:
            isbn = ""
            isbn0 = contents.find('div', id='bookDataBox').findAll('div', class_="infoBoxRowItem")[1].text.strip().replace("\n", "")
            for num in isbn0:
                if num == " ":
                    break
                isbn += num
        except:
            isbn = ""
        return isbn

    @staticmethod
    def get_author_url(contents):
        """
        get author's url of the book
        :param contents: content of the web page
        :return: author's url of the book
        """
        try:
            author_url = contents.find('div', id="bookAuthors").find("a")['href']
        except:
            author_url = ""
        return author_url

    @staticmethod
    def get_author(contents):
        """
        get author's name of the book
        :param contents: content of the web page
        :return: author's name of the book
        """
        try:
            author = contents.find('div', id="bookAuthors").find("a").find("span").text.strip()
        except:
            author = ""
        return author

    @staticmethod
    def get_rating(contents):
        """
        get rating of the book
        :param contents: content of the web page
        :return: rating of the book
        """
        try:
            rating = contents.find('span', itemprop="ratingValue").text.strip()
        except:
            rating = ""
        return rating

    @staticmethod
    def get_rating_count(contents):
        """
        get the number of rating of the book
        :param contents: content of the web page
        :return: the number of rating
        """
        try:
            rating_count = contents.find('div', id="bookMeta").findAll("meta")[0]['content']
        except:
            rating_count = ""
        return rating_count

    @staticmethod
    def get_review_count(contents):
        """
        get the number of review of the book
        :param contents: content of the web page
        :return: the number of review
        """
        try:
            review_count = contents.find('div', id="bookMeta").findAll("meta")[1]['content']
        except:
            review_count = ""
        return review_count

    @staticmethod
    def get_image_url(contents):
        """
        get image url of the book
        :param contents: content of the web page
        :return: book's image url
        """
        try:
            image_url = contents.find('div', class_="bookCoverPrimary").find("a").find('img')['src']
        except:
            image_url = ""
        return image_url

    @staticmethod
    def get_sim_books(soup):
        """
        get similar books' name and url
        :param soup: soup of the web page
        :return: list of similar books with name and url
        """
        try:
            books = soup.find('div', class_="rightContainer").find('div', class_="carouselRow").findAll("a")
            sim_book_name = []
            sim_book_url = []
            for book in books:
                # print(books[i].find("img")['alt'])
                sim_book_name.append(book.find("img")['alt'])
                # print(books[i]['href'])
                sim_book_url.append(book['href'])
            sim_books = geek.c_[(sim_book_name, sim_book_url)]
        except:
            sim_books = ""
        return sim_books

    def get_info(self, url):
        """
        get information of the book
        :param url: url of the web page
        :return: all kinds of information of the author, return nothing if the input url is None
        """
        if url is None:
            return
        page = requests.get(url)
        soup = BeautifulSoup(page.content, "html.parser")
        contents = soup.find('div', class_="leftContainer")
        self.book_url = url
        print(self.book_url)
        self.title = self.get_title(contents)
        print(self.title)
        self.book_id = self.get_book_id(url)
        print(self.book_id)
        self.isbn = self.get_isbn(contents)
        print(self.isbn)
        self.author_url = self.get_author_url(contents)
        print(self.author_url)
        self.author = self.get_author(contents)
        print(self.author)
        self.rating = self.get_rating(contents)
        print(self.rating)
        self.rating_count = self.get_rating_count(contents)
        print(self.rating_count)
        self.review_count = self.get_review_count(contents)
        print(self.review_count)
        self.image_url = self.get_image_url(contents)
        print(self.image_url)
        self.sim_books = self.get_sim_books(soup)
        print(len(self.sim_books))
        print(self.sim_books)

    def store_data(self):
        """
        put all data of the author in a list
        :return: the list of all data
        """
        data = {}
        data['book_url'] = self.book_url
        data['title'] = self.title
        data['book_id'] = self.book_id
        data['isbn'] = self.isbn
        data['author_url'] = self.author_url
        data['author'] = self.author
        data['rating'] = self.rating
        data['rating_count'] = self.rating_count
        data['review_count'] = self.review_count
        data['image_url'] = self.image_url
        data['sim_books'] = []
        for book in self.sim_books:
            data['sim_books'].append(book.tolist())
        return data
        # json_object = json.dumps(data, indent=4)
        # with open(self.title + '.json', 'w') as f:
        #     f.write(json_object)


# if __name__ == "__main__":
#         print("Start")
#         info_book = WebScraperBook()
#         info_book.get_info('https://www.goodreads.com/book/show/3735293-clean-code')
#         info_book.store_data()
#         print("Finished")
