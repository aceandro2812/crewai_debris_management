from fastapi import FastAPI, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from database import engine, get_db
from models import schemas
from crews.debris_management_crew import DebrisManagementCrew
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

# Create database tables
schemas.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Construction Site Debris Management")

# Configure templates
templates = Jinja2Templates(directory="templates")

@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/materials/", response_model=schemas.Material)
def create_material(material: schemas.MaterialCreate, db: Session = Depends(get_db)):
    db_material = schemas.ConstructionMaterial(**material.dict())
    db.add(db_material)
    db.commit()
    db.refresh(db_material)
    return db_material

@app.post("/debris/analyze/")
async def analyze_debris(debris: schemas.DebrisCreate, db: Session = Depends(get_db)):
    # Get all materials from database
    materials = db.query(schemas.ConstructionMaterial).all()
    materials_data = [{"name": m.material_name, "weight": m.weight} for m in materials]
    
    # Create crew and analyze debris
    crew = DebrisManagementCrew()
    analysis_result = crew.analyze_debris(materials_data, debris.weight)
    
    # Save debris record
    db_debris = schemas.Debris(weight=debris.weight)
    db.add(db_debris)
    db.commit()
    
    return {"analysis": analysis_result}

@app.get("/materials/", response_model=list[schemas.Material])
def get_materials(db: Session = Depends(get_db)):
    return db.query(schemas.ConstructionMaterial).all()