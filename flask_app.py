from flask import Flask, jsonify, request

from delivery_tools import delivery_data_integrity_check, delivery_fee_calculator

app = Flask(__name__)


@app.route("/", methods=["POST"])
def get_data():
    data = request.get_json(force=True)
    if not delivery_data_integrity_check(data):
        return (
            jsonify(
                {
                    "Error": "Incorrect input. Your data query should \
                     have the following fields: \
                     cart_value, delivery_distance, number_of_items and time"
                }
            ),
            400,
        )
    delivery_fee = delivery_fee_calculator(data)
    return jsonify(delivery_fee)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
