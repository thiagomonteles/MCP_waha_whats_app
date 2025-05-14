from fastmcp import FastMCP

import requests

# Inicializa o servidor MCP com um nome identificador
mcp = FastMCP("whatsapp_mcp_server")

# Recurso: lista de contatos predefinidos
@mcp.resource("resource://contatos")
def get_contatos() -> list[dict[str, str]]:
    """Lista de contatos predefinidos (nome e número em formato internacional)."""
    return [
        {"Antonio": "+556294638284", "Thiago": "+556291938719"}
    ]

# Tool: envia mensagem via WAHA API
@mcp.tool()
def send_message(numero: str, mensagem: str) -> str:
    """Envia uma mensagem de texto via WAHA (WhatsApp HTTP API).

    Args:
        numero: Número do destinatário em formato internacional (ex: +5511999999999).
        mensagem: Texto da mensagem a ser enviada.

    Returns:
        Uma string indicando sucesso ou descrevendo um erro.
    """

    chat_id = f"{numero.lstrip('+')}@c.us"
    payload = {
        "chatId": chat_id,
        "text": mensagem,
        "session": "default"
    }
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }
    try:
        # Chamada HTTP POST para o endpoint /api/sendText do WAHA
        response = requests.post("http://localhost:3000/api/sendText",
                                 json=payload, headers=headers)
        response.raise_for_status()  
    except Exception as e:
        return f"Erro ao enviar mensagem: {e}"
    return "Mensagem enviada com sucesso."

if __name__ == "__main__":
    mcp.run(transport="sse", host="127.0.0.1", port=8000)
