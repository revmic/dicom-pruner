import argparse
import json
import psycopg2
from psycopg2.extras import Json

parser = argparse.ArgumentParser(description="Populate PostgreSQL dicom_metadata table from an NDJSON file.")
parser.add_argument("ndjson_file", help="Path to the NDJSON file")
args = parser.parse_args()

def connect_db():
    return psycopg2.connect(
        dbname="db",
        user="root",
        password="secret",
        host="localhost",
        port="54321"
    )

def insert_data(conn, ndjson_file):
    with open(ndjson_file, 'r') as f, conn.cursor() as cur:
        for line in f:
            json_obj = json.loads(line)
            cur.execute("INSERT INTO dicom_metadata (data) VALUES (%s)", (Json(json_obj),))
        conn.commit()

def main():
    conn = connect_db()
    try:
        insert_data(conn, args.ndjson_file)
    finally:
        conn.close()

if __name__ == "__main__":
    main()
