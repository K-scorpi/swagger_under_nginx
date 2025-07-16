import os
import subprocess
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
import json

app = FastAPI()

ACCESS_FILE = "access_status.json"

# Инициализация файла состояния доступа
if not os.path.exists(ACCESS_FILE):
    with open(ACCESS_FILE, "w") as f:
        json.dump({"allowed": True}, f)


def get_access_status():
    with open(ACCESS_FILE, "r") as f:
        data = json.load(f)
    return data["allowed"]


def set_access_status(allowed: bool):
    with open(ACCESS_FILE, "w") as f:
        json.dump({"allowed": allowed}, f)


def execute_systemctl(command: str):
    try:
        result = subprocess.run(
            ["sudo", "systemctl", command, "nginx"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        return {"stdout": result.stdout, "stderr": result.stderr}
    except subprocess.CalledProcessError as e:
        return {"stdout": e.stdout, "stderr": e.stderr}


@app.get("/access")
def check_access():
    """Проверить текущий статус доступа"""
    return {"access_allowed": get_access_status()}


@app.post("/access/enable")
def enable_access():
    """Разрешить доступ к управлению сервисом"""
    set_access_status(True)
    return {"message": "Доступ разрешён"}


@app.post("/access/disable")
def disable_access():
    """Запретить доступ к управлению сервисом"""
    set_access_status(False)
    return {"message": "Доступ запрещён"}


@app.get("/status")
def get_status():
    """Получить текущий статус сервиса nginx"""
    if not get_access_status():
        raise HTTPException(status_code=403, detail="Доступ запрещён")

    output = execute_systemctl("is-active")
    return {"status": output["stdout"].strip() or output["stderr"].strip()}


@app.post("/start")
def start_service():
    """Запустить сервис nginx"""
    if not get_access_status():
        raise HTTPException(status_code=403, detail="Доступ запрещён")

    result = execute_systemctl("start")
    return {"message": "nginx started", "output": result}


@app.post("/stop")
def stop_service():
    """Остановить сервис nginx"""
    if not get_access_status():
        raise HTTPException(status_code=403, detail="Доступ запрещён")

    result = execute_systemctl("stop")
    return {"message": "nginx stopped", "output": result}


@app.post("/restart")
def restart_service():
    """Перезапустить сервис nginx"""
    if not get_access_status():
        raise HTTPException(status_code=403, detail="Доступ запрещён")

    result = execute_systemctl("restart")
    return {"message": "nginx restarted", "output": result}