import json

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Literal
from app.client import get_producer

app = FastAPI()
producer = get_producer()

class RiderUpdate(BaseModel):
    name : str
    location : Literal["north", "south"]

@app.post("/riders/location")
def update_location(data: RiderUpdate):
    partition = 0
    
    if data.location == "south":
        partition = 1

    message  = {
       "name": data.name,
        "location" : data.location
    }

    try:
        producer.produce(
            topic= "rider-updates",
            partition=partition,
            key= "location-update",
            value=json.dumps(message)

        )

        remaining = producer.flush(5)

        if remaining > 0:
            raise HTTPException(
                status_code= 503, detail="Server timed out"
            )


        return {
            "message": "Rider update published",
            "partition": partition,
            "data": message
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )