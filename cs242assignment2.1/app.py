from flask import Flask, jsonify, abort, request, render_template
import os
from pymongo import MongoClient
from dotenv import load_dotenv

PROJECT_FOLDER = os.path.expanduser('/')
load_dotenv(os.path.join(PROJECT_FOLDER, '.env'))
MONGODB_USERNAME = os.getenv('MONGODB_USERNAME')
MONGODB_PASSWORD = os.getenv('MONGODB_PASSWORD')

app = Flask(__name__)


def read_from_db():
    mongodb_client = (
            'mongodb+srv://%s:%s@cluster0-x2acz.mongodb.net/test?retryWrites=true&w=majority'
            % (MONGODB_USERNAME, MONGODB_PASSWORD))
    client = MongoClient(mongodb_client)
    database = client.goodreads_data
    return database


@app.route('/')
def initial():
    return "books and authors info scraped from website https://www.goodreads.com", 200


@app.errorhandler(404)
def page_not_found(e):
    """
    error
    :param e: error
    :return: error message
    """
    return "<h1>404</h1><p>The resource could not be found.</p>", 404


@app.route('/api/books', methods=['GET'])
def get_book():
    """
    GET book
    :return: GET book info
    """
    result = []
    query_parameters = request.args
    book_title = query_parameters.get('title')
    print(book_title)
    if book_title:
        parsed_book_title = book_title.replace('"', '')
        database = read_from_db()
        temp = database.books_data.find_one({"title": parsed_book_title})
        if temp is None:
            return page_not_found(404)
        temp.pop('_id')
        print(temp)
        result.append(temp)
        return jsonify({parsed_book_title: result}), 200
    book_author = query_parameters.get('author')
    print(book_author)
    if book_author:
        parsed_book_author = book_author.replace('"', '')
        database = read_from_db()
        temp = database.books_data.find_one({"author": parsed_book_author})
        if temp is None:
            return page_not_found(404)
        temp.pop('_id')
        print(temp)
        result.append(temp)
        return jsonify({parsed_book_author: result}), 200
    book_related_book = query_parameters.get('related_book')
    print(book_related_book)
    if book_related_book:
        parsed_book_related_book = book_related_book.replace('"', '')
        database = read_from_db()
        collection = database.books_data
        for record in collection.find():
            record.pop('_id')
            for sim_book in record['sim_books']:
                if parsed_book_related_book == sim_book[0]:
                    result.append(record)
        if not result:
            return page_not_found(404)
        return jsonify({parsed_book_related_book: result}), 200
    collection = read_from_db().books_data
    for record in collection.find():
        record.pop('_id')
        result.append(record)
    return jsonify({"books": result}), 200


@app.route('/api/authors', methods=['GET'])
def get_author():
    """
    GET author
    :return: GET author info
    """
    result = []
    query_parameters = request.args
    author_name = query_parameters.get('name')
    print(author_name)
    if author_name:
        parsed_author_name = author_name.replace('"', '')
        database = read_from_db()
        temp = database.authors_data.find_one({"name": parsed_author_name})
        if temp is None:
            return page_not_found(404)
        temp.pop('_id')
        print(temp)
        result.append(temp)
        return jsonify({parsed_author_name: result}), 200
    author_book_title = query_parameters.get('book_title')
    print(author_book_title)
    if author_book_title:
        parsed_author_book_title = author_book_title.replace('"', '')
        database = read_from_db()
        collection = database.authors_data
        for record in collection.find():
            record.pop('_id')
            for author_book in record['author_books']:
                if parsed_author_book_title == author_book[0]:
                    result.append(record)
        if not result:
            return page_not_found(404)
        return jsonify({parsed_author_book_title: result}), 200
    collection = read_from_db().authors_data
    for record in collection.find():
        record.pop('_id')
        result.append(record)
    return jsonify({"authors": result}), 200


