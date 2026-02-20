# fast-api-accelerate

This project is a CLI for creating standard backend projects using FastAPI.
Tenologias usadas: 
gerenciador de dependencias: uv

## Pre-requisitos 
-  astral-uv  installed in your machine
```bash
    sudo snap install astral-uv --classic
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
    uv add --dev pytest
```

## remove dependences
```bash
    uv remove requests
```

## run app
```bash
    python3 ./main.py 
```
