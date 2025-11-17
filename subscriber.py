import paho.mqtt.client as mqtt
import json

BROKER = "localhost"
PORT = 1883
TOPIC = "banco/transferencia_real"

def on_message(client, userdata, message):
    payload = message.payload.decode()
    dados = json.loads(payload)
    print(f"💰 Transação processada: De {dados['de']} para {dados['para']} - R$ {dados['valor']}")

client = mqtt.Client(callback_api_version=mqtt.CallbackAPIVersion.VERSION2, client_id="BancoSubscriber")
client.on_message = on_message
client.connect(BROKER, PORT)
client.subscribe(TOPIC)

print("Sistema Bancário Interno")
print(f"Aguardando transações no canal seguro: {TOPIC}\n")

client.loop_forever()