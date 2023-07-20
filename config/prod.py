# Purpose: Production configuration file for cryptex
from os import environ
class Config:
    PDB_NAME = environ.get("POSTGRES_DB")
    PDB_USER = environ.get("POSTGRES_USER")
    PDB_PASS = environ.get("POSTGRES_PASSWORD")
    PDB_HOST = "postgres"
    PDB_PORT = 5432
