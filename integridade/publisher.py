import paho.mqtt.client as mqtt
import time
import json

BROKER = "localhost"
PORT = 1883
TOPIC = "banco/transferencia"

client_id = f"BancoPublisher_{int(time.time())}"

client = mqtt.Client(
    callback_api_version=mqtt.CallbackAPIVersion.VERSION2,
    client_id=client_id,
    clean_session=True
)
client.connect(BROKER, PORT)

print("Banco conectado ao broker MQTT")
print(f"Client ID: {client_id}")
print("Enviando transações financeiras...\n")

transferencias = [
    {"de": "Gabriel", "para": "Paula", "valor": 5000, "senha": "senha123"},
    {"de": "Paula", "para": "Leandro", "valor": 10000, "senha": "12345678"},
    {"de": "Leandro", "para": "Gabriel", "valor": 2500, "senha": "qwerty"}
]

for i, transf in enumerate(transferencias, 1):
    mensagem = json.dumps(transf)
    client.publish(TOPIC, mensagem)
    print(f"✅ Transação {i} enviada: {mensagem}")
    time.sleep(2)

client.disconnect()
print("\n🏦 Banco desconectado")