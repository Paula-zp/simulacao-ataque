import paho.mqtt.client as mqtt
import time
import json

BROKER = "localhost"
PORT = 1883
TOPIC = "banco/mensagem_secreta"

def cifra_cesar(texto, chave):
    resultado = ""
    for char in texto:
        if char.isalpha():
            base = ord('A') if char.isupper() else ord('a')
            resultado += chr((ord(char) - base + chave) % 26 + base)
        else:
            resultado += char
    return resultado

client_id = f"BancoPublisher_{int(time.time())}"

client = mqtt.Client(
    callback_api_version=mqtt.CallbackAPIVersion.VERSION2,
    client_id=client_id,
    clean_session=True
)
client.connect(BROKER, PORT)

print("Banco conectado ao broker MQTT")
print(f"Client ID: {client_id}")
print("Enviando mensagens criptografadas (Cifra de César)...\n")

CHAVE_SECRETA = 13  # ROT13

mensagens = [
    "Transferencia de R$ 50000 aprovada para conta secreta",
    "Senha do cofre: ALPHA2024BRAVO",
    "Reuniao secreta as 15h na sala executiva"
]

for i, msg in enumerate(mensagens, 1):
    msg_cifrada = cifra_cesar(msg, CHAVE_SECRETA)
    
    dados = {
        "id": i,
        "mensagem_cifrada": msg_cifrada,
        "timestamp": time.time()
    }
    
    payload = json.dumps(dados)
    client.publish(TOPIC, payload)
    
    print(f"Mensagem {i} enviada:")
    print(f"   Original: {msg}")
    print(f"   Cifrada:  {msg_cifrada}\n")
    time.sleep(2)

client.disconnect()
print("Banco desconectado")