from marshmallow import Schema, fields, validate, pre_load


class AuthorSchema(Schema):
    """
    Schema for validating and serializing/deserializing Author data.

    Attributes:
        name (str): The name of the author, required and cannot be empty.
        birthdate (date): The birth date of the author, required.
        date_of_death (date): The date of death of the author, optional.
    """

    name = fields.String(required=True, validate=validate.Length(min=1))
    birthdate = fields.Date(required=True)
    date_of_death = fields.Date(allow_none=True)

    @pre_load
    def process_empty_strings(self, data, **kwargs):
        """
        Preprocessing step that converts empty strings to None for date_of_death field.

        Args:
            data (dict): The input data being validated.
            **kwargs: Additional arguments.

        Returns:
            dict: The processed data with empty strings replaced by None.
        """
        for field in ['date_of_death']:
            if field in data and data[field] == '':
                data[field] = None
        return data
