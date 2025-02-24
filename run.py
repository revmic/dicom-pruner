import psycopg2
import json

def replace_inlinebinary(json_data):
    if isinstance(json_data, dict):
        for key, value in json_data.items():
            if isinstance(value, dict) and "InlineBinary" in value:
                value["InlineBinary"] = "REMOVED"
            else:
                replace_inlinebinary(value)
    elif isinstance(json_data, list):
        for item in json_data:
            replace_inlinebinary(item)

def update_database():
    conn = psycopg2.connect(
        dbname="db",
        user="root",
        password="secret",
        host="localhost",
        port="54321"
    )
    cursor = conn.cursor()
    
    # Fetch all records
    cursor.execute("SELECT id, data FROM dicom_metadata ORDER BY id")
    records = cursor.fetchall()
    
    for record in records:
        record_id, data = record
        
        if data:
            # json_data = json.loads(data)
            json_data = data if isinstance(data, dict) else json.loads(data)
            replace_inlinebinary(json_data)
            updated_data = json.dumps(json_data)
            
            cursor.execute(
                "UPDATE dicom_metadata SET data = %s WHERE id = %s",
                (updated_data, record_id)
            )
    
    conn.commit()
    cursor.close()
    conn.close()
    
if __name__ == "__main__":
    update_database()
