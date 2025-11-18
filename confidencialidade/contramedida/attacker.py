import paho.mqtt.client as mqtt
import json
import time

BROKER = "localhost"
PORT = 1883
TOPIC = "banco/mensagem_secreta"

client_id = f"Attacker_{int(time.time())}"

print("TENTATIVA DE ATAQUE BRUTE FORCE")
print("=" * 50)
print("Tentando quebrar AES-256...")
print(f"Client ID: {client_id}\n")

def on_connect(client, userdata, flags, rc, properties=None):
    print(f"Atacante conectado!")
    client.subscribe(TOPIC)
    print(f"Inscrito no tópico: {TOPIC}\n")

def on_message(client, userdata, message):
    payload = message.payload.decode()
    dados = json.loads(payload)
    
    print(f"\nMENSAGEM INTERCEPTADA #{dados['id']}")
    print(f"   Texto criptografado: {dados['mensagem_secreta'][:60]}...")
    
    print(f"\nTentando quebrar AES-256 por força bruta...")
    print(f"   Número de chaves possíveis: 2^256")
    print(f"   = 115.792.089.237.316.195.423.570.985.008.687.907.853.269.984.665.640.564.039.457.584.007.913.129.639.936")
    print(f"\n   Tempo estimado (1 bilhão de tentativas/segundo):")
    print(f"   = 3.67 × 10^51 anos (idade do universo: 1.38 × 10^10 anos)")
    
    print(f"\n   Erro: Não é possível quebrar por força bruta")
    print("=" * 70)

client = mqtt.Client(
    callback_api_version=mqtt.CallbackAPIVersion.VERSION2,
    client_id=client_id,
    clean_session=True
)
client.on_connect = on_connect
client.on_message = on_message
client.connect(BROKER, PORT)

client.loop_forever()