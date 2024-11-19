from flask import Blueprint, jsonify, request
from marshmallow import ValidationError #We import ValidationError because we'll treat the exception in the routes
from logger.logger_base import Logger

# We heredate from Blueprint. we put it as an argument to BookRoutes
class BookRoutes(Blueprint):
    def __init__(self, book_service, book_schema):
        super().__init__(
            "book", __name__
        )  # we initialize the methods of the father. we give the routing table a name of 'books'
        self.book_service = book_service
        self.book_schema = book_schema
        self.register_routes()
        self.logger = Logger()

    # this method will allow us to define our routes
    def register_routes(self):
        # we map the /api/v1/books to the get_books method that will answer the route
        self.route("/api/v1/books", methods=["GET"])(self.get_books)
        # we map the /api/v1/books POST to the add_books method that will answer the route
        self.route('/api/v1/books', methods=["POST"])(self.add_books)
        self.route('/api/v1/books/<int:book_id>', methods=["PUT"])(self.update_book) #With <int:book_id> we tell our API it will receive a query parameter of type int called book_id
        self.route('/api/v1/books/<int:book_id>', methods=["DELETE"])(self.delete_book)

    def get_books(self):
        books = (
            self.book_service.get_all_book()
        )  # We get all the books using our service
        return jsonify(books), 200  # We return the books and the HTTP 200 Code
    

    def fetch_request_data(self):
        try:
            request_data = request.json #We get the data from the request

            #We need to validate if there is data in the request
            if not request_data:
                return jsonify({'error': 'Invalid data'}), 400 #We return 400 because its the client's fault
            
            #Were going to decompose the data incoming from the JSON to all the fields in the schema
            title = request_data.get('title')
            author = request_data.get('author')
            year = request_data.get('year')
            edition = request_data.get('edition')

            return title, author, year, edition
        except Exception as e:
            self.logger.error(f'Error fetching the request data: {e}')
            return jsonify({'error': f'Error fetching the request data: {e}'}), 500
    
    def add_books(self):
        try:
            # We call the fetch_request_data method to get the data from the request
            title, author, year, edition = self.fetch_request_data()

            #Now we actually call the validation methods from the schema
            try:
                self.book_schema.validate_title(title)
                self.book_schema.validate_author(author)
                self.book_schema.validate_year(year)
                self.book_schema.validate_edition(edition)
            except ValidationError as e:
                return jsonify({'error': f'Invalid data: {e}', 'details': f'{e}', 'error_code': 'ERROR_INVALID_DATA'}), 400
            
            #Once weve validated the data, and its correct, we'll rebuild the request
            #We do this because in the request recived there could be more data than we need
            #So with this we make sure that only the verified data is sent to the service (DB)
            new_book = {
                'title': title,
                'author': author,
                'year': year,
                'edition': edition
            }

            #We call the service to add the book to the DB
            created_book = self.book_service.add_book(new_book)
            self.logger.info(f'New book created: {created_book}')

            #From our API the response will be the book created in JSON
            return jsonify(created_book), 201 #We use 201 because we created a new resource

        except Exception as e:
            self.logger.error(f'Error adding a new book to the database: {e}')
            return jsonify({'error': f'Error adding a new book to the database: {e}'}), 500
        
    
    def update_book(self, book_id):
        try:
            # We call the fetch_request_data method to get the data from the request
            title, author, year, edition = self.fetch_request_data()

            #Now we actually call the validation methods from the schema
            try:
                self.book_schema.validate_title(title)
                self.book_schema.validate_author(author)
                self.book_schema.validate_year(year)
                self.book_schema.validate_edition(edition)
            except ValidationError as e:
                return jsonify({'error': f'Invalid data: {e}', 'details': f'{e}', 'error_code': 'ERROR_INVALID_DATA'}), 400
            
            #Once weve validated the data, and its correct, we'll rebuild the request
            #We do this because in the request recived there could be more data than we need
            #So with this we make sure that only the verified data is sent to the service (DB)
            update_book = {
                '_id': book_id, #Unlike the CREATE method (_id is created in Mongo), we need to send the _id, because were replacing the book 
                'title': title,
                'author': author,
                'year': year,
                'edition': edition
            }

            #We call the service to update the book to the DB
            updated_book = self.book_service.update_book(book_id, update_book)
            if updated_book:
                return jsonify(update_book), 200 #We return the book we updated not updated_book because it returns a mongo object
            else:
                return jsonify({'error': 'Book not found'}), 404

        except Exception as e:
            self.logger.error(f'Error updating the book in the database: {e}')
            return jsonify({'error': f'Error updating the book in the database: {e}'}), 500
        
    def delete_book(self, book_id):
        try:
            deleted_book = self.book_service.delete_book(book_id)
            if deleted_book:
                return jsonify(deleted_book), 200
            else:
                return jsonify({'error': 'Book not found'}), 404
        except Exception as e:
            self.logger.error(f'Error deleting the book in the database: {e}')
            return jsonify({'error': f'Error deleting the book in the database: {e}'}), 500


    # In service we do the DB connection and return an array
    # In here we only call our service, and return a json and a code
