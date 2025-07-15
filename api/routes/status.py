from fastapi import APIRouter, HTTPException
from pymongo import MongoClient
from bson.json_util import dumps
import json

router = APIRouter()

# Securely load credentials (e.g., via environment variables in real systems)
db = client["smart_transport"]

@router.get("/get-all-components")
def get_all():
    data = list(db.components.find({}, {"_id": 0, "component_id": 1, "vehicle_id": 1}))
    return data

@router.get("/get-component-status/{component_id}")
def get_status(component_id: str):
    component = db.components.find_one({"component_id": component_id})
    
    if not component:
        raise HTTPException(status_code=404, detail="Component not found")

    # Remove internal MongoDB ID for cleaner API response
    component.pop("_id", None)

    return component
