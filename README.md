# 🤖 Telegram LLM Chatbot with Memory & Plugins

[![Python 3.9](https://img.shields.io/badge/python-3.9-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Docker](https://badgen.net/badge/icon/docker?icon=docker&label)](https://docker.com)

A sophisticated Telegram chatbot powered by Together.ai's LLMs (Llama 3/Mistral) with persistent memory, plugin support, and role-based interactions. Built with Python and ChromaDB.

**Repository**: https://github.com/yurikorolov/Telegram-Chatbot

## 🌟 Features

- **LLM Backed**  
  - Meta-Llama-3.1-8B-Instruct-Turbo & Mistral-7B
  - Together.ai API integration
- **Memory System**  
  - ChromaDB vector storage
  - Context-aware conversations
- **Plugin Architecture**  
  - WolframAlpha math integration
  - Extensible plugin system
- **Role Play**  
  - Lawyer/Developer/Marketer personas
  - Custom mission modes
- **Docker Ready**  
  - Pre-configured compose setup
  - Persistent storage volumes

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- Docker & Docker Compose
- Telegram API keys ([Get here](https://my.telegram.org/auth))
- Together.ai API key ([Sign up](https://api.together.xyz/))

### Installation
```bash
git clone https://github.com/yurikorolov/Telegram-Chatbot
cd Telegram-Chatbot
```

### Configuration
1. Create `.env` file:
```ini
API_ID=your_telegram_api_id
API_HASH=your_telegram_api_hash
BOT_TOKEN=your_bot_token
TOGETHER_API_KEY=your_together_key
WOLFRAMALPHA_APP_ID=your_wolfram_id
```

2. Build & Run with Docker:
```bash
mkdir -p chroma_data onnx_models  # Create volume directories
docker-compose up --build -d
```

### Manual Setup (Without Docker)
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python main.py
```

## 🛠 Usage

### Core Commands
| Command                | Description                          |
|------------------------|--------------------------------------|
| `/start`               | Initialize the bot                   |
| `/missions [name]`     | Enable teaching/assist/converse mode |
| `/plugins toggle`      | Enable WolframAlpha integration      |
| `/role [name]`         | Activate lawyer/developer persona    |
| `/memory`              | Toggle conversation memory           |
| `/addmemory`           | Manually store important information |

### Example Interaction
```
User: /role Lawyer
Bot: Role set

User: What's required for a valid contract?
Bot: [Legal analysis using Llama-3 in lawyer persona...]
```

## 🔧 Configuration

### Environment Variables
| Variable               | Required | Description                     |
|------------------------|----------|---------------------------------|
| `API_ID`               | Yes      | Telegram App ID                 |
| `API_HASH`             | Yes      | Telegram App Hash               |
| `BOT_TOKEN`            | Yes      | Telegram Bot Token              |
| `TOGETHER_API_KEY`     | Yes      | Together.ai API Key             |
| `WOLFRAMALPHA_APP_ID`  | No       | For math plugin functionality   |

### Docker Volumes
| Host Path             | Container Path            | Purpose               |
|-----------------------|---------------------------|-----------------------|
| `./chroma_data`       | `/app/persist`            | Conversation memory   |
| `./onnx_models`       | `/root/.cache/chroma/...` | ML models             |

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## 📜 License

MIT License - See [LICENSE](LICENSE) for details

## 💡 Tech Stack

- **Core**: Python 3.9, Telethon
- **AI**: Together.ai, Llama-3, Mistral
- **Memory**: ChromaDB
- **Plugins**: WolframAlpha API
- **Infra**: Docker, Docker Compose