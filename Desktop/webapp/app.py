#from flask import Flask

# 1. This creates the store application
#app = Flask(__name__)

# 2. This is what happens when a customer visits the main page
#@app.route('/')
#def home():
    # The message the customer sees!
   # return "<h1>Welcome to the Spandana Magical Toy Store!</h1>"

# 3. This opens the store's hidden internal door (8000) for business
#if __name__ == '__main__':
   # app.run(debug=True, host='0.0.0.0', port=8000)#
from flask import Flask
# These new tools are for talking to the database
from sqlalchemy import create_engine, text
import time
import psycopg2 

# Create the store application
app = Flask(__name__)

# This is the secret address for the Inventory Book (Database container)
# It uses the name 'db' because that's what we called the service in docker-compose.yml
DB_URL = "postgresql+psycopg2://spandana:mysecretpassword@db/toys_db"

def connect_to_db():
    """Tries to connect to the database with a waiting period."""
    attempts = 0
    # Try to connect up to 5 times, as the database takes a moment to start
    while attempts < 5:
        try:
            # We use SQLAlchemy to manage the connection
            engine = create_engine(DB_URL)
            # Try a simple query to ensure connection is live
            with engine.connect() as connection:
                # The SELECT 1 is like asking the book: "Are you awake?"
                connection.execute(text("SELECT 1"))
                print("Database connection successful!")
                return engine
        except psycopg2.OperationalError as e:
            # This specific error happens if the database isn't fully ready yet
            print(f"Database not ready (Attempt {attempts + 1}). Waiting... Error: {e}")
            time.sleep(3) # Wait 3 seconds before trying again
            attempts += 1
        except Exception as e:
            # Catch all other errors
            print(f"General connection failed (Attempt {attempts + 1}): {e}")
            time.sleep(3) 
            attempts += 1
            
    # If all attempts fail, we raise an error
    raise Exception("Could not connect to the database after multiple attempts.")

# The global database engine variable (starts as empty)
db_engine = None

# This function runs just before the web server starts handling traffic
@app.before_request
def initialize_db():
    global db_engine
    if db_engine is None:
        try:
            db_engine = connect_to_db()
        except Exception as e:
            print(f"Failed to initialize database connection pool: {e}")
            # We don't want the app to crash, so we allow it to start without a connection

# This is what happens when a customer visits the front door (the main page)
@app.route('/')
def home():
    # If the connection failed, we show a friendly message
    if db_engine is None:
        return "<h1>Store is Running...</h1><p>But the Inventory Book is not ready yet! Please wait for the database connection.</p>", 503

    try:
        # A successful greeting that proves the database is connected
        return "<h1>Welcome to the Spandana Magical Toy Store!</h1><p>🥳 **SUCCESS!** The Inventory Book (Database) is connected and ready to track toys.</p>"
    except Exception:
        # If the connection breaks later
        return "<h1>Store is Running...</h1><p>ERROR: Lost connection to the Inventory Book. Check the server logs.</p>", 500

# This makes the store open for business
if __name__ == '__main__':
    # Try to connect to the database before the server starts
    initialize_db() 
    app.run(debug=True, host='0.0.0.0', port=8000)