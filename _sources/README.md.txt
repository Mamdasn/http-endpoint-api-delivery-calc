# Delivery Fee Calculator FastAPI App

## Brief Description
This FastAPI application provides an API for calculating delivery fees based on various factors such as cart value, delivery distance, number of items, and time.

## Usage
The application exposes an endpoint (`/delivery_fee`) that accepts POST requests with JSON payload containing delivery information. It returns the calculated delivery fee.

### Endpoint
- POST `/delivery_fee`: Accepts a JSON object with `cart_value`, `delivery_distance`, `number_of_items`, and `time`. Returns the calculated delivery fee.

### Response status codes
- `200`: Successful Response
- `400`: Bad Request
- `422`: Validation Error

### Example Query
Example sent query to `/delivery_fee`:
```Python
{
    "cart_value": 890,
    "delivery_distance": 1,
    "number_of_items": 1,
    "time": "2024-01-15T13:00:00Z",
}
```
`/delivery_fee`'s response:
```Python
{
    "delivery_fee": 310
}
```

## Instructions

### Prerequisites
- Python 3.8+
- Other dependencies in `requirements.txt`

### Setup and Running Locally
1. Clone the repository.
2. Install dependencies: `pip install -r requirements.txt`.
3. Run the application: `uvicorn --workers 1 --host 0.0.0.0 --port 5000 api_app:app`.

### Docker Usage
Alternatively, you can build and run this app using Docker:

1. Build the Docker image: `docker build -t delivery-fee-calculator .`
2. Run the Docker container: `docker run -p 5000:5000 delivery-fee-calculator`

## Tests
The `tests` directory contains unit tests for the delivery fee calculation logic, and the endpoint response.

### Running Tests
Run the tests using the following command:
```Python
python -m unittest discover -s tests -v
```
The implemented tests can also be executed using the `pytest` testing tool.

This will execute various test cases defined in `test_delivery_fee.py` and `test_delivery_fee_http_api.py`, evaluating the logic of the delivery fee calculations and the http endpoint responses under different scenarios.

## Documentation
Documentation built by `sphinx`: [Docs](https://mamdasn.github.io/http-endpoint-api-delivery-calc/)
