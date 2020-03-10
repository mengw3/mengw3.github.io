"""
do web scraper for an author page
"""
import requests
from bs4 import BeautifulSoup
import numpy as geek


class WebScraperAuthor:
    """
    do web scraper for an author page
    """
    def __init__(self):
        """
        initial all variables
        """
        self.name = ""
        self.author_url = ""
        self.author_id = ""
        self.rating = ""
        self.rating_count = ""
        self.review_count = ""
        self.image_url = ""
        self.related_authors = []
        self.author_books = []

    @staticmethod
    def get_name(contents):
        """
        get name of the author
        :param contents: content of the web page
        :return: name of the author
        """
        try:
            name = contents.find('h1', class_='authorName').text.strip()
        except:
            name = ""
        return name

    @staticmethod
    def get_author_id(url):
        """
        get id of the author
        :param url: url of the web page
        :return: id of the author
        """
        try:
            author_id = ""
            for character in url[38:]:
                if not character.isdigit():
                    break
                author_id += character
        except:
            author_id = ""
        return author_id

    @staticmethod
    def get_rating(contents):
        """
        get rating of the author
        :param contents: content of the web page
        :return: rating of the author
        """
        try:
            rating = ""
            number = contents.find('span', class_="rating").text.strip().replace("\n", "")
            for num in number:
                if num.isdigit() or num == ".":
                    rating += num
        except:
            rating = ""
        return rating

    @staticmethod
    def get_rating_count(contents):
        """
        get the number of rating of the author
        :param contents: content of the web page
        :return: the number of rating
        """
        try:
            rating_count = contents.find('span', class_="votes").find("span")['content']
        except:
            rating_count = ""
        return rating_count

    @staticmethod
    def get_review_count(contents):
        """
        get the number of review of the author
        :param contents: content of the web page
        :return: the number of review
        """
        try:
            review_count = contents.find('span', class_="count").find("span")['content']
        except:
            review_count = ""
        return review_count

    @staticmethod
    def get_image_url(soup):
        """
        get image url of the author
        :param soup: soup of the web page
        :return: author's image url
        """
        try:
            image_url = soup.find('div', class_="leftContainer").find("img")['src']
        except:
            image_url = ""
        return image_url

    @staticmethod
    def get_relate_authors(contents):
        """
        get related authors of the author
        :param contents: content of the web page
        :return: list of related authors with name and url
        """
        try:
            url = contents.find('div', class_="hreview-aggregate").findAll("a")[1]['href']
            header = 'https://www.goodreads.com'
            # print(header + url)
            page = requests.get(header + url)
            soup = BeautifulSoup(page.content, "html.parser")
            contents = soup.findAll('div', class_="listWithDividers__item")
            authors_name = []
            authors_url = []
            i = 0
            for item in contents:
                author = item.find('a', class_="gr-h3 gr-h3--serif gr-h3--noMargin")
                # print(author)
                if i != 0:
                    authors_name.append(author.find('span', itemprop="name").text)
                    # print(author.find('span', itemprop="name").text)
                    authors_url.append(author['href'])
                    # print(author['href'])
                i = i + 1
            relate_authors = geek.c_[(authors_name, authors_url)]
        except:
            relate_authors = ""
        return relate_authors

    @staticmethod
    def get_author_books(contents):
        """
        get books who are written by the author
        :param contents: content of the web page
        :return: names and urls of author's books
        """
        try:
            url = contents.find('div', itemtype="https://schema.org/Collection").find('a', class_="actionLink")['href']
            # print(url)
            header = 'https://www.goodreads.com'
            # print(header + url)
            page = requests.get(header + url)
            soup = BeautifulSoup(page.content, "html.parser")
            contents = soup.find('div', class_="leftContainer").find('table', class_="tableList").findAll("tr")
            books_name = []
            books_url = []
            for item in contents:
                books_name.append(item.find('a', class_="bookTitle").find("span").text)
                # print(book.find('a', class_="bookTitle").find("span").text)
                books_url.append(header + item.find('a', class_="bookTitle")['href'])
                # print(header + book.find('a', class_="bookTitle")['href'])
            author_books = geek.c_[(books_name, books_url)]
        except:
            author_books = ""
        return author_books

    def get_info(self, url):
        """
        get information of the author
        :param url: url of the web page
        :return: all kinds of information of the author, return nothing if the input url is None
        """
        if url is None:
            return
        page = requests.get(url)
        soup = BeautifulSoup(page.content, "html.parser")
        contents = soup.find('div', class_="rightContainer")
        self.name = self.get_name(contents)
        print(self.name)
        self.author_url = url
        print(self.author_url)
        self.author_id = self.get_author_id(url)
        print(self.author_id)
        self.rating = self.get_rating(contents)
        print(self.rating)
        self.rating_count = self.get_rating_count(contents)
        print(self.rating_count)
        self.review_count = self.get_review_count(contents)
        print(self.review_count)
        self.image_url = self.get_image_url(soup)
        print(self.image_url)
        self.related_authors = self.get_relate_authors(contents)
        print(len(self.related_authors))
        print(self.related_authors)
        self.author_books = self.get_author_books(contents)
        print(len(self.get_author_books(contents)))
        print(self.author_books)

    def store_data(self):
        """
        put all data of the author in a list
        :return: the list of all data
        """
        data = {}
        data['name'] = self.name
        data['author_url'] = self.author_url
        data['author_id'] = self.author_id
        data['rating'] = self.rating
        data['rating_count'] = self.rating_count
        data['review_count'] = self.review_count
        data['image_url'] = self.image_url
        data['related_authors'] = []
        for author in self.related_authors:
            data['related_authors'].append(author.tolist())
        data['author_books'] = []
        for book in self.author_books:
            data['author_books'].append(book.tolist())
        return data
        # json_object = json.dumps(data, indent=4)
        # with open('authors.json', 'w') as f:
        #     f.write(json_object)


# if __name__ == "__main__":
#     print("Start")
#     info_author = WebScraperAuthor()
# #     info_author.get_info('https://www.goodreads.com/author/show/60805.Joshua_Bloch')
# #     info_author.store_data()
#     info_author.get_info('https://www.goodreads.com/author/show/45372.Robert_C_Martin')
#     # info_author.store_data()
#     print("Finished")
