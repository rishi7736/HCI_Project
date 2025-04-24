import sqlite3
import os

# Database setup script
create_tables_script = '''
-- Drop tables if they exist to avoid conflicts
DROP TABLE IF EXISTS form_queries;
DROP TABLE IF EXISTS input_ques;
DROP TABLE IF EXISTS ques_categories;
DROP TABLE IF EXISTS forms;
DROP TABLE IF EXISTS services;

-- Create services table
CREATE TABLE services (
    service_id TEXT PRIMARY KEY,
    service_name TEXT NOT NULL,
    service_description TEXT
);

-- Create forms table
CREATE TABLE forms (
    form_id TEXT PRIMARY KEY,
    form_name TEXT NOT NULL,
    form_description TEXT,
    form_link TEXT NOT NULL,
    service_id TEXT NOT NULL,
    FOREIGN KEY (service_id) REFERENCES services (service_id)
);

-- Create question categories
CREATE TABLE ques_categories (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT
);

-- Create input questions table
CREATE TABLE input_ques (
    ques_id TEXT PRIMARY KEY,
    ques_text TEXT NOT NULL,
    placeholder TEXT,
    category_id TEXT,
    FOREIGN KEY (category_id) REFERENCES ques_categories (id)
);

-- Create form_queries table (mapping between forms and questions)
CREATE TABLE form_queries (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    form_id TEXT NOT NULL,
    form_query_id TEXT NOT NULL,
    FOREIGN KEY (form_id) REFERENCES forms (form_id),
    FOREIGN KEY (form_query_id) REFERENCES input_ques (ques_id)
);
'''

# Sample data script
insert_data_script = '''
-- Insert sample data for services
INSERT INTO services (service_id, service_name, service_description) VALUES
('SVC001', 'Divorce', 'Legal services related to divorce proceedings'),
('SVC002', 'Wills & Testaments', 'Estate planning and will creation services'),
('SVC003', 'Power of Attorney', 'Legal authorization documents'),
('SVC004', 'Business Formation', 'Documents for business creation and management');

-- Insert sample forms
INSERT INTO forms (form_id, form_name, form_description, form_link, service_id) VALUES
('FRM001', 'Divorce Petition', 'Initial petition for divorce filing', 'https://www.courts.ca.gov/documents/fl100.pdf', 'SVC001'),
('FRM002', 'Simple Will', 'Basic last will and testament', 'https://www.courts.gov.bc.ca/supreme_court/practice_and_procedure/will_samples/will_sample_1.pdf', 'SVC002'),
('FRM003', 'Durable Power of Attorney', 'General power of attorney document', 'https://www.courts.ca.gov/documents/gc142.pdf', 'SVC003'),
('FRM004', 'LLC Formation', 'Limited Liability Company formation document', 'https://dos.ny.gov/system/files/documents/2021/02/1336-f.pdf', 'SVC004');

-- Insert question categories
INSERT INTO ques_categories (id, name, description) VALUES
('CAT001', 'Personal Information', 'Basic personal details'),
('CAT002', 'Spouse Information', 'Details about spouse or partner'),
('CAT003', 'Property Information', 'Information about assets and property'),
('CAT004', 'Business Details', 'Information about business entity');

-- Insert sample questions
INSERT INTO input_ques (ques_id, ques_text, placeholder, category_id) VALUES
('Q001', 'Full Name', 'Enter your full legal name', 'CAT001'),
('Q002', 'Date of Birth', 'MM/DD/YYYY', 'CAT001'),
('Q003', 'Address', 'Enter your current residential address', 'CAT001'),
('Q004', 'Spouse Name', 'Enter spouse full legal name', 'CAT002'),
('Q005', 'Property Address', 'Enter property address', 'CAT003'),
('Q006', 'Business Name', 'Enter business name', 'CAT004'),
('Q007', 'Marriage Date', 'MM/DD/YYYY', 'CAT002'),
('Q008', 'Business Type', 'LLC, Corporation, etc.', 'CAT004');

-- Connect forms to questions
INSERT INTO form_queries (form_id, form_query_id) VALUES
('FRM001', 'Q001'), -- Divorce form needs personal info
('FRM001', 'Q002'),
('FRM001', 'Q003'),
('FRM001', 'Q004'),
('FRM001', 'Q007'),
('FRM002', 'Q001'), -- Will needs personal info
('FRM002', 'Q002'),
('FRM002', 'Q003'),
('FRM003', 'Q001'), -- Power of Attorney needs personal info
('FRM003', 'Q002'),
('FRM003', 'Q003'),
('FRM004', 'Q001'), -- LLC Formation needs personal and business info
('FRM004', 'Q003'),
('FRM004', 'Q006'),
('FRM004', 'Q008');
'''

def init_database():
    db_file = 'legal_assistant.db'
    
    # Check if database file exists and try to remove it
    if os.path.exists(db_file):
        try:
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
                except Exception as e:
                    print(f"Could not remove temporary file {db_file}: {str(e)}")
                    return False
    
    try:
        # Create a new connection to the database
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()
        
        print("Creating database tables...")
        cursor.executescript(create_tables_script)
        
        print("Inserting sample data...")
        cursor.executescript(insert_data_script)
        
        # Commit the changes and close the connection
        conn.commit()
        
        # Verify tables were created
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        print(f"Tables created: {[table[0] for table in tables]}")
        
        # Verify services were inserted
        cursor.execute("SELECT COUNT(*) FROM services")
        service_count = cursor.fetchone()[0]
        print(f"Service count: {service_count}")
        
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