import sqlite3
import os
import time
import sys

def init_database():
    db_file = 'legal_assistant.db'
    
    # Check if database file exists
    if os.path.exists(db_file):
        try:
            # Try to remove the existing database
            os.remove(db_file)
            print(f"Removed existing database: {db_file}")
        except PermissionError:
            print(f"Cannot remove {db_file} - it's being used by another process.")
            print("Please stop the application before initializing the database.")
            print("Attempting to create a new database with a temporary name...")
            db_file = 'legal_assistant_new.db'
            
            # If the temp file already exists, remove it
            if os.path.exists(db_file):
                try:
                    os.remove(db_file)
                except:
                    print(f"Could not remove temporary file {db_file}")
                    sys.exit(1)
    
    try:
        # Create a new connection to the database
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()
        
        # Open and execute the schema.sql file
        with open('schema.sql', 'r') as f:
            schema_sql = f.read()
            cursor.executescript(schema_sql)
        
        # Commit the changes and close the connection
        conn.commit()
        conn.close()
        
        print(f"Database initialized successfully at: {db_file}")
        
        if db_file != 'legal_assistant.db':
            print("NOTE: A new database was created at:", db_file)
            print("To use this database, you'll need to either:")
            print("1. Rename it to 'legal_assistant.db' after stopping the application, or")
            print("2. Update your application to connect to this new database file.")
        
        return True
    except Exception as e:
        print(f"Error initializing database: {str(e)}")
        return False

if __name__ == "__main__":
    init_database()