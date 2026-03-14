import requests as req
import json
def extract_data():
    url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum,tether,bnb,xrp,usdc,solana,tron&vs_currencies=usd"
    data=req.get(url).json()
    print("extract completed")
    return data