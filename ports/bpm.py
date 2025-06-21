from fastapi import HTTPException
import httpx
from schemas.edge import BPMRequest
from collections import deque
import statistics


class BPMProcessor:
    def __init__(self):
        self.backend_url = "http://localhost:8080/api/bpm/receive"
        self.bpm_data = deque(
            maxlen=10
        )  # Guardamos los últimos 10 datos de BPM para análisis en tiempo real
        self.processed_bpm = []  # Almacenamos los BPM procesados

    async def process_bpm(self, bpm: BPMRequest):
        """Procesar el valor BPM y hacer análisis en tiempo real"""
        if bpm.bpm_value < 30 or bpm.bpm_value > 200:
            raise HTTPException(
                status_code=400, detail="BPM value out of range (30-200)"
            )

        # Ingresar el nuevo dato de BPM en nuestra cola para análisis en tiempo real
        self.bpm_data.append(bpm.bpm_value)

        # Calcular la media de los últimos BPM
        average_bpm = statistics.mean(self.bpm_data) if self.bpm_data else 0
        anomaly_detected = self.detect_anomaly(bpm.bpm_value)

        result = {
            "processed_bpm": bpm.bpm_value,
            "timestamp": bpm.timestamp,
            "status": "valid",
            "average_bpm": average_bpm,
            "anomaly_detected": anomaly_detected,
        }

        # Guardar los datos procesados
        self.processed_bpm.append(result)

        # Enviar los datos procesados al backend Spring Boot (opcional)
        await self.send_data_to_spring_backend(result)

        return result

    def detect_anomaly(self, bpm_value: float):
        """Detectar anomalías en los datos BPM (por ejemplo, picos fuera de rango)"""
        if bpm_value > 150:
            return True
        return False

    async def send_data_to_spring_backend(self, data: dict):
        """Enviar los datos procesados al backend de Spring Boot"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(self.backend_url, json=data)
                response.raise_for_status()  # Lanza un error si la respuesta no es exitosa
                return response.json()
        except httpx.HTTPStatusError as e:
            raise HTTPException(status_code=500, detail=f"Backend error: {e}")
        except Exception as e:
            raise HTTPException(
                status_code=500, detail=f"Error sending data to Spring Boot: {e}"
            )

    def get_processed_bpm_data(self):
        """Obtener los datos BPM procesados"""
        return self.processed_bpm
