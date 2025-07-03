from fastapi import APIRouter, HTTPException
from ports.bpm import BPMProcessor
from schemas.edge import BPMRequest
import httpx

router = APIRouter()

# Instanciamos el procesador de BPM
bpm_processor = BPMProcessor()


# Endpoint para recibir los datos BPM y procesarlos
@router.post("/edge/bpm")
async def process_bpm_data(data: BPMRequest):
    try:
        # Procesamos el BPM
        result = await bpm_processor.process_bpm(data)

        # Datos que se enviarán al backend de Spring Boot
        payload = {
            "processed_bpm": result["processed_bpm"],  # El valor procesado de BPM
            "timestamp": result["timestamp"],  # Timestamp del BPM
            "average_bpm": result["average_bpm"],  # Promedio de BPM calculado
            "status": result["status"],  # Estado del BPM (validado, etc.)
            "anomaly_detected": result["anomaly_detected"],  # Si se detectó anomalía
        }

        # URL del backend de Spring Boot
        backend_url = "http://localhost:8080/api/bpm/receive"  # Cambia esto con la URL real de tu backend de Spring Boot

        # Realizar el POST al backend de Spring Boot
        async with httpx.AsyncClient() as client:
            response = await client.post(backend_url, json=payload)
            response.raise_for_status()  # Lanza un error si la respuesta no es exitosa

        return {"message": "BPM processed successfully", "data": result}

    except HTTPException as e:
        raise e
    except httpx.HTTPStatusError as e:
        raise HTTPException(
            status_code=500, detail=f"Error al enviar los datos al backend: {e}"
        )
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
