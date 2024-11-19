from marshmallow import fields, validates, ValidationError

class BookSchema:
    #In this case we wont create a constructor (__init__)
    #Well define the properties inside of the class directly
    #Because marshmallow validations work this wa

    title = fields.String(required=True) #We can define the type of the field.
                                        # With required we can define that the field is mandatory
    author = fields.String(required=True)
    year = fields.String(required=True)
    edition = fields.String(required=True)

    #Well use a new decorator to validate field by field
    @validates('title')
    def validate_title(self, value):
        if len(value) < 5:
            raise ValidationError('Title must be at least 5 characters long')
            #This ValidationError will break the request and return a 400 status code, we need to handle it in the routes
        

    @validates('author')
    def validate_author(self, value):
        if len(value) < 5:
            raise ValidationError('Author must be at least 5 characters long')
        
    @validates('year')
    def validate_year(self, value):
        if len(value) <= 3:
            raise ValidationError('Year must be at least 4 characters long')
        
    @validates('edition')
    def validate_edition(self, value):
        if len(value) < 5:
            raise ValidationError('Author must be at least 5 characters long')
        
if __name__ == '__main__':
    from logger.logger_base import Logger
    logger = Logger()
    schema = BookSchema()
    schema.validate_title('Title 5')
    try:
        schema.validate_author('Au')
    except ValidationError as e:
        logger.error(f'An error has ocurred: {e}')
    schema.validate_year('2023')
    schema.validate_edition('Edition 5')