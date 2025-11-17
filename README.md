# Simulacao de ataque Man-in-the-Middle

Este repositorio demonstra, de forma simples, como um invasor pode se posicionar entre um publicador e um assinante MQTT para adulterar mensagens de transferencia bancaria.

## Componentes

- `man-in-the-middle/publisher.py` envia tres transferencias ficticias para o topico `banco/transferencia`.
- `man-in-the-middle/attacker.py` assina o topico original, altera o campo `para` da mensagem e encaminha o JSON adulterado para `banco/transferencia_real`.
- `man-in-the-middle/subscriber.py` representa o sistema bancario legitimo, assinando apenas o topico adulterado.

## Requisitos

- Python 3.11+ (ou equivalente instalado na sua maquina).
- Broker MQTT local (por exemplo Mosquitto) aceitando conexoes em `localhost:1883`.
- Dependencias listadas em `requirements.txt` (principalmente `paho-mqtt`).

## Como executar

1. (Opcional) criar e ativar um ambiente virtual:
   ```powershell
   python -m venv venv
   .\venv\Scripts\activate
   ```
2. Instalar dependencias:
   ```powershell
   pip install -r requirements.txt
   ```
3. Garantir que o broker MQTT esteja em execucao.
4. Em tres terminais separados, dentro de `man-in-the-middle`, executar:
   ```powershell
   # Terminal 1 - sistema legitimo
   python subscriber.py

   # Terminal 2 - atacante
   python attacker.py

   # Terminal 3 - banco publicador
   python publisher.py
   ```

O subscriber mostrara que as transferencias recebidas chegam com o destino modificado, evidenciando a quebra de integridade causada pelo ataque MITM.
