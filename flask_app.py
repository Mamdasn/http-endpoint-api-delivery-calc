from delivery_tools import delivery_data_integrity_check, delivery_fee_calculator
from flask import Flask, jsonify, request

app = Flask(__name__)


@app.route("/", methods=["POST"])
def get_data():
    data = request.get_json(force=True)
    delivery_fee = delivery_fee_calculator(data)
    return jsonify(delivery_fee)


if __name__ == "__main__":
    app.run(debug=True)
