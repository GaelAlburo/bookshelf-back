from flask import jsonify
from logger.logger_base import Logger


# Service has all the logic of the app, all the logic of the API
class BookService:
    def __init__(self, db_conn):
        self.logger = Logger()
        self.db_conn = db_conn

        # We must create the READ, CREATE, UPDATE, DELETE

    # READ all books methods
    def get_all_book(self):

        # Well try to make the connection to the DB
        try:
            books = list(self.db_conn.db.books.find())  # Well cast the result to a list
            # db is the database / books is the name of the collection / find() method from pymongo returns all documents from books
            return books
        except (
            Exception
        ) as e:  # We use our logger to display the error in fetching from DB
            self.logger.error(f"Error fetching all books from the database: {e}")
            return (
                jsonify({"error": f"Error fetching all books from the database: {e}"}),
                500,
            )
    
    def get_book_by_id(self, book_id):
        try:
            book = self.db_conn.db.books.find_one({'_id': book_id})
            return book
        except Exception as e:
            self.logger.error(f'Error fetching the book by id from the database: {e}')
            return jsonify({'error': f'Error fetching the book by id from the database: {e}'}), 500

    # CREATE method
    def add_book(self, new_book):
        try:
            # we calculate the next _id
            max_id = self.db_conn.db.books.find_one(sort=[("_id", -1)])[
                "_id"
            ]  # We do the sort so we can know the last _id of that array
            next_id = max_id + 1
            new_book["_id"] = next_id
            self.db_conn.db.books.insert_one(new_book)
            return new_book
        except Exception as e:
            self.logger.error(f"Error creating the new book: {e}")
            return jsonify({"error": f"Error creating the new book: {e}"}), 500
        
    # UPDATE method
    def update_book(self, book_id, book):
        try:
            update_book = self.get_book_by_id(book_id)
            if update_book:
                updated_book = self.db_conn.db.books.update_one({'_id': book_id}, {'$set': book}) # We use the $set operator to update the book
                if updated_book.modified_count > 0: # modified_count is a property that returns the number of documents modified
                    self.logger.info(f'modified_count: {updated_book.modified_count}')
                    return updated_book
                else: # if modified_count is 0, it means that there was no update made 
                    return 'The book is already up-to-date'
            else: # If the book is not found, we return None
                return None
        except Exception as e:
            self.logger.error(f'Error updating the book: {e}')
            return jsonify({'error': f'Error updating the book: {e}'}), 500
        
    def delete_book(self, book_id):
        try:
            deleted_book = self.get_book_by_id(book_id) # We search for the book to delete

            if deleted_book: # If the book to delete exists, we delete it
                self.db_conn.db.books.delete_one({'_id': book_id})
                return deleted_book # We return the book that was deleted
            else: # If the book to delete does not exist, we return None
                return None
            
        except Exception as e:
            self.logger.error(f'Error deleting the book data: {e}')
            return jsonify({'error': f'Error deleting the book data: {e}'}), 500


if __name__ == "__main__":
    from models.book_model import (
        BookModel,
    )  # We import it here because we only use it for this test, not for the service

    logger = Logger()
    db_conn = BookModel()
    book_service = BookService(db_conn)

    try:
        db_conn.connect_to_database()
        books = book_service.get_all_book()
        logger.info(f"Books fetched: {books}")

        # Add book
        new_book = book_service.add_book(
            {
                "title": "titulo1",
                "author": "Lovecraft",
                "year": "1987",
                "edition": "first",
            }
        )
        logger.info(f"New book added: {new_book}")

        #Get Book by id
        book = book_service.get_book_by_id(3)
        logger.info(f'Book fetched: {book}')

        # Update book
        updated_book = book_service.update_book(2, {'author': 'Stephen King'})
        logger.info(f'Book updated: {updated_book}')

        #Delete book
        deleted_book = book_service.delete_book(9)
        logger.info(f'Book deleted: {deleted_book}')

    except Exception as e:
        logger.error(f"An error has ocurred: {e}")
    finally:
        db_conn.close_connection()
        logger.info("Connection to database was succesfully closed")
