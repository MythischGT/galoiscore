import os, sys
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.routers import field, ecc, utils

app = FastAPI(
    title="galois-api",
    description="REST API over galois_core: prime-field arithmetic, ECC, and number-theory utils.",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(field.router, prefix="/api/field", tags=["Prime Field"])
app.include_router(ecc.router,   prefix="/api/ecc",   tags=["ECC"])
app.include_router(utils.router, prefix="/api/utils", tags=["Utilities"])

@app.get("/", tags=["Meta"])
def root():
    return {
        "name": "galois-api",
        "version": "0.1.0",
        "docs": "/docs",
        "endpoints": ["/api/field", "/api/ecc", "/api/utils"],
    }