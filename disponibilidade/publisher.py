import json
import time

import paho.mqtt.client as mqtt

BROKER = "localhost"
PORT = 1883
TOPIC = "banco/disponibilidade/status"
HEARTBEAT_INTERVAL = 1.0  # seconds


def main():
    client_id = f"BancoPublisher_Disponibilidade_{int(time.time())}"
    client = mqtt.Client(
        callback_api_version=mqtt.CallbackAPIVersion.VERSION2,
        client_id=client_id,
        clean_session=True,
    )
    client.connect(BROKER, PORT)

    print("Publisher de disponibilidade iniciado")
    print(f"Client ID: {client_id}")
    print(f"Enviando heartbeats para o tópico {TOPIC}\n")

    seq = 0
    try:
        while True:
            seq += 1
            payload = {
                "tipo": "legitimo",
                "sequencia": seq,
                "status": "operacional",
                "timestamp": time.time(),
            }
            client.publish(TOPIC, json.dumps(payload))
            print(f"Heartbeat #{seq} enviado")
            time.sleep(HEARTBEAT_INTERVAL)
    except KeyboardInterrupt:
        print("\nEnvio interrompido pelo usuário")
    finally:
        client.disconnect()
        print("Publisher desconectado")


if __name__ == "__main__":
    main()
