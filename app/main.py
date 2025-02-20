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

app = FastAPI(
    title="Construction Site Debris Management",
    debug=True  # Enable debug mode for detailed error information
)

# Configure CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
    try:
        # Get all materials from database
        materials = db.query(schemas.ConstructionMaterial).all()
        if not materials:
            raise HTTPException(status_code=400, detail="No construction materials found in database")
            
        materials_data = [{"name": m.material_name, "weight": m.weight} for m in materials]
        
        # Create crew and analyze debris
        crew = DebrisManagementCrew()
        analysis_result = crew.analyze_debris(materials_data, float(debris.weight))
        
        if not analysis_result:
            raise HTTPException(status_code=500, detail="Failed to generate analysis results")
        
        # Save debris record using the SQLAlchemy model
        db_debris = schemas.DebrisModel(weight=debris.weight)
        db.add(db_debris)
        db.commit()
        db.refresh(db_debris)
        
        return {"analysis": analysis_result}
    except ValueError as ve:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        print(f"Error in analyze_debris: {str(e)}")
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/materials/", response_model=list[schemas.Material])
def get_materials(db: Session = Depends(get_db)):
    return db.query(schemas.ConstructionMaterial).all()