@app.route('/api/books', methods=['PUT'])
def put_book():
    """
    PUT books
    :return: PUT books info
    """
    result = []
    query_parameters = request.args
    data = request.json
    book_title = query_parameters.get('title')
    if book_title:
        parsed_book_title = book_title.replace('"', '')
        database = read_from_db()
        collection = database.books_data
        temp = collection.find_one({"title": parsed_book_title})
        if temp is None:
            return page_not_found(404)
        my_query = {"title": parsed_book_title}
        new_values = {"$set": data}
        collection.update_one(my_query, new_values)
        temp = collection.find_one(data)
        temp.pop('_id')
        result.append(temp)
        return jsonify({"change book title": result}), 200
    book_id = query_parameters.get('id')
    if book_id:
        parsed_book_id = book_id.replace('"', '')
        database = read_from_db()
        collection = database.books_data
        temp = collection.find_one({"book_id": parsed_book_id})
        if temp is None:
            return page_not_found(404)
        my_query = {"book_id": parsed_book_id}
        new_values = {"$set": data}
        collection.update_one(my_query, new_values)
        temp = collection.find_one(data)
        temp.pop('_id')
        result.append(temp)
        return jsonify({"change book id": result}), 200
    book_isbn = query_parameters.get('isbn')
    if book_isbn:
        parsed_book_isbn = book_isbn.replace('"', '')
        database = read_from_db()
        collection = database.books_data
        temp = collection.find_one({"isbn": parsed_book_isbn})
        if temp is None:
            return page_not_found(404)
        my_query = {"isbn": parsed_book_isbn}
        new_values = {"$set": data}
        collection.update_one(my_query, new_values)
        temp = collection.find_one(data)
        temp.pop('_id')
        result.append(temp)
        return jsonify({"change book isbn": result}), 200
    book_rating = query_parameters.get('rating')
    if book_rating:
        parsed_book_rating = book_rating.replace('"', '')
        database = read_from_db()
        collection = database.books_data
        temp = collection.find_one({"rating": parsed_book_rating})
        if temp is None:
            return page_not_found(404)
        my_query = {"rating": parsed_book_rating}
        new_values = {"$set": data}
        collection.update_one(my_query, new_values)
        temp = collection.find_one(data)
        temp.pop('_id')
        result.append(temp)
        return jsonify({"change book rating": result}), 200
    book_rating_count = query_parameters.get('rating_count')
    if book_rating_count:
        parsed_book_rating_count = book_rating_count.replace('"', '')
        database = read_from_db()
        collection = database.books_data
        temp = collection.find_one({"rating_count": parsed_book_rating_count})
        if temp is None:
            return page_not_found(404)
        my_query = {"rating_count": parsed_book_rating_count}
        new_values = {"$set": data}
        collection.update_one(my_query, new_values)
        temp = collection.find_one(data)
        temp.pop('_id')
        result.append(temp)
        return jsonify({"change book rating count": result}), 200
    book_review_count = query_parameters.get('review_count')
    if book_review_count:
        parsed_book_review_count = book_review_count.replace('"', '')
        database = read_from_db()
        collection = database.books_data
        temp = collection.find_one({"review_count": parsed_book_review_count})
        if temp is None:
            return page_not_found(404)
        my_query = {"review_count": parsed_book_review_count}
        new_values = {"$set": data}
        collection.update_one(my_query, new_values)
        temp = collection.find_one(data)
        temp.pop('_id')
        result.append(temp)
        return jsonify({"change book review count": result}), 200
    return page_not_found(404)


