# propertiesdatabase.py
import sqlite3
import pandas as pd

class PropertyDatabase:
    def __init__(self, db_name):
        """Initialize the database connection."""
        self.conn = sqlite3.connect(db_name)
        self.table = "propertiesv1"
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        """Create the properties table if it doesn't already exist."""
        query = """
        CREATE TABLE IF NOT EXISTS {} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            type TEXT CHECK(type IN ('shop', 'office', 'kiosk', 'flat', 'house', 'plot')),
            address TEXT,
            size REAL,
            price REAL,
            rent REAL,
            city TEXT,
            url TEXT
        );
        """.format(self.table)
        self.cursor.execute(query)
        self.conn.commit()

    def insert_property(self, prop_type, address,size, price, rent, city,url):
        """Insert a new property into the properties table."""
        query = f"""
        INSERT INTO {self.table} (type, address,size, price, rent, city,url)
        VALUES (?, ?, ?, ?, ?, ?, ?);
        """
        self.cursor.execute(query, (prop_type, address,size, price, rent, city,url))
        self.conn.commit()

    def get_propertiesDF(self):
        """Retrieve all properties from the properties table."""
        query = f"SELECT * FROM {self.table};"
        df = pd.read_sql_query(query, self.conn)
        return df;

    def close(self):
        """Close the database connection."""
        self.conn.close()
