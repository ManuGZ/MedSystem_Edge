from fastapi import FastAPI
from adapters.bpm.bpm_processor import router as bpm_router

app = FastAPI()

# Registrar el router de BPM
app.include_router(bpm_router)