@app.route('/api/authors', methods=['PUT'])
def put_author():
    """
    PUT authors
    :return: PUT authors info
    """
    result = []
    query_parameters = request.args
    data = request.json
    author_name = query_parameters.get('name')
    if author_name:
        parsed_author_name = author_name.replace('"', '')
        database = read_from_db()
        collection = database.authors_data
        temp = collection.find_one({"name": parsed_author_name})
        if temp is None:
            return page_not_found(404)
        my_query = {"name": parsed_author_name}
        new_values = {"$set": data}
        collection.update_one(my_query, new_values)
        temp = collection.find_one(data)
        temp.pop('_id')
        result.append(temp)
        return jsonify({"change author name": result}), 200
    author_url = query_parameters.get('url')
    if author_url:
        parsed_author_url = author_url.replace('"', '')
        database = read_from_db()
        collection = database.authors_data
        temp = collection.find_one({"author_url": parsed_author_url})
        if temp is None:
            return page_not_found(404)
        my_query = {"author_url": parsed_author_url}
        new_values = {"$set": data}
        collection.update_one(my_query, new_values)
        temp = collection.find_one(data)
        temp.pop('_id')
        result.append(temp)
        return jsonify({"change author url": result}), 200
    author_id = query_parameters.get('id')
    if author_id:
        parsed_author_id = author_id.replace('"', '')
        database = read_from_db()
        collection = database.authors_data
        temp = collection.find_one({"author_id": parsed_author_id})
        if temp is None:
            return page_not_found(404)
        my_query = {"author_id": parsed_author_id}
        new_values = {"$set": data}
        collection.update_one(my_query, new_values)
        temp = collection.find_one(data)
        temp.pop('_id')
        result.append(temp)
        return jsonify({"change author id": result}), 200
    author_rating = query_parameters.get('rating')
    if author_rating:
        parsed_author_rating = author_rating.replace('"', '')
        database = read_from_db()
        collection = database.authors_data
        temp = collection.find_one({"rating": parsed_author_rating})
        if temp is None:
            return page_not_found(404)
        my_query = {"rating": parsed_author_rating}
        new_values = {"$set": data}
        collection.update_one(my_query, new_values)
        temp = collection.find_one(data)
        temp.pop('_id')
        result.append(temp)
        return jsonify({"change author rating": result}), 200
    author_rating_count = query_parameters.get('rating_count')
    if author_rating_count:
        parsed_author_rating_count = author_rating_count.replace('"', '')
        database = read_from_db()
        collection = database.authors_data
        temp = collection.find_one({"rating_count": parsed_author_rating_count})
        if temp is None:
            return page_not_found(404)
        my_query = {"rating_count": parsed_author_rating_count}
        new_values = {"$set": data}
        collection.update_one(my_query, new_values)
        temp = collection.find_one(data)
        temp.pop('_id')
        result.append(temp)
        return jsonify({"change author rating count": result}), 200
    author_review_count = query_parameters.get('review_count')
    if author_review_count:
        parsed_author_review_count = author_review_count.replace('"', '')
        database = read_from_db()
        collection = database.authors_data
        temp = collection.find_one({"review_count": parsed_author_review_count})
        if temp is None:
            return page_not_found(404)
        my_query = {"review_count": parsed_author_review_count}
        new_values = {"$set": data}
        collection.update_one(my_query, new_values)
        temp = collection.find_one(data)
        temp.pop('_id')
        result.append(temp)
        return jsonify({"change author review count": result}), 200
    author_image_url = query_parameters.get('image_url')
    if author_image_url:
        parsed_author_image_url = author_image_url.replace('"', '')
        database = read_from_db()
        collection = database.authors_data
        temp = collection.find_one({"image_url": parsed_author_image_url})
        if temp is None:
            return page_not_found(404)
        my_query = {"image_url": parsed_author_image_url}
        new_values = {"$set": data}
        collection.update_one(my_query, new_values)
        temp = collection.find_one(data)
        temp.pop('_id')
        result.append(temp)
        return jsonify({"change author image url": result}), 200
    return page_not_found(404)


@app.route('/api/book', methods=['POST'])
def post_book():
    """
    POST book
    :return: POST book info
    """
    result = []
    data = request.json
    database = read_from_db()
    collection = database.books_data
    collection.insert_one(data)
    temp = collection.find_one(data)
    temp.pop('_id')
    result.append(temp)
    return jsonify({"add a new book": result}), 201


@app.route('/api/books', methods=['POST'])
def post_books():
    """
    POST book
    :return: POST books info
    """
    result = []
    data = request.json
    database = read_from_db()
    collection = database.books_data
    collection.insert_many(data)
    for each in data:
        for record in collection.find(each):
            record.pop('_id')
            result.append(record)
    return jsonify({"add several new books": result}), 201


@app.route('/api/author', methods=['POST'])
def post_author():
    """
    POST author
    :return: POST author info
    """
    result = []
    data = request.json
    database = read_from_db()
    collection = database.authors_data
    collection.insert_one(data)
    temp = collection.find_one(data)
    temp.pop('_id')
    result.append(temp)
    return jsonify({"add a new author": result}), 201


@app.route('/api/authors', methods=['POST'])
def post_authors():
    """
    POST authors
    :return: POST authors info
    """
    result = []
    data = request.json
    database = read_from_db()
    collection = database.authors_data
    collection.insert_many(data)
    for each in data:
        for record in collection.find(each):
            record.pop('_id')
            result.append(record)
    return jsonify({"add several new authors": result}), 201


def delete_book_helper(parameter, parsed_parameter):
    """
    delete book helper function
    :param parameter: tag
    :param parsed_parameter: info
    :return: if delete
    """
    database = read_from_db()
    collection = database.books_data
    temp = collection.find_one({parameter: parsed_parameter})
    if temp is None:
        return "not found"
    collection.delete_one({parameter: parsed_parameter})


