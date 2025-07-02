# LPhantom – Quick Start Guide

Transforme o repositório em um app local que usa Llama 3.2 via **Ollama** e ferramentas MCP.

---

## Pré‑requisitos

| Ferramenta          | Versão recomendada | Como instalar                                                                 |          |
| ------------------- | ------------------ | ----------------------------------------------------------------------------- | -------- |
| **Python**          | ≥ 3.10             | [https://python.org](https://python.org)                                      |          |
| **Git**             | qualquer           | [https://git-scm.com](https://git-scm.com)                                    |          |
| **Ollama**          | 0.1.32 ou maior    | \`\`\`curl -fsSL [https://ollama.ai/install.sh](https://ollama.ai/install.sh) | sh\`\`\` |
| **Poetry** ou `pip` | opcional           | para instalar dependências                                                    |          |

> **Windows** / **macOS**: baixe o instalador gráfico em [https://ollama.ai](https://ollama.ai).

---

## 1 ▪ Baixe o modelo Llama 3.2

```bash
ollama pull llama3.2
```

Esperado: download de \~4 GB; uma vez concluído o modelo fica disponível localmente em `~/.ollama`.

---

## 2 ▪ Clone o repositório e instale dependências

```bash
git clone https://github.com/Hughboss432/automato-reactagent.git
cd seu‑repo
# ambiente virtual opcional X (OBRIGATORIO ATUALMENTE)
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

---

## 3 ▪ Inicie o servidor de ferramentas MCP

`server.py` expõe as ferramentas (add, subtract, multiply, secret\_word…).

```bash
python server.py
```

*Escuta em stdio/pipe; nenhum port TCP é aberto.*

---

## 4 ▪ Execute a aplicação Streamlit

Abra um segundo terminal (deixe `server.py` rodando) e digite:

```bash
streamlit run app.py
```

Streamlit imprimirá algo como:

```
  You can now view your Streamlit app in your browser.
  Local URL: http://localhost:xxxx
```

Acesse o link no navegador. Pronto! O chat usará o modelo **llama3.2** local e chamará as ferramentas servidas pelo MCP.

---

## 5 ▪ Atalho (tudo‑em‑um) X (AINDA NÃO FUNCIONA)

Linux/macOS:

```bash
./run.sh   # script helper que faz passos 1‑4 automaticamente
```

Windows PowerShell:

```powershell
.\run.ps1   # idem
```

---

## Problemas comuns X (TEMPORARIO)

| Sintoma                              | Causa provável                                     | Solução                                                                          |
| ------------------------------------ | -------------------------------------------------- | -------------------------------------------------------------------------------- |
| `ERR: model not found`               | O Ollama não consegue localizar *llama3.2*         | Verifique se o download terminou e rode `ollama list`                            |
| JSON da ferramenta aparece no chat   | Pipeline `agent → tools → agent` não está completo | Revise `create_graph_with_tools()` – garanta que o nó `tools` volta para `agent` |
| `TypeError: object is not awaitable` | Mistura de nós async e sync                        | Use `app.astream` para nós async ou converta o nó para sync                      |

---

## Licença

Coloque aqui sua licença (MIT, Apache‑2.0, Proprietária etc.).
