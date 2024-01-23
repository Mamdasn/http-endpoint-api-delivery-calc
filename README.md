# Delivery Fee Calculator Flask App

## Brief Description
This Flask application provides an API for calculating delivery fees based on various factors such as cart value, delivery distance, number of items, and time.

## Usage
The application exposes an endpoint (`/`) that accepts POST requests with JSON payload containing delivery information. It returns the calculated delivery fee.

### Endpoints
- POST `/`: Accepts a JSON object with `cart_value`, `delivery_distance`, `number_of_items`, and `time`. Returns the calculated delivery fee.

## Instructions

### Prerequisites
- Python 3.11
- Other dependencies in `requirements.txt`

### Setup and Running Locally
1. Clone the repository.
2. Install dependencies: `pip install -r requirements.txt`.
3. Run the application: `gunicorn --bind 0.0.0.0:5000 wsgi:app`.

### Docker Usage
Alternatively, you can build and run this app using Docker:

1. Build the Docker image: `docker build -t delivery-fee-calculator .`
2. Run the Docker container: `docker run -p 5000:5000 delivery-fee-calculator`

## Tests
The `tests` directory contains unit tests for the delivery fee calculation logic, and the endpoint response.

### Running Tests
Run the tests using the following command:
```Python
python -m unittest discover -s tests
```
This will execute various test cases defined in `test_delivery_fee.py` and `test_delivery_fee_http_api.py`, evaluating the logic of the delivery fee calculations under different scenarios.
