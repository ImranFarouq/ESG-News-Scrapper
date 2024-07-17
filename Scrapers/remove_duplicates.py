import MySQLdb

# MySQL connection details
db = MySQLdb.connect(host='13.201.128.161', user='test', passwd='test@123', db='mysql')
cursor = db.cursor()

# Check if esg_news table exists
check_table_query = "SHOW TABLES LIKE 'esg_news'"
cursor.execute(check_table_query)
table_exists = cursor.fetchone()

if table_exists:
    print("Table 'esg_news' already exists.")
else:
    # Create table if it does not exist
    create_table_query = '''
        CREATE TABLE esg_news (
            Title VARCHAR(255),
            Description TEXT,
            Date DATE,
            Link VARCHAR(255),
            Image_URL VARCHAR(255),
            Source VARCHAR(255)
        )
    '''
    cursor.execute(create_table_query)
    print("Table 'esg_news' created.")

# Create temporary table to store unique records
temp_table_name = 'esg_news_temp'

try:
    # Drop temporary table if it exists
    cursor.execute(f"DROP TABLE IF EXISTS {temp_table_name}")

    # Create temporary table with the same structure as the original table
    cursor.execute(f"CREATE TABLE {temp_table_name} LIKE esg_news")

    # Insert distinct rows into the temporary table
    insert_temp_query = '''
        INSERT INTO esg_news_temp (Title, Description, Date, Link, Image_URL, Source)
        SELECT DISTINCT Title, Description, Date, Link, Image_URL, Source
        FROM esg_news
    '''
    cursor.execute(insert_temp_query)

    # Drop the original table
    cursor.execute('DROP TABLE esg_news')

    # Rename the temporary table to the original table name
    cursor.execute(f"RENAME TABLE {temp_table_name} TO esg_news")

    # Commit changes
    db.commit()
    print("Duplicates removed and updated table created.")

except Exception as e:
    print(f"Error removing duplicates: {e}")
    db.rollback()  # Rollback in case of error

finally:
    # Close connection
    cursor.close()
    db.close()

