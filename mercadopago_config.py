import os
import mercadopago

ACCESS_TOKEN = os.getenv("MERCADOPAGO_ACCESS_TOKEN")

if not ACCESS_TOKEN:
    raise RuntimeError("MERCADOPAGO_ACCESS_TOKEN não configurado")

sdk = mercadopago.SDK(ACCESS_TOKEN)
