from flask import Flask
from models.book_model import BookModel
from flask_cors import CORS
from services.book_services import BookService
from routes.book_routes import BookRoutes
from schemas.book_schemas import BookSchema

app = Flask(__name__)
CORS(app)  # This gives permissions to all
# if we want only our front to have access: CORS(app,)

# Model
db_conn = BookModel()
db_conn.connect_to_database()

# Service:
book_service = BookService(db_conn)

# Schema:
book_schema = BookSchema()

# Routes:
book_routes = BookRoutes(book_service, book_schema)

# App:
app.register_blueprint(book_routes)  # We create the routing table

if __name__ == "__main__":
    try:
        app.run(debug=True)
    finally:
        db_conn.close_connection()
