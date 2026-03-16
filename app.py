from flask import Flask, render_template, jsonify
import monitoring
import sqlite3

app = Flask(__name__)

@app.route("/")
def index():
    resultats = monitoring.get_resultats()
    return render_template("index.html", resultats=resultats)

@app.route("/api/statuts")
def api_statuts():
    resultats = monitoring.get_resultats()
    return jsonify(resultats)

@app.route("/api/historique")
def api_historique():
    conn = sqlite3.connect("historique.db")
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute("""
        SELECT nom, ip, statut, timestamp
        FROM pings
        WHERE timestamp >= datetime('now', '-24 hours')
        ORDER BY timestamp DESC
    """)
    rows = [dict(row) for row in c.fetchall()]
    conn.close()
    return jsonify(rows)

if __name__ == "__main__":
    app.run(debug=True)