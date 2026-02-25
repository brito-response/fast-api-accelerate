# fast-api-accelerate

This project is a CLI for creating standard backend projects using FastAPI.

## ⚙️ Technologies used: 
dependency manager: uv
web framework:FastAPI
Python 3.10+
Typer (CLI framework)

## 📋 Requirements

Python 3.10 or higher
<p align="center"> <img src="./docs/arquitetura_base.png" width="750"/> </p> <p align="center"> A powerful CLI to scaffold structured and production-ready FastAPI backend projects. </p>

## Pre-requisitos 
-  astral-uv  installed in your machine
```bash
    sudo snap install astral-uv --classic #or
    curl -LsSf https://astral.sh/uv/install.sh | sh && source ~/.bashrc
```

## install dependences 
```bash
    uv sync && source .venv/bin/activate
```

## add pacjkages
```bash
    uv add fastapi
```

## add pacjkages of development
```bash
    uv add --dev pytest &&
    uv add --dev black
```

## remove dependences
```bash
    uv remove requests
```

## run app
```bash
    python3 ./main.py 
```

📄 License

MIT License
