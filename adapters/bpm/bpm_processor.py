from fastapi import APIRouter, HTTPException
from ports.bpm import BPMProcessor
from schemas.edge import BPMRequest

router = APIRouter()

# Instanciamos el procesador de BPM
bpm_processor = BPMProcessor()


# Endpoint para recibir los datos BPM y procesarlos
@router.post("/edge/bpm")
async def process_bpm_data(data: BPMRequest):
    try:
        result = await bpm_processor.process_bpm(data)
        return {"message": "BPM processed successfully", "data": result}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")


# Endpoint para obtener todos los datos BPM procesados
@router.get("/edge/bpm/data")
async def get_bpm_data():
    try:
        data = bpm_processor.get_processed_bpm_data()
        return {"message": "Processed BPM data", "data": data}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error retrieving data")
