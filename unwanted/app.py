from flask import Flask, jsonify
import mysql.connector

app = Flask(__name__)

@app.route('/vulnerabilities/<cve_id>')
def get_vulnerability(cve_id):
    # Connect to the MySQL database
    conn = mysql.connector.connect(
        host="localhost",         # Replace with your MySQL host
        user="root",          # Replace with your MySQL username
        password="Aasath@7862",      # Replace with your MySQL password
        database="usnvd"         # Replace with your MySQL database name
    )
    cursor = conn.cursor()

    # Query to fetch the vulnerability
    cursor.execute("SELECT * FROM vulnerabilities WHERE id = %s", (cve_id,))
    vulnerability = cursor.fetchone()

    # Close the connection
    conn.close()

    # Check if the vulnerability exists
    if not vulnerability:
        return jsonify({"error": "Vulnerability not found"}), 404

    # Return the vulnerability details as JSON
    return jsonify({
        "id": vulnerability[0],
        "description": vulnerability[1],
        "severity": vulnerability[2],
        "published_date": vulnerability[3].strftime('%Y-%m-%d %H:%M:%S') if vulnerability[3] else None,
        "last_modified_date": vulnerability[4].strftime('%Y-%m-%d %H:%M:%S') if vulnerability[4] else None
    })

if __name__ == '__main__':
    app.run(debug=True)
