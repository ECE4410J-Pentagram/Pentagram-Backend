# Purpose: Production configuration file for cryptex
from os import environ
class Config:
    PDB_NAME = environ.get("POSTGRES_DB")
    PDB_USER = environ.get("POSTGRES_USER")
    PDB_PASS = environ.get("POSTGRES_PASSWORD")
    PDB_HOST = environ.get("POSTGRES_HOST")
    PDB_PORT = environ.get("POSTGRES_PORT")
    REDIS_HOST = environ.get("REDIS_HOST")
