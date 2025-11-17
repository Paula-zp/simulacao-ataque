import json
import time

import paho.mqtt.client as mqtt

BROKER = "localhost"
PORT = 1883
TOPIC = "banco/disponibilidade/status"
MAX_LATENCY = 2.0  # segundos aceitáveis para o heartbeat

state = {
    "legitimas": 0,
    "flood": 0,
    "ultima_sequencia": 0,
}


def on_connect(client, userdata, flags, rc, properties=None):
    print("Monitor de disponibilidade conectado ao broker")
    client.subscribe(TOPIC)
    print(f"Inscrito no tópico {TOPIC}\n")
    print("Aguardando heartbeats...\n")


def on_message(client, userdata, message):
    payload = message.payload.decode()
    dados = json.loads(payload)

    if dados.get("tipo") == "legitimo":
        state["legitimas"] += 1
        seq = dados.get("sequencia", 0)
        atraso = time.time() - dados.get("timestamp", time.time())

        delta = seq - state["ultima_sequencia"]
        state["ultima_sequencia"] = max(state["ultima_sequencia"], seq)

        print(f"Heartbeat #{seq} recebido (atraso {atraso:.2f}s)")

        if atraso > MAX_LATENCY:
            print("ALERTA: Heartbeat atrasado além do limite esperado!")

        if delta > 1:
            print("ALERTA: Heartbeats perdidos detectados!")
    else:
        state["flood"] += 1
        total = state["flood"]
        if total % 200 == 0:
            print(f"Ruído malicioso detectado ({total} mensagens flood acumuladas)")


def main():
    client_id = f"MonitorDisponibilidade_{int(time.time())}"
    client = mqtt.Client(
        callback_api_version=mqtt.CallbackAPIVersion.VERSION2,
        client_id=client_id,
        clean_session=True,
    )
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(BROKER, PORT)

    print("Monitor de disponibilidade iniciado")
    print(f"Client ID: {client_id}")

    try:
        client.loop_forever()
    except KeyboardInterrupt:
        print("\nMonitor finalizado pelo usuário")


if __name__ == "__main__":
    main()
