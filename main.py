from fastapi import FastAPI
import util
from apartment import Apartment
import pickle
import math

app = FastAPI()
input_pickle = open("./german_apartment_rent_prices_XGBoost_model.pickle","rb")
classifier=pickle.load(input_pickle)

@app.get('/')
def index():
    return {'message': 'Welcome to German Apartment Rent server. Created in April 2024 by Marsetio Noorprajuda'}

@app.post('/predict')
def predict_apartment_price(data:Apartment):
    data = data.dict()
    livingSpace = float(data['livingSpace'])
    noRooms = float(data['noRooms'])
    additionCost = float(data['additionCost'])

    heating_type = str(data['heating_type'])
    condition = str(data['condition'])
    typeOfFlat = str(data['typeOfFlat'])
    regio2 = str(data['regio2'])   
    
    estimated_price = util.get_estimated_price(livingSpace,noRooms,additionCost,heating_type,condition,typeOfFlat,regio2)
    estimated_price =  math.ceil(estimated_price*100)/100
    
    return {
        'estimated_price': estimated_price
    }