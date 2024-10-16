from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Author(db.Model):
    """
    Represents an author in the library system.

    Attributes:
        id (int): The primary key of the author.
        name (str): The name of the author.
        birth_date (date): The birth date of the author (optional).
        date_of_death (date): The date of death of the author (optional).
        books (list): A list of books associated with the author.
    """

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    birth_date = db.Column(db.Date, nullable=True)
    date_of_death = db.Column(db.Date, nullable=True)
    books = db.relationship('Book', backref='author', cascade="all, delete-orphan")

    def __repr__(self):
        """
        Returns a string representation of the Author instance for debugging purposes.

        Returns:
            str: The representation of the author object.
        """
        return f"<Author(id={self.id}, name='{self.name}')>"

    def __str__(self):
        """
        Returns a human-readable string representation of the Author instance.

        Returns:
            str: A string with the author's name.
        """
        return f"Author: {self.name}"


class Book(db.Model):
    """
    Represents a book in the library system.

    Attributes:
        id (int): The primary key of the book.
        author_id (int): Foreign key linking to the Author.
        title (str): The title of the book.
        isbn (str): The ISBN of the book (optional).
        publication_year (int): The year the book was published.
    """

    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey(Author.id))
    title = db.Column(db.String, nullable=False)
    isbn = db.Column(db.String, nullable=True)
    publication_year = db.Column(db.Integer)

    def __repr__(self):
        """
        Returns a string representation of the Book instance for debugging purposes.

        Returns:
            str: The representation of the book object.
        """
        return f"<Book(id={self.id}, title='{self.title}', author_id={self.author_id})>"

    def __str__(self):
        """
        Returns a human-readable string representation of the Book instance.

        Returns:
            str: A string with the book's title and author ID.
        """
        return f"Book: {self.title} by Author ID: {self.author_id}"
