from flask import Flask, request, jsonify
from flask_cors import CORS
import snell_model as sm

app = Flask(__name__)
CORS(app)

@app.route("/predict", methods=["POST"])
def predict():
    data = request.json
    date = data["date"]
    time = data["time"]
    density = sm.predict_density(date, time)
    return jsonify({"density": density})

if __name__ == "__main__":
    app.run(debug=True)