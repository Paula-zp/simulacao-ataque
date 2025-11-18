import paho.mqtt.client as mqtt
import json
import time
from cryptography.fernet import Fernet
import base64
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

client_id = f"BancoSubscriber_{int(time.time())}"

print(f"Client ID: {client_id}")

fernet = Fernet(CHAVE_AES)

def on_connect(client, userdata, flags, rc, properties=None):
    print(f"Conectado ao broker!")
    client.subscribe(TOPIC)
    print(f"Inscrito no tópico: {TOPIC}\n")
    print("Aguardando mensagens secretas...\n")

def on_message(client, userdata, message):
    payload = message.payload.decode()
    dados = json.loads(payload)
    
    msg_secreta = dados['mensagem_secreta'].encode()
    msg_original = fernet.decrypt(msg_secreta).decode()
    
    print(f"Mensagem #{dados['id']} recebida:")
    print(f"   Secreta: {dados['mensagem_secreta'][:50]}...")
    print(f"   Sem o segredo: {msg_original}")
    print(f"   Mensagem processada com sucesso!\n")

client = mqtt.Client(
    callback_api_version=mqtt.CallbackAPIVersion.VERSION2,
    client_id=client_id,
    clean_session=True
)
client.on_connect = on_connect
client.on_message = on_message
client.connect(BROKER, PORT)

client.loop_forever()