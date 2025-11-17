import paho.mqtt.client as mqtt
import json
import time

BROKER = "localhost"
PORT = 1883
TOPIC = "banco/mensagem_secreta"

CHAVE_SECRETA = 13

def decifra_cesar(texto, chave):
    resultado = ""
    for char in texto:
        if char.isalpha():
            base = ord('A') if char.isupper() else ord('a')
            resultado += chr((ord(char) - base - chave) % 26 + base)
        else:
            resultado += char
    return resultado

client_id = f"BancoSubscriber_{int(time.time())}"

print("Sistema Bancário Receptor")
print(f"Client ID: {client_id}")
print(f"Chave de descriptografia: {CHAVE_SECRETA}")

def on_connect(client, userdata, flags, rc, properties=None):
    print(f"Conectado ao broker!")
    client.subscribe(TOPIC)
    print(f"Inscrito no tópico: {TOPIC}\n")
    print("Aguardando mensagens criptografadas...\n")

def on_message(client, userdata, message):
    payload = message.payload.decode()
    dados = json.loads(payload)
    
    msg_cifrada = dados['mensagem_cifrada']
    msg_original = decifra_cesar(msg_cifrada, CHAVE_SECRETA)
    
    print(f"Mensagem #{dados['id']} recebida:")
    print(f"   Cifrada:      {msg_cifrada}")
    print(f"   Decifrada:    {msg_original}")
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