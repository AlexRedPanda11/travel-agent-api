import os
from fastapi import FastAPI
from duffel_api import Duffel

app = FastAPI()

@app.get("/")
def read_root():
    return {"status": "Server is running"}

@app.get("/quote")
def get_quote(origin: str, destination: str, date: str):
    access_token = os.environ.get("DUFFEL_ACCESS_TOKEN")
    if not access_token:
        return {"error": "Missing Duffel access token"}
        
    client = Duffel(access_token=access_token)
    
    try:
        offer_request = client.offer_requests.create() \
            .passengers([{"type": "adult"}]) \
            .slices([{"origin": origin, "destination": destination, "departure_date": date}]) \
            .return_offers() \
            .execute()
            
        offers = offer_request.offers
        if not offers:
            return {"message": "No flights found"}
            
        first_offer = offers[0]
        wholesale_price = float(first_offer.total_amount)
        airline = first_offer.owner.name
        
        markup_percentage = 0.10
        retail_markup = wholesale_price * markup_percentage
        final_retail_price = wholesale_price + retail_markup
        
        return {
            "airline": airline,
            "wholesale_cost": f"${wholesale_price:.2f}",
            "retail_markup": f"${retail_markup:.2f}",
            "final_price_to_client": f"${final_retail_price:.2f}"
        }
        
    except Exception as error:
        return {"error": str(error)}
