import paho.mqtt.client as mqtt
import time
import json
from cryptography.fernet import Fernet
import base64
import os
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

def gerar_chave_from_senha(senha):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=b'salt',
        iterations=100000,
    )
    key = base64.urlsafe_b64encode(kdf.derive(senha.encode()))
    return key

BROKER = "localhost"
PORT = 1883
TOPIC = "banco/mensagem_secreta"
SENHA_COMPARTILHADA = "SenhaCompartilhada"
CHAVE_AES = gerar_chave_from_senha(SENHA_COMPARTILHADA)

client_id = f"BancoPublisher_{int(time.time())}"

client = mqtt.Client(
    callback_api_version=mqtt.CallbackAPIVersion.VERSION2,
    client_id=client_id,
    clean_session=True
)
client.connect(BROKER, PORT)

print("Banco conectado (CRIPTOGRAFIA FORTE)")
print(f"Client ID: {client_id}")
print("Usando AES-256 com Fernet\n")

mensagens = [
    "Transferencia de R$ 50000 aprovada para conta secreta",
    "Senha do cofre: ALPHA2024BRAVO",
    "Reuniao secreta as 15h na sala executiva"
]

fernet = Fernet(CHAVE_AES)

for i, msg in enumerate(mensagens, 1):
    msg_secreta = fernet.encrypt(msg.encode()).decode()
    
    dados = {
        "id": i,
        "mensagem_secreta": msg_secreta,
        "timestamp": time.time()
    }
    
    payload = json.dumps(dados)
    client.publish(TOPIC, payload)
    
    print(f"Mensagem {i} enviada:")
    print(f"   Original: {msg}")
    print(f"   secreta (AES-256): {msg_secreta[:50]}...")
    print()
    time.sleep(2)

client.disconnect()
print("🏦 Banco desconectado")