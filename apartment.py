from pydantic import BaseModel

class Apartment(BaseModel):
    livingSpace : float
    noRooms : float
    additionCost : float
    heating_type : str
    condition : str
    typeOfFlat : str
    regio2 : str