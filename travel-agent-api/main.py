```python
import os
from fastapi import FastAPI
from amadeus import Client, ResponseError

app = FastAPI()

@app.get("/")
def read_root():
    return {"status": "Server is running"}

@app.get("/quote")
def get_quote(origin: str, destination: str, date: str):
    client_id = os.environ.get("AMADEUS_CLIENT_ID")
    client_secret = os.environ.get("AMADEUS_CLIENT_SECRET")
   
    amadeus = Client(client_id=client_id, client_secret=client_secret)
   
    try:
        response = amadeus.shopping.flight_offers_search.get(
            originLocationCode=origin,
            destinationLocationCode=destination,
            departureDate=date,
            adults=1
        )
       
        if not response.data:
            return {"message": "No flights found"}
       
        first_flight = response.data[0]
        wholesale_price = float(first_flight["price"]["total"])
        airline = first_flight["itineraries"][0]["segments"][0]["carrierCode"]
       
        markup_percentage = 0.10
        retail_markup = wholesale_price * markup_percentage
        final_retail_price = wholesale_price + retail_markup
       
        return {
            "airline": airline,
            "wholesale_cost": f"${wholesale_price:.2f}",
            "retail_markup": f"${retail_markup:.2f}",
            "final_price_to_client": f"${final_retail_price:.2f}"
        }
       
    except ResponseError as error:
        return {"error": str(error)}

```
