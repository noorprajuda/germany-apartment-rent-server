import json
import pickle
import numpy as np
from fastapi import FastAPI

app = FastAPI()

__heattype = None
__roomcon = None
__flattype = None
__locations = None

__data_columns = None
__model = None

def get_estimated_price(livingSpace: float, noRooms: int, additionCost: float, heating_type: str, condition: str, typeOfFlat: str, regio2: str) -> float:
    global __data_columns
    global __model

    try:
        heatingIndex = __data_columns.index(heating_type.lower())
        conIndex = __data_columns.index(condition.lower())
        flatTypeIndex = __data_columns.index(typeOfFlat.lower())
        regionIndex = __data_columns.index(regio2.lower())
    except ValueError:
        heatingIndex = -1
        conIndex = -1
        flatTypeIndex = -1
        regionIndex = -1

    x = np.zeros(len(__data_columns))
    x[0] = livingSpace
    x[1] = noRooms
    x[2] = additionCost

    if heatingIndex >= 0:
        x[heatingIndex] = 1
    if conIndex >= 0:
        x[conIndex] = 1
    if flatTypeIndex >= 0:
        x[flatTypeIndex] = 1
    if regionIndex >= 0:
        x[regionIndex] = 1

    return float(__model.predict([x])[0])  # Convert to Python float

def get_heattype_names():
    global __heattype
    return __heattype

def get_roomcon_names():
    global __roomcon
    return __roomcon

def get_flattype_names():
    global __flattype
    return __flattype

def get_location_names():
    global __locations
    return __locations

def load_saved_artifacts():
    global __data_columns
    global __heattype
    global __roomcon
    global __flattype
    global __locations
    global __model

    print("Loading saved artifacts...start")
    with open("./columns.json", 'r') as f:
        __data_columns = json.load(f)['data_columns']
        __heattype = __data_columns[3:13]
        __roomcon = __data_columns[13:21]
        __flattype = __data_columns[21:31]
        __locations = __data_columns[31:]
        print(__heattype)
        print(__roomcon)
        print(__flattype)
        print(__locations)
    with open("./german_apartment_rent_prices_XGBoost_model.pickle", 'rb') as f:
        __model = pickle.load(f)
    print("Loading saved artifacts...done")

load_saved_artifacts()

@app.get("/estimate/")
async def estimate_price(livingSpace: float, noRooms: int, additionCost: float, heating_type: str, condition: str, typeOfFlat: str, regio2: str) -> float:
    return get_estimated_price(livingSpace, noRooms, additionCost, heating_type, condition, typeOfFlat, regio2)
