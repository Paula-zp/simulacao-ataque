import paho.mqtt.client as mqtt
import json
import time

BROKER = "localhost"
PORT = 1883
TOPIC = "banco/mensagem_secreta"

def decifra_cesar(texto, chave):
    resultado = ""
    for char in texto:
        if char.isalpha():
            base = ord('A') if char.isupper() else ord('a')
            resultado += chr((ord(char) - base - chave) % 26 + base)
        else:
            resultado += char
    return resultado

def brute_force_cesar(texto_cifrado):
    print("\n🔓 INICIANDO BRUTE FORCE - Testando todas as 26 chaves possíveis:")
    print("=" * 70)
    
    resultados = []
    for chave in range(26):
        texto_decifrado = decifra_cesar(texto_cifrado, chave)
        resultados.append((chave, texto_decifrado))
        print(f"Chave {chave:2d}: {texto_decifrado}")
    
    print("=" * 70)
    
    palavras_comuns = [
    'transferencia', 'aprovada', 'autorizada', 'processada', 'realizada',
    'enviada', 'recebida', 'confirmada', 'cancelada', 'pendente',
    'senha', 'conta', 'banco', 'cofre', 'saldo', 'deposito', 'saque',
    'pagamento', 'agencia', 'cliente', 'gerente', 'cartao', 'credito',
    'debito', 'cheque', 'pix', 'ted', 'doc', 'emprestimo', 'financiamento',
    'reais', 'dolar', 'valor', 'quantia', 'total', 'parcela', 'juros',
    'taxa', 'desconto', 'cashback', 'pontos', 'segura', 'seguro', 'privada', 
    'confidencial', 'secreta', 'criptografada', 'protegida', 'autenticacao', 'token', 
    'codigo', 'verificacao', 'reuniao', 'sala', 'escritorio', 'agencia', 'sede', 'filial', 
    'hoje', 'amanha', 'segunda', 'terca', 'quarta', 'quinta', 'sexta', 'diretor', 'presidente', 
    'executivo', 'analista', 'operador', 'titular', 'beneficiario', 'portador', 'contrato', 'documento', 'comprovante', 'extrato', 'fatura', 'boleto', 'nota', 'recibo', 'declaracao',
    'assinar', 'autorizar', 'validar', 'bloquear', 'desbloquear',
    'ativar', 'desativar', 'solicitar', 'requisitar'
    ]
    
    for chave, texto in resultados:
        texto_lower = texto.lower()
        if any(palavra in texto_lower for palavra in palavras_comuns):
            print(f"\nMENSAGEM QUEBRADA! Chave mais provável: {chave}")
            print(f"   Texto decifrado: {texto}")
            return chave, texto
    
    return None, None

client_id = f"Attacker_Cesar_{int(time.time())}"

print("ATAQUE DE CRIPTOANÁLISE ATIVO")
print("=" * 50)
print("Interceptando mensagens cifradas...")
print(f"Client ID: {client_id}\n")

def on_connect(client, userdata, flags, rc, properties=None):
    print(f"Atacante conectado ao broker!")
    client.subscribe(TOPIC)
    print(f"Inscrito no tópico: {TOPIC}\n")

def on_message(client, userdata, message):
    payload = message.payload.decode()
    dados = json.loads(payload)
    
    print(f"\nMENSAGEM INTERCEPTADA #{dados['id']}")
    print(f"   Texto cifrado: {dados['mensagem_cifrada']}")
    
    chave_quebrada, texto_original = brute_force_cesar(dados['mensagem_cifrada'])
    
    if chave_quebrada is not None:
        print(f"\nCRIPTOGRAFIA QUEBRADA COM SUCESSO!")
        print(f"   CONFIDENCIALIDADE VIOLADA!")
        print(f"   Chave descoberta: {chave_quebrada}")
        print(f"   Mensagem original revelada: {texto_original}")
    
    print("\n" + "=" * 70 + "\n")

client = mqtt.Client(
    callback_api_version=mqtt.CallbackAPIVersion.VERSION2,
    client_id=client_id,
    clean_session=True
)
client.on_connect = on_connect
client.on_message = on_message
client.connect(BROKER, PORT)

client.loop_forever()