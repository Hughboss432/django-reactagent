# LPhantom – Quick Start Guide

Transforme este repositório em um *app* local que conversa com modelos open‑source através do **Ollama** e expõe ferramentas via **MCP**.

---

## Pré‑requisitos

| Ferramenta         | Versão mínima  | Como instalar                                              |
| ------------------ | -------------- | ---------------------------------------------------------- |
| **Python**         | 3.10 ou mais   | [https://python.org](https://python.org)                   |
| **Git**            | qualquer       | [https://git-scm.com](https://git-scm.com)                 |
| **Ollama**         | 0.6.6 ou mais¹ | [https://ollama.com/download](https://ollama.com/download) |
| **Poetry** / `pip` | opcional       | para gerenciar dependências                                |

> **¹ Por quê?** O modelo **Qwen 3** exige Ollama ≥ 0.6.6 ([ollama.com](https://ollama.com/library/qwen3?utm_source=chatgpt.com))

### Instalação rápida do Ollama

*Windows / macOS*: baixe o instalador gráfico em [https://ollama.com](https://ollama.com).

*Linux* (Snap):

```bash
sudo snap install ollama
```

Inicie o serviço:

```bash
ollama serve            # inicia a API em http://localhost:11434/ ([geshan.com.np](https://geshan.com.np/blog/2025/02/ollama-commands/?utm_source=chatgpt.com))
```

---

## 1 ▪ Baixe o modelo **Qwen 3**

O projeto foi testado com o modelo **Qwen 3**, que oferece suporte a *tool‑calling*.

```bash
ollama pull qwen3       # ~5 GB, uma única vez
```

O modelo fica em `~/.ollama` após o download.

---

## 2 ▪ Clone o repositório e instale as dependências

```bash
git clone https://github.com/Hughboss432/django-reactagent.git
cd django-reactagent

# ambiente virtual recomendado
python -m venv .venv && source .venv/bin/activate

# via pip (ou poetry install)
pip install -r requirements.txt
```

---

## 3 ▪ Inicie o servidor de ferramentas **MCP**

O servidor MCP localizado na pasta `MCP/` é iniciado automaticamente ao executar a aplicação. Ele expõe ferramentas como `add`, `subtract`, `multiply`, `secret_word`, entre outras.

Para iniciar o servidor manualmente em modo de teste:

```bash
mcp dev server.py
```

O terminal exibirá algo como:

```
Local URL: http://localhost:8001
```

> *Obs.* Escuta em stdio/pipe; nenhum port TCP é aberto (funciona de forma local).

---

## 4 ▪ Execute a aplicação Django

Abra o **terminal** e digite:

```bash
python manage.py runserver
```

Acesse [http://localhost:8000](http://localhost:8000) no navegador. O chat usará o modelo **Qwen 3** local e chamará as ferramentas servidas pelo MCP.

---

## 5 ▪ Script auxiliar (opcional – ainda em testes)

```bash
./run.sh   # faz os passos 1‑4 automaticamente (Linux/macOS)
```

No Windows:

```powershell
.\run.ps1
```

---

## Problemas comuns

| Sintoma                              | Possível causa                           | Solução                                                                        |
| ------------------------------------ | ---------------------------------------- | ------------------------------------------------------------------------------ |
| `ERR: model not found`               | Modelo Qwen3 não baixado                 | Execute `ollama pull qwen3` e confirme em `ollama list`.                       |
| Ferramenta aparece como JSON no chat | Fluxo `agent → tools → agent` incompleto | Revise `create_graph_with_tools()`: o nó **tools** deve retornar ao **agent**. |
| `TypeError: object is not awaitable` | Mistura de nós sync/async                | Use `app.astream()` ou converta o nó para síncrono.                            |

---

## Licença

MIT
