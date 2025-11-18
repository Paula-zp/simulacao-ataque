import paho.mqtt.client as mqtt
import json
import time

BROKER = "localhost"
PORT = 1883
TOPIC = "banco/transferencia_real"

client_id = f"BancoSubscriber_{int(time.time())}"

def on_connect(client, userdata, flags, rc, properties=None):
    print(f"Conectado ao broker!")
    client.subscribe(TOPIC)
    print(f"Inscrito no tópico: {TOPIC}\n")
    print("Aguardando transações...\n")

def on_message(client, userdata, message):
    payload = message.payload.decode()
    dados = json.loads(payload)
    print(f"Transação processada: De {dados['de']} para {dados['para']} - R$ {dados['valor']}")

print("Sistema Bancário Interno")
print(f"Client ID: {client_id}")

client = mqtt.Client(
    callback_api_version=mqtt.CallbackAPIVersion.VERSION2,
    client_id=client_id,
    clean_session=True
)
client.on_connect = on_connect
client.on_message = on_message
client.connect(BROKER, PORT)

client.loop_forever()