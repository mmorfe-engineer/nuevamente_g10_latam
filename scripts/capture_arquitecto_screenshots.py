import json
import time
import base64
from pathlib import Path
import requests
import websocket

CDP_BASE = "http://localhost:9222"
SCREENSHOT_DIR = Path("/home/bitcoinpapa/projects/nuevamente/docs/screenshots")
ARTIFACT_DIR = Path("/home/bitcoinpapa/.gemini/antigravity/brain/adbf5ada-d35d-45d8-8894-b102bf515c88/screenshots")

tabs = requests.get(f"{CDP_BASE}/json/list").json()
target = next((t for t in tabs if t.get("type") == "page" and "8501" in t.get("url", "")), None)
if not target:
    print("No 8501 tab found")
    exit(1)

ws = websocket.create_connection(target["webSocketDebuggerUrl"], timeout=15)
msg_id = 0
def send(method, params=None):
    global msg_id
    msg_id += 1
    ws.send(json.dumps({"id": msg_id, "method": method, "params": params or {}}))
    while True:
        resp = json.loads(ws.recv())
        if resp.get("id") == msg_id:
            return resp.get("result", {})

def set_viewport(w=1400, h=1400):
    send("Emulation.setDeviceMetricsOverride", {
        "width": w,
        "height": h,
        "deviceScaleFactor": 1,
        "mobile": False
    })

def capture(filepath):
    res = send("Page.captureScreenshot", {"format": "png"})
    data = base64.b64decode(res["data"])
    with open(filepath, "wb") as f:
        f.write(data)
    with open(ARTIFACT_DIR / filepath.name, "wb") as f:
        f.write(data)
    print(f"📸 Capturado: {filepath.name} ({len(data)} bytes)")

def scroll(y):
    expr = f"""
    (() => {{
        const main = document.querySelector('.stMain') || document.querySelector('section[data-testid="stMain"]');
        if (main) main.scrollTop = {y};
        window.scrollTo(0, {y});
    }})()
    """
    send("Runtime.evaluate", {"expression": expr})
    time.sleep(1.0)

set_viewport(1400, 1400)
scroll(0)
time.sleep(1.0)

f3 = SCREENSHOT_DIR / "05_pci_dss_02_arquitecto_guia_practica_encabezado.png"
capture(f3)

# Scroll down to practical steps and code/commands
scroll(520)
time.sleep(1.0)
f4 = SCREENSHOT_DIR / "05_pci_dss_02_guia_practica_pasos.png"
capture(f4)

print("✅ Capturas de Arquitecto / Guía Práctica guardadas exitosamente.")