@app.route('/api/book', methods=['DELETE'])
def delete_book():
    """
    DELETE book
    :return: DELETE book info
    """
    query_parameters = request.args
    book_title = query_parameters.get('title')
    if book_title:
        parsed_book_title = book_title.replace('"', '')
        parameter = "title"
        result = delete_book_helper(parameter, parsed_book_title)
        if result == "not found":
            return page_not_found(404)
        return jsonify({"delete a book": parsed_book_title}), 201
    book_url = query_parameters.get('url')
    if book_url:
        parsed_book_url = book_url.replace('"', '')
        parameter = "book_url"
        result = delete_book_helper(parameter, parsed_book_url)
        if result == "not found":
            return page_not_found(404)
        return jsonify({"delete a book": parsed_book_url}), 201
    book_id = query_parameters.get('id')
    if book_id:
        parsed_book_id = book_id.replace('"', '')
        parameter = "book_id"
        result = delete_book_helper(parameter, parsed_book_id)
        if result == "not found":
            return page_not_found(404)
        return jsonify({"delete a book": parsed_book_id}), 201
    book_isbn = query_parameters.get('isbn')
    if book_isbn:
        parsed_book_isbn = book_isbn.replace('"', '')
        parameter = "isbn"
        result = delete_book_helper(parameter, parsed_book_isbn)
        if result == "not found":
            return page_not_found(404)
        return jsonify({"delete a book": parsed_book_isbn}), 201
    book_author_url = query_parameters.get('author_url')
    if book_author_url:
        parsed_book_author_url = book_author_url.replace('"', '')
        parameter = "author_url"
        result = delete_book_helper(parameter, parsed_book_author_url)
        if result == "not found":
            return page_not_found(404)
        return jsonify({"delete a book": parsed_book_author_url}), 201
    book_author = query_parameters.get('author')
    if book_author:
        parsed_book_author = book_author.replace('"', '')
        parameter = "author"
        result = delete_book_helper(parameter, parsed_book_author)
        if result == "not found":
            return page_not_found(404)
        return jsonify({"delete a book": parsed_book_author}), 201
    book_rating = query_parameters.get('rating')
    if book_rating:
        parsed_book_rating = book_rating.replace('"', '')
        parameter = "rating"
        result = delete_book_helper(parameter, parsed_book_rating)
        if result == "not found":
            return page_not_found(404)
        return jsonify({"delete a book": parsed_book_rating}), 201
    book_rating_count = query_parameters.get('rating_count')
    if book_rating_count:
        parsed_book_rating_count = book_rating_count.replace('"', '')
        parameter = "rating_count"
        result = delete_book_helper(parameter, parsed_book_rating_count)
        if result == "not found":
            return page_not_found(404)
        return jsonify({"delete a book": parsed_book_rating_count}), 201
    book_review_count = query_parameters.get('review_count')
    if book_review_count:
        parsed_book_review_count = book_review_count.replace('"', '')
        parameter = "review_count"
        result = delete_book_helper(parameter, parsed_book_review_count)
        if result == "not found":
            return page_not_found(404)
        return jsonify({"delete a book": parsed_book_review_count}), 201
    book_image_url = query_parameters.get('image_url')
    if book_image_url:
        parsed_book_image_url = book_image_url.replace('"', '')
        parameter = "image_url"
        result = delete_book_helper(parameter, parsed_book_image_url)
        if result == "not found":
            return page_not_found(404)
        return jsonify({"delete a book": parsed_book_image_url}), 201
    return page_not_found(404)


def delete_author_helper(parameter, parsed_parameter):
    """
    delete author helper function
    :param parameter: tag
    :param parsed_parameter: info
    :return: if delete
    """
    database = read_from_db()
    collection = database.authors_data
    temp = collection.find_one({parameter: parsed_parameter})
    if temp is None:
        return "not found"
    collection.delete_one({parameter: parsed_parameter})


