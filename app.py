import json
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configure SQLAlchemy to connect to your PostgreSQL database
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:root@localhost:5432/Library'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable modification tracking (optional but recommended)
db = SQLAlchemy(app)

# Define the Book model for both Library and RestrictedLibrary
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(), nullable=False)
    author = db.Column(db.String(), nullable=False)
    genre = db.Column(db.String(), nullable=False)
    library_type = db.Column(db.String(), nullable=False)  # to distinguish between 'library' and 'restricted-library'

# Create all tables
with app.app_context():
    db.create_all()
    print("Tables created successfully")

# Routes for CRUD operations on Book entities
@app.route("/")
def index():
    return "Hello pandiyan"

@app.route("/library/add", methods=["POST"])
def add_book_to_library():
    data = request.get_json()
    title = data['title']
    author = data['author']
    genre = data['genre']
    book = Book(title=title, author=author, genre=genre, library_type='library')
    db.session.add(book)
    db.session.commit()
    return jsonify("New Book added to Library")

@app.route("/library/books", methods=["GET"])
def get_books_in_library():
    all_books = []
    books = Book.query.filter_by(library_type='library').all()
    for book in books:
        all_books.append({
            "title": book.title,
            "author": book.author,
            "genre": book.genre
        })
    return jsonify(all_books)

@app.route("/library/remove", methods=["DELETE"])
def remove_book_from_library():
    data = request.get_json()
    title = data['title']
    book = Book.query.filter_by(title=title, library_type='library').first()
    if book:
        db.session.delete(book)
        db.session.commit()
        return jsonify("Book removed from Library")
    else:
        return jsonify("Book Not Found in Library"), 404

@app.route("/restricted-library/add", methods=["POST"])
def add_book_to_restricted_library():
    data = request.get_json()
    title = data['title']
    author = data['author']
    genre = data['genre']
    book = Book(title=title, author=author, genre=genre, library_type='restricted-library')
    db.session.add(book)
    db.session.commit()
    return jsonify("New Book added to Restricted Library")

@app.route("/restricted-library/books", methods=["GET"])
def get_books_in_restricted_library():
    all_books = []
    books = Book.query.filter_by(library_type='restricted-library').all()
    for book in books:
        all_books.append({
            "title": book.title,
            "author": book.author,
            "genre": book.genre
        })
    return jsonify(all_books)

@app.route("/restricted-library/remove", methods=["DELETE"])
def remove_book_from_restricted_library():
    data = request.get_json()
    title = data['title']
    book = Book.query.filter_by(title=title, library_type='restricted-library').first()
    if book:
        db.session.delete(book)
        db.session.commit()
        return jsonify("Book removed from Restricted Library")
    else:
        return jsonify("Book Not Found in Restricted Library"), 404

if __name__ == "__main__":
    app.run(debug=True)
