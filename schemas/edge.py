from pydantic import BaseModel


# ---------- 3. MONITORING ----------
class MonitoringRequest(BaseModel):
    siteId: str
    metric: str
    value: float


# ---------- 5. BPM ----------
class BPMRequest(BaseModel):
    bpm_value: float
    timestamp: str