@app.route('/api/author', methods=['DELETE'])
def delete_author():
    """
    DELETE author
    :return: DELETE author info
    """
    query_parameters = request.args
    author_name = query_parameters.get('name')
    if author_name:
        parsed_author_name = author_name.replace('"', '')
        parameter = "name"
        result = delete_author_helper(parameter, parsed_author_name)
        if result == "not found":
            return page_not_found(404)
        return jsonify({"delete an author": parsed_author_name}), 201
    author_url = query_parameters.get('url')
    if author_url:
        parsed_author_url = author_url.replace('"', '')
        parameter = "author_url"
        result = delete_author_helper(parameter, parsed_author_url)
        if result == "not found":
            return page_not_found(404)
        return jsonify({"delete an author": parsed_author_url}), 201
    author_id = query_parameters.get('id')
    if author_id:
        parsed_author_id = author_id.replace('"', '')
        parameter = "author_id"
        result = delete_author_helper(parameter, parsed_author_id)
        if result == "not found":
            return page_not_found(404)
        return jsonify({"delete an author": parsed_author_id}), 201
    author_rating = query_parameters.get('rating')
    if author_rating:
        parsed_author_rating = author_rating.replace('"', '')
        parameter = "rating"
        result = delete_author_helper(parameter, parsed_author_rating)
        if result == "not found":
            return page_not_found(404)
        return jsonify({"delete an author": parsed_author_rating}), 201
    author_rating_count = query_parameters.get('rating_count')
    if author_rating_count:
        parsed_author_rating_count = author_rating_count.replace('"', '')
        parameter = "rating_count"
        result = delete_author_helper(parameter, parsed_author_rating_count)
        if result == "not found":
            return page_not_found(404)
        return jsonify({"delete an author": parsed_author_rating_count}), 201
    author_review_count = query_parameters.get('review_count')
    if author_review_count:
        parsed_author_review_count = author_review_count.replace('"', '')
        parameter = "review_count"
        result = delete_author_helper(parameter, parsed_author_review_count)
        if result == "not found":
            return page_not_found(404)
        return jsonify({"delete an author": parsed_author_review_count}), 201
    author_image_url = query_parameters.get('image_url')
    if author_image_url:
        parsed_author_image_url = author_image_url.replace('"', '')
        parameter = "image_url"
        result = delete_author_helper(parameter, parsed_author_image_url)
        if result == "not found":
            return page_not_found(404)
        return jsonify({"delete an author": parsed_author_image_url}), 201
    return page_not_found


@app.route('/books', methods=['GET'])
def get_book_web():
    """
    get list of books
    :return: web page
    """
    result = []
    collection = read_from_db().books_data
    for record in collection.find():
        record.pop('_id')
        result.append(record)
    return render_template('book_list.html', u=result)


searchBook = False


@app.route('/bookM', methods=['GET','POST'])
def change_book_web():
    """
    manipulate books
    :return: web page
    """
    global searchBook
    searchBook = False
    if request.method == "POST":
        if request.form['input'] == "Insert":
            searchBook = False
            form = request.form.to_dict()

            # data to read
            title = form['title']
            book_url = form['book_url']
            book_id = form['book_id']
            isbn = form['isbn']
            author_url = form['author_url']
            author = form['author']
            rating = form['rating']
            rating_count = form['rating_count']
            review_count = form['review_count']
            image_url = form['image_url']

            output = []
            data = {}
            data['book_url'] = book_url
            data['title'] = title
            data['book_id'] = book_id
            data['isbn'] = isbn
            data['author_url'] = author_url
            data['author'] = author
            data['rating'] = rating
            data['rating_count'] = rating_count
            data['review_count'] = review_count
            data['image_url'] = image_url
            data['sim_books'] = []
            output.append(data)

            database = read_from_db()
            collection = database.books_data
            collection.insert_many(output)

        if request.form['input'] == "Search":
            form = request.form.to_dict()
            search_book_id = form['search_book_id']
            searchBook = True

        if request.form['input'] == "Delete":
            searchBook = False
            form = request.form.to_dict()
            deleted_book_id = form['deleted_book_id']
            parameter = "book_id"
            delete_book_helper(parameter, deleted_book_id)

        if request.form['input'] == "Update":
            searchBook = False
            form = request.form.to_dict()
            # data to read
            input_book_id = form['input_book_id']
            title = form['update_title']
            book_url = form['update_book_url']
            book_id = form['update_book_id']
            isbn = form['update_isbn']
            author_url = form['update_author_url']
            author = form['update_author']
            rating = form['update_rating']
            rating_count = form['update_rating_count']
            review_count = form['update_review_count']
            image_url = form['update_image_url']

            data = {}
            if book_url:
                data['book_url'] = book_url
            if title:
                data['title'] = title
            if book_id:
                data['book_id'] = book_id
            if isbn:
                data['isbn'] = isbn
            if author_url:
                data['author_url'] = author_url
            if author:
                data['author'] = author
            if rating:
                data['rating'] = rating
            if rating_count:
                data['rating_count'] = rating_count
            if review_count:
                data['review_count'] = review_count
            if image_url:
                data['image_url'] = image_url

            result = []
            database = read_from_db()
            collection = database.books_data
            temp = collection.find_one({"book_id": input_book_id})
            if temp is None:
                return render_template('book_list.html', u=result)
            my_query = {"book_id": input_book_id}
            new_values = {"$set": data}
            collection.update_one(my_query, new_values)
            temp = collection.find_one(data)
            temp.pop('_id')
            result.append(temp)
            return render_template('book_list.html', u=result)

    if searchBook:
        result = []
        collection = read_from_db().books_data
        temp = collection.find_one({"book_id": search_book_id})
        if temp is None:
            return render_template('book_list.html', u=result)
        result.append(temp)
        return render_template('book_list.html', u=result)
    else:
        return render_template('books_manipulation.html')


