from flask import Flask, abort, jsonify, request

from delivery_tools import delivery_fee_calculator, delivery_query_integrity_check

app = Flask(__name__)


@app.before_request
def before_request_func():
    data = request.get_json(silent=True)
    if not data:
        abort(415, description="Invalid json query")
    if not delivery_query_integrity_check(data):
        abort(400, description="Invalid query parameters")


@app.route("/", methods=["POST"])
def get_data():
    data = request.get_json()
    delivery_fee = delivery_fee_calculator(data)
    return jsonify(delivery_fee)


if __name__ == "__main__":
    app.run(debug=True)
