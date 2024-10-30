from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from chat import get_response
 
app = Flask(__name__)
CORS(app)


@app.post("/predict")
def predict():
    try:
        text = request.get_json().get("message")
        # Check if the text is valid
        if not text:
            return jsonify({"answer": "Invalid input."}), 400
        response = get_response(text)
        message = {"answer": response}
        return jsonify(message)
    except Exception as e:
        return jsonify({"answer": "An error occurred: {}".format(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
