from fastapi import FastAPI
from adapters.bpm.bpm_processor import router as bpm_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost:4200/",
    # Puedes agregar más orígenes si necesitas
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # puedes usar [""] para desarrollo si no tienes riesgos
    allow_credentials=True,
    allow_methods=[""],
    allow_headers=["*"],
)

# Registrar el router de BPM
app.include_router(bpm_router)
