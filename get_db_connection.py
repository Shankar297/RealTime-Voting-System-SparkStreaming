import psycopg2
def connect_to_db():
    conn = None
    cur = None
    try:
        conn = psycopg2.connect(    host="localhost",        # Connect to the local machine where Docker is running
                                        port="5433",             # PostgreSQL port from your Docker Compose file
                                        database="votingdb",     # Database name specified in the Docker Compose
                                        user="postgres",         # User specified in the Docker Compose
                                        password="postgres"      # Password specified in the Docker Compose
                                )
        cur = conn.cursor()
    except Exception as e:
        print(f"ERROR: Getting Error {str(e)}")

    return conn, cur