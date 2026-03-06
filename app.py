from flask import Flask, render_template
import monitoring

app = Flask(__name__)

@app.route("/")
def index():
    resultats = monitoring.get_resultats()
    return render_template("index.html", resultats=resultats)

from flask import Flask, render_template, jsonify

@app.route("/api/statuts")
def api_statuts():
    resultats = monitoring.get_resultats()
    return jsonify(resultats)

if __name__ == "__main__":
    app.run(debug=True)