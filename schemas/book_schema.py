from marshmallow import Schema, fields, validate, validates, ValidationError
from schemas.image_field_schema import ImageFileField
from data_models import Author


class BookSchema(Schema):
    """
    Schema for validating and serializing/deserializing Book data.

    Attributes:
        title (str): The title of the book, required and cannot be empty.
        isbn (str): The ISBN of the book, optional and can be None.
        publication_year (int): The publication year of the book, required.
        author_id (int): The ID of the author of the book, required.
    """

    title = fields.String(required=True, validate=validate.Length(min=1))
    isbn = ImageFileField(required=False, allow_none=True)
    publication_year = fields.Integer(required=True)
    author_id = fields.Integer(required=True)

    @validates('author_id')
    def validate_author_id(self, author_id):
        """
        Validate the author ID to ensure it corresponds to an existing author.

        Args:
            author_id (int): The ID of the author to validate.

        Raises:
            ValidationError: If the author ID does not correspond to a valid author.
        """
        author = Author.query.get(author_id)
        if not author:
            raise ValidationError('Invalid author ID.')

    @validates('publication_year')
    def validate_publication_year(self, year):
        """
        Validate the publication year to ensure it falls within a reasonable range.

        Args:
            year (int): The publication year to validate.

        Raises:
            ValidationError: If the publication year is not between 1900 and 2100.
        """
        if year < 1900 or year > 2100:  # Example validation for reasonable year range
            raise ValidationError('Publication year must be between 1900 and 2100.')
