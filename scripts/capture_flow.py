import json
import time
import base64
from pathlib import Path
import requests
import websocket

CDP_BASE = "http://localhost:9222"
SCREENSHOT_DIR = Path("/home/bitcoinpapa/projects/nuevamente/docs/screenshots")
SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)

class CDPClient:
    def __init__(self, url="http://localhost:8501"):
        r = requests.put(f"{CDP_BASE}/json/new?{url}")
        target = r.json()
        self.target_id = target["id"]
        self.ws_url = target["webSocketDebuggerUrl"]
        self.ws = websocket.create_connection(self.ws_url, timeout=60)
        self.msg_id = 0
        self.send("Page.enable")
        self.send("Runtime.enable")
        self.send("DOM.enable")

    def send(self, method, params=None):
        self.msg_id += 1
        payload = {"id": self.msg_id, "method": method, "params": params or {}}
        self.ws.send(json.dumps(payload))
        while True:
            resp = json.loads(self.ws.recv())
            if resp.get("id") == self.msg_id:
                return resp.get("result", {})

    def evaluate(self, expr):
        res = self.send("Runtime.evaluate", {"expression": expr, "returnByValue": True, "awaitPromise": True})
        return res.get("result", {}).get("value")

    def capture_screenshot(self, filepath):
        params = {"format": "png"}
        res = self.send("Page.captureScreenshot", params)
        data = base64.b64decode(res["data"])
        with open(filepath, "wb") as f:
            f.write(data)
        print(f"Saved: {filepath} ({len(data)} bytes)")

    def click_at_text(self, text, tag="button"):
        box = self.evaluate(f"""
        (() => {{
            const elements = Array.from(document.querySelectorAll('{tag}'));
            const target = elements.find(el => el.innerText.includes('{text}'));
            if (!target) return null;
            target.scrollIntoView({{behavior: 'instant', block: 'center'}});
            const rect = target.getBoundingClientRect();
            return {{ x: Math.round(rect.left + rect.width / 2), y: Math.round(rect.top + rect.height / 2) }};
        }})()
        """)
        if not box:
            print(f"Could not find element with text '{text}'")
            return False
        
        time.sleep(0.3)
        box = self.evaluate(f"""
        (() => {{
            const elements = Array.from(document.querySelectorAll('{tag}'));
            const target = elements.find(el => el.innerText.includes('{text}'));
            if (!target) return null;
            const rect = target.getBoundingClientRect();
            return {{ x: Math.round(rect.left + rect.width / 2), y: Math.round(rect.top + rect.height / 2) }};
        }})()
        """)
        x, y = box["x"], box["y"]
        self.send("Input.dispatchMouseEvent", {"type": "mouseMoved", "x": x, "y": y})
        self.send("Input.dispatchMouseEvent", {"type": "mousePressed", "x": x, "y": y, "button": "left", "clickCount": 1})
        self.send("Input.dispatchMouseEvent", {"type": "mouseReleased", "x": x, "y": y, "button": "left", "clickCount": 1})
        print(f"Dispatched click on '{text}' at ({x}, {y})")
        return True

    def click_tab(self, tab_index):
        click_script = f"""
        (() => {{
            const tabs = Array.from(document.querySelectorAll('button[data-baseweb="tab"]'));
            if (tabs[{tab_index}]) {{
                tabs[{tab_index}].click();
                return true;
            }}
            return false;
        }})()
        """
        res = self.evaluate(click_script)
        print(f"Clicked tab {tab_index}: {res}")
        return res

    def scroll_to(self, y=0):
        self.evaluate(f"window.scrollTo(0, {y});")
        time.sleep(0.5)

    def close(self):
        try:
            self.ws.close()
            requests.get(f"{CDP_BASE}/json/close/{self.target_id}")
        except Exception:
            pass

def run():
    client = CDPClient("http://localhost:8501")
    print("Navigating to http://localhost:8501 ...")
    time.sleep(4)
    
    # 1. Capture Pantalla de Bienvenida (Estación de Ingesta O-01 + 3 Muestras O-12 + KPIs Aún sin medir)
    f1 = SCREENSHOT_DIR / "01_pantalla_bienvenida.png"
    client.capture_screenshot(f1)
    
    # Also capture lower half showing uploader & 4 parameters
    client.scroll_to(450)
    time.sleep(1)
    f1_params = SCREENSHOT_DIR / "01_pantalla_bienvenida_parametros.png"
    client.capture_screenshot(f1_params)
    
    # 2. Click Canonical Button: "⚡ Caso Canónico Oracle: Redes VCN (Pág. 4)"
    print("Clicking canonical demo button...")
    client.scroll_to(0)
    client.click_at_text("Caso Canónico Oracle")
    time.sleep(3)
    
    # 3. Click Generar Material Didáctico
    print("Clicking generate button...")
    client.click_at_text("Generar Material Didáctico")
    
    # Wait for generation to finish
    print("Waiting for generation to finish...")
    for i in range(30):
        time.sleep(1)
        has_intro = client.evaluate("document.body.innerText.includes('Apertura Andragógica')")
        if has_intro:
            print(f"Generation completed after {i+1}s!")
            break
    
    time.sleep(2)
    client.scroll_to(0)
    
    # 4. Capture Pantalla 2: Flashcards Generadas (con sector dinámico, sin NIST, KPIs actualizados en vivo)
    f2 = SCREENSHOT_DIR / "02_flashcards_generadas.png"
    client.capture_screenshot(f2)
    
    # Scroll slightly down to show flashcard body and rating bar
    client.scroll_to(420)
    time.sleep(1)
    f2_card = SCREENSHOT_DIR / "02_flashcard_detalle_sm2.png"
    client.capture_screenshot(f2_card)
    
    # 5. Capture Pantalla 3: Tab de Auditoría y Métricas
    print("Switching to Auditoria tab...")
    client.scroll_to(0)
    client.click_tab(1)
    time.sleep(2)
    client.scroll_to(0)
    f3 = SCREENSHOT_DIR / "03_auditoria_metricas.png"
    client.capture_screenshot(f3)
    
    # 6. Capture Pantalla 4: Tab de Trazabilidad PMO y Matriz
    print("Switching to Trazabilidad PMO tab...")
    client.click_tab(2)
    time.sleep(2)
    client.scroll_to(0)
    f4 = SCREENSHOT_DIR / "04_trazabilidad_pmo_matriz.png"
    client.capture_screenshot(f4)
    
    client.close()
    print("All captures completed successfully!")

if __name__ == "__main__":
    run()
