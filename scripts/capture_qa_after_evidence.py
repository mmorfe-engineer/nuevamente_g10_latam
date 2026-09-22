import json
import time
import base64
from pathlib import Path
import requests
import websocket

CDP_BASE = "http://localhost:9222"
EVIDENCE_DIR = Path("/home/bitcoinpapa/projects/nuevamente/docs/qa/evidence")
ARTIFACT_DIR = Path("/home/bitcoinpapa/.gemini/antigravity/brain/adbf5ada-d35d-45d8-8894-b102bf515c88/screenshots")

tabs = requests.get(f"{CDP_BASE}/json/list").json()
target = next((t for t in tabs if t.get("type") == "page" and "8501" in t.get("url", "")), None)
if not target:
    print("Error: No se encontró pestaña en 8501")
    exit(1)

ws = websocket.create_connection(target["webSocketDebuggerUrl"], timeout=20)
msg_id = 0

def send(method, params=None):
    global msg_id
    msg_id += 1
    ws.send(json.dumps({"id": msg_id, "method": method, "params": params or {}}))
    while True:
        resp = json.loads(ws.recv())
        if resp.get("id") == msg_id:
            return resp.get("result", {})

def set_viewport(w=1300, h=950):
    send("Emulation.setDeviceMetricsOverride", {
        "width": w,
        "height": h,
        "deviceScaleFactor": 1,
        "mobile": False
    })

def capture(out_path):
    res = send("Page.captureScreenshot", {"format": "png"})
    data = base64.b64decode(res["data"])
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "wb") as f:
        f.write(data)
    with open(ARTIFACT_DIR / out_path.name, "wb") as f:
        f.write(data)
    print(f"📸 Guardado: {out_path} ({len(data)} bytes)")

def eval_js(expr):
    res = send("Runtime.evaluate", {"expression": expr, "returnByValue": True})
    return res.get("result", {}).get("value")

def click_selector(selector):
    expr = f"""
    (() => {{
        const el = document.querySelector('{selector}');
        if (!el) return false;
        el.scrollIntoView({{behavior: 'instant', block: 'center'}});
        el.click();
        return true;
    }})()
    """
    return eval_js(expr)

def click_button_by_text(text):
    expr = f"""
    (() => {{
        const btns = Array.from(document.querySelectorAll('button'));
        const target = btns.find(b => b.innerText.includes('{text}'));
        if (!target) return false;
        target.scrollIntoView({{behavior: 'instant', block: 'center'}});
        target.click();
        return true;
    }})()
    """
    return eval_js(expr)

set_viewport(1300, 950)
time.sleep(2.0)

# 1. DEF-03 AFTER: Encabezado institucional limpio con padding-top clamp
print("Capturando DEF-03 AFTER (Área 01)...")
eval_js("window.scrollTo(0, 0);")
time.sleep(1.0)
capture(EVIDENCE_DIR / "area_01" / "DEF-03_after.png")

# 2. Cargar Caso Canónico y capturar DEF-01 AFTER (Área 02)
print("Accionando caso canónico para DEF-01...")
click_button_by_text("Caso Canónico Oracle")
time.sleep(2.0)
capture(EVIDENCE_DIR / "area_02" / "DEF-01_after.png")

# 3. Generar Material Didáctico
print("Generando material didáctico...")
click_button_by_text("Generar Material Didáctico")
time.sleep(6.0)

# Esperar a que rendericen resultados
for _ in range(15):
    has_results = eval_js("document.body.innerText.includes('Paso 3 Completado') || document.body.innerText.includes('Flashcards')")
    if has_results:
        break
    time.sleep(1.0)

time.sleep(2.0)

# 4. DEF-06 AFTER: KPI Banner con Fragmentos del Lote Activo (ADR-012)
print("Capturando DEF-06 AFTER (Área 03)...")
eval_js("window.scrollTo(0, 0);")
time.sleep(1.0)
capture(EVIDENCE_DIR / "area_03" / "DEF-06_after.png")

# 5. Voltear tarjeta y calificar para probar ciclo de vida
print("Interactuando con flashcard...")
click_button_by_text("Voltear Tarjeta")
time.sleep(1.5)
click_button_by_text("Alcanzado")
time.sleep(1.5)

# 6. Tab 2: Auditoría de Calidad (DEF-04 AFTER)
print("Navegando a Tab 2 (Auditoría)...")
eval_js("""
(() => {
    const tabs = Array.from(document.querySelectorAll('button[data-baseweb="tab"]'));
    if (tabs.length >= 2) tabs[1].click();
})()
""")
time.sleep(2.0)
eval_js("""
(() => {
    const el = Array.from(document.querySelectorAll('h3')).find(h => h.innerText.includes('Fundamento Metodológico'));
    if (el) el.scrollIntoView({behavior: 'instant', block: 'center'});
})()
""")
time.sleep(1.0)
capture(EVIDENCE_DIR / "area_09" / "DEF-04_after.png")

# 7. Tab 3: Trazabilidad PMO (DEF-05 AFTER)
print("Navegando a Tab 3 (Trazabilidad PMO)...")
eval_js("""
(() => {
    const tabs = Array.from(document.querySelectorAll('button[data-baseweb="tab"]'));
    if (tabs.length >= 3) tabs[2].click();
})()
""")
time.sleep(2.0)
eval_js("window.scrollTo(0, 0);")
time.sleep(1.0)
capture(EVIDENCE_DIR / "area_10" / "DEF-05_after.png")

# 8. Reinicio y vuelta a Tab 1: Probar DEF-02 AFTER (Área 07)
print("Probando reinicio 'Adaptar Nuevo Documento'...")
eval_js("""
(() => {
    const tabs = Array.from(document.querySelectorAll('button[data-baseweb="tab"]'));
    if (tabs.length >= 1) tabs[0].click();
})()
""")
time.sleep(1.5)
click_button_by_text("Adaptar Nuevo Documento")
time.sleep(2.0)
eval_js("window.scrollTo(0, 0);")
time.sleep(1.0)
capture(EVIDENCE_DIR / "area_07" / "DEF-02_after.png")

print("✅ Todas las evidencias AFTER han sido capturadas exitosamente.")
