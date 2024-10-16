from flask import Flask, render_template, redirect, request, url_for, flash, jsonify
from data_models import Book, Author, db
from marshmallow import ValidationError
import os
from schemas import author_schema, book_schema
from werkzeug.utils import secure_filename

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(basedir, "data/library.sqlite")}'
# Generates a random 24-byte key
secret_key = os.urandom(24)
app.secret_key = secret_key
app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, 'static/images')

# Ensure the folder exists (create it if it doesn't)
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
db.init_app(app)


#with app.app_context():
#db.create_all()

@app.route('/add_author', methods=['GET', 'POST'])
def add_author():
    """
    Handles the addition of a new author.
    - GET: Renders the add author form.
    - POST: Validates the form data and adds the author to the database.
    """
    if request.method == 'GET':
        return render_template('add_author.html')
    author_schemas = author_schema.AuthorSchema()
    form_data = request.form.to_dict()
    try:
        data = author_schemas.load(form_data)
        author = Author(name=data['name'],
                        birth_date=data['birthdate'],
                        date_of_death=data['date_of_death'])
        db.session.add(author)
        db.session.commit()
        flash('Author added successfully!', 'success')
        return redirect(url_for('add_author'))
    except ValidationError as err:
        # If there are validation errors, display them on the form
        for field, error in err.messages.items():
            flash(f"{field}: {', '.join(error)}", 'error')
        return redirect(url_for('add_author'))


@app.route('/add_book', methods=['GET', 'POST'])
def add_book():
    """
    Handles the addition of a new book.
    - GET: Renders the add book form with a list of available authors.
    - POST: Validates the form data and adds the book to the database, including image upload.
    """
    if request.method == 'GET':
        authors = Author.query.all()
        return render_template('add_book.html', authors=authors)
    book_schemas = book_schema.BookSchema()
    uploaded_file = request.files.get('isbn')
    try:
        form_data = {
            'title': request.form['title'],
            'author_id': request.form['author_id'],
            'publication_year': request.form['publication_year'],
            'isbn': uploaded_file
        }
        data = book_schemas.load(form_data)
        isbn = uploaded_file
        if isbn:
            filename = secure_filename(isbn.filename)
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            isbn.save(image_path)
        else:
            filename = None
        book = Book(
            author_id=data['author_id'],
            title=data['title'],
            isbn=filename,
            publication_year=data['publication_year']
        )
        db.session.add(book)
        db.session.commit()
        flash('Book added successfully!', 'success')
        return redirect(url_for('add_book'))
    except ValidationError as err:
        # If there are validation errors, display them on the form
        for field, error in err.messages.items():
            flash(f"{field}: {', '.join(error)}", 'error')
        return redirect(url_for('add_book'))


@app.route('/', methods=['GET'])
def home_page():
    """
    Displays the home page with a list of books.
    Supports sorting by title or author and searching by book title.
    """
    sort_by = request.args.get('sort_by', 'title')
    query = db.session.query(Book, Author).join(Author)

    # Filter by search term
    search = request.args.get('search')
    if search:
        query = query.filter(Book.title.ilike(f'%{search}%'))
    if sort_by == 'author':
        query = query.order_by(Author.name)
    else:
        query = query.order_by(Book.title)
    books = query.all()

    if not books:
        flash('No books found with that title.', 'warning')
        return render_template('home.html', books=books)
    return render_template('home.html', books=books)


@app.route('/delete_book/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    """
    Deletes a book by its ID.
    Returns a JSON response indicating success or failure.
    """
    book = Book.query.get(book_id)
    if book:
        db.session.delete(book)
        db.session.commit()
        flash('Book deleted successfully!', 'success')
        return jsonify({'message': 'Book deleted successfully!'}), 200
    else:
        flash('Book not found!', 'error')
        return jsonify({'message': 'Book not found!'}), 404


@app.route('/book/<int:book_id>', methods=['GET'])
def show_book(book_id):
    """
    Displays the details of a specific book by its ID.
    """
    book = Book.query.get_or_404(book_id)
    author = Author.query.get(book.author_id)
    return render_template('show_book.html', book=book, author=author)


@app.route('/author/<int:author_id>/delete', methods=['DELETE'])
def delete_author(author_id):
    """
    Deletes an author by their ID, along with all books related to that author.
    Returns a JSON response indicating success or failure.
    """
    author = Author.query.get_or_404(author_id)
    try:
        db.session.delete(author)  # This will also delete all related books
        db.session.commit()
        flash(f"Author {author.name} and all their books have been deleted.", "success")
        return jsonify({'message': "Author deleted successfully!"}), 200
    except Exception as e:
        db.session.rollback()
        flash(f"Error deleting author: {e}", "error")
        return jsonify({'message': "Error deleting author"}), 404


if __name__ == '__main__':
    app.run(debug=True)
