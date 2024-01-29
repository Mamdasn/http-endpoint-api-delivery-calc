from datetime import datetime

import uvicorn
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel, field_validator

from delivery_tools import delivery_fee_calculator

app = FastAPI()


class DeliveryRequest(BaseModel):
    """
    Evaluates the delivery data by checking the presence and type
    of required fields.
    This function examines the provided `data` dictionary to ensure
    it contains all necessary keys: `cart_value`,
    `delivery_distance`, `number_of_items`, and `time`.
    Additionally, it checks that `cart_value`, `delivery_distance`,
    and `number_of_items` are integers, and `time` is a string and
    is convertable to utc datatime.
    It doesnt raise an error if all the data needed is provided and
    follow the criteria mentioned above.
    """

    cart_value: int
    delivery_distance: int
    number_of_items: int
    time: str

    @field_validator("time")
    def validate_time_format(cls, time):
        try:
            datetime.fromisoformat(time.replace("Z", "+00:00"))
            return time
        except ValueError:
            raise ValueError("Time must be a valid ISO format string")


class DeliveryResponse(BaseModel):
    """
    Evaluates the response of the delivery fee calculator by checking
    data type the of `delivery_fee` field.
    If the value for `delivery_fee` in the response is an integer,
    it does not return an error.
    """

    delivery_fee: int


@app.post("/delivery_fee")
async def get_delivery_fee(data: DeliveryRequest):
    try:
        delivery_fee = delivery_fee_calculator(data.dict())
        DeliveryResponse(delivery_fee=delivery_fee.get("delivery_fee"))
        return delivery_fee
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.exception_handler(ValueError)
async def validation_exception_handler(request: Request, exc: ValueError):
    return JSONResponse(status_code=400, content={"message": f"Error: {exc}"})


if __name__ == "__main__":
    uvicorn.run("api_app:app", host="0.0.0.0", port=5000, reload=True)