searchAuthor = False


@app.route('/authorM', methods=['GET','POST'])
def change_author_web():
    """
    manipulate authors
    :return: web page
    """
    global searchAuthor
    searchAuthor = False
    if request.method == "POST":
        if request.form['input'] == "Insert":
            searchAuthor = False
            form = request.form.to_dict()

            # data to read
            name = form['name']
            author_url = form['author_url']
            author_id = form['author_id']
            rating = form['rating']
            rating_count = form['rating_count']
            review_count = form['review_count']
            image_url = form['image_url']

            output = []
            data = {}
            data['name'] = name
            data['author_url'] = author_url
            data['author_id'] = author_id
            data['rating'] = rating
            data['rating_count'] = rating_count
            data['review_count'] = review_count
            data['image_url'] = image_url
            data['related_authors'] = []
            data['author_books'] = []
            output.append(data)

            database = read_from_db()
            collection = database.authors_data
            collection.insert_many(output)

        if request.form['input'] == "Search":
            form = request.form.to_dict()
            search_author_id = form['search_author_id']
            searchAuthor = True

        if request.form['input'] == "Delete":
            searchAuthor = False
            form = request.form.to_dict()
            deleted_author_id = form['deleted_author_id']
            parameter = "author_id"
            delete_author_helper(parameter, deleted_author_id)

        if request.form['input'] == "Update":
            searchAuthor = False
            form = request.form.to_dict()
            # data to read
            input_author_id = form['input_author_id']
            name = form['update_name']
            author_url = form['update_author_url']
            author_id = form['update_author_id']
            rating = form['update_rating']
            rating_count = form['update_rating_count']
            review_count = form['update_review_count']
            image_url = form['update_image_url']

            data = {}
            if name:
                data['name'] = name
            if author_url:
                data['author_url'] = author_url
            if author_id:
                data['author_id'] = author_id
            if rating:
                data['rating'] = rating
            if rating_count:
                data['rating_count'] = rating_count
            if review_count:
                data['review_count'] = review_count
            if image_url:
                data['image_url'] = image_url

            result = []
            database = read_from_db()
            collection = database.authors_data
            temp = collection.find_one({"author_id": input_author_id})
            if temp is None:
                return render_template('author_list.html', u=result)
            my_query = {"author_id": input_author_id}
            new_values = {"$set": data}
            collection.update_one(my_query, new_values)
            temp = collection.find_one(data)
            temp.pop('_id')
            result.append(temp)
            return render_template('author_list.html', u=result)

    if searchAuthor:
        result = []
        collection = read_from_db().authors_data
        temp = collection.find_one({"author_id": search_author_id})
        if temp is None:
            return render_template('author_list.html', u=result)
        result.append(temp)
        return render_template('author_list.html', u=result)
    else:
        return render_template('authors_manipulation.html')


@app.route('/authors', methods=['GET'])
def get_author_web():
    """
    get list of authors
    :return: web page
    """
    result = []
    collection = read_from_db().authors_data
    for record in collection.find():
        record.pop('_id')
        result.append(record)
    return render_template('author_list.html', u=result)


if __name__ == '__main__':
    app.run(debug=True)
