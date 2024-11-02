# app/config/logging_config.py
import logging
from logging.handlers import RotatingFileHandler
import os

# Crear directorio para los logs si no existe
os.makedirs("logs", exist_ok=True)

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("ParkingLotAPI")
handler = RotatingFileHandler("logs/parking_lot_api.log", maxBytes=1000000, backupCount=3)
formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
handler.setFormatter(formatter)
logger.addHandler(handler)
