from marshmallow import ValidationError
from marshmallow.fields import Field


class ImageFileField(Field):
    """
    Custom field for validating image file uploads in Marshmallow schemas.

    This field checks for the presence of a file and validates its type to ensure
    that only allowed image formats (JPEG, PNG, and GIF) are accepted.

    Methods:
        _deserialize(value, attr, data, **kwargs): Deserialize the input value and validate
            that it is a valid image file.
    """

    def _deserialize(self, value, attr, data, **kwargs):
        """
        Deserialize and validate the uploaded image file.

        Args:
            value: The uploaded file to validate.
            attr: The attribute name of the field in the input data.
            data: The complete input data being processed.

        Returns:
            The validated file object if successful; None if no file is uploaded.

        Raises:
            ValidationError: If no file is uploaded or if the file type is invalid.
        """
        if not value:
            return None
        if not value.filename:
            raise ValidationError("No file uploaded.")
        if not value.filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
            raise ValidationError("Invalid image file type. Only JPEG, PNG, and GIF are allowed.")

        return value
