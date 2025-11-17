# Simulação de ataques MQTT

Este repositório consolida dois cenários simples que ilustram como um invasor pode comprometer **integridade** e **confidencialidade** em mensagens trafegando por um broker MQTT local.

## Estrutura

- `integridade/` – fluxo publisher/attacker/subscriber no qual o atacante se posiciona como *man-in-the-middle*, altera o campo `para` e redireciona as transações para outro tópico.
- `confidencialidade/` – fluxo publisher/subscriber usando Cifra de César (ROT13) e um atacante que intercepta e faz *brute force* para quebrar a mensagem confidencial.
- `disponibilidade/` – fluxo publisher/attacker/subscriber no qual o atacante realiza um flood de mensagens para o mesmo tópico e degrada o recebimento dos heartbeats.

Cada pasta contém três scripts independentes (`publisher*.py`, `attacker*.py`, `subscriber*.py`) prontos para serem executados em terminais separados.

## Requisitos

- Python 3.11+ (ou equivalente disponível na máquina).
- Broker MQTT aceitando conexões em `localhost:1883` (ex.: Mosquitto).
- Dependências listadas em `requirements.txt` (`paho-mqtt`).

### Setup rápido

```powershell
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
```

## Cenário 1 – Violação de integridade (MITM)

1. Abra três terminais e navegue para `integridade/`.
2. Terminal 1 – sistema legítimo:
   ```powershell
   python subscriber.py
   ```
3. Terminal 2 – atacante MITM:
   ```powershell
   python attacker.py
   ```
4. Terminal 3 – banco publicador:
   ```powershell
   python publisher.py
   ```

### Resultado esperado

O atacante lê `banco/transferencia`, sobrescreve o destinatário para “Conta do Hacker” e publica a mensagem adulterada em `banco/transferencia_real`. O subscriber legítimo, que confia apenas no tópico adulterado, processa transações já manipuladas, evidenciando a quebra de integridade.

## Cenário 2 – Violação de confidencialidade (Cifra de César)

1. Abra três terminais e navegue para `confidencialidade/`.
2. Terminal 1 – banco receptor:
   ```powershell
   python subscriber_cesar.py
   ```
3. Terminal 2 – atacante criptoanalista:
   ```powershell
   python attacker_cesar.py
   ```
4. Terminal 3 – banco emissor de mensagens cifradas:
   ```powershell
   python publisher_cesar.py
   ```

### Resultado esperado

O publisher envia mensagens sensíveis cifradas com ROT13 no tópico `banco/mensagem_secreta`. O attacker intercepta cada publicação, executa *brute force* das 26 chaves possíveis da Cifra de César e identifica automaticamente a chave correta usando palavras-chave financeiras. Com a chave recuperada, ele revela o conteúdo das mensagens, demonstrando a perda total de confidencialidade.

## Cenário 3 – Ataque à disponibilidade (Flood / DoS)

1. Abra três terminais e navegue para `disponibilidade/`.
2. Terminal 1 – monitor legítimo:
   ```powershell
   python subscriber.py
   ```
3. Terminal 2 – atacante flooder:
   ```powershell
   python attacker.py
   ```
4. Terminal 3 – publisher de heartbeats:
   ```powershell
   python publisher.py
   ```

### Resultado esperado

O publisher envia heartbeats sequenciais que o monitor usa para medir latência e quedas. O atacante publica centenas de mensagens por segundo com payload grande no mesmo tópico `banco/disponibilidade/status`, forçando o broker e o subscriber a tratar ruído constante. O monitor imprime alertas quando detecta heartbeats atrasados ou sequências quebradas, simulando a indisponibilidade causada pelo DoS.

---

Esses dois exemplos podem ser combinados ou estendidos para explorar conceitos de CIA triad (Confidentiality, Integrity, Availability) em ambientes MQTT e reforçar boas práticas de proteção (TLS, autenticação por certificado, tópicos segregados, payload criptografado robusto, etc.).
