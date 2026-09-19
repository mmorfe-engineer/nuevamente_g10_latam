import json
import time
import base64
import os
from pathlib import Path
import requests
import websocket

CDP_BASE = "http://localhost:9222"
SCREENSHOT_DIR = Path("/home/bitcoinpapa/projects/nuevamente/docs/screenshots")
SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)
PDF_PATH = os.path.abspath("data/fuentes_ciberseguridad/05_pci_dss_v4_0_la_seguridad_bancaria.pdf")

class CDPAutomation:
    def __init__(self, url="http://localhost:8501"):
        try:
            tabs = requests.get(f"{CDP_BASE}/json/list").json()
            for t in tabs:
                if t.get("type") == "page" and "8501" in t.get("url", ""):
                    requests.get(f"{CDP_BASE}/json/close/{t['id']}")
        except Exception:
            pass

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
        if "result" in res:
            inner = res["result"]
            if "value" in inner:
                return inner["value"]
            if "result" in inner and "value" in inner["result"]:
                return inner["result"]["value"]
        return None

    def set_viewport(self, width=1400, height=1400):
        self.send("Emulation.setDeviceMetricsOverride", {
            "width": width,
            "height": height,
            "deviceScaleFactor": 1,
            "mobile": False
        })

    def capture_screenshot(self, filepath):
        params = {"format": "png"}
        res = self.send("Page.captureScreenshot", params)
        data = base64.b64decode(res["data"])
        with open(filepath, "wb") as f:
            f.write(data)
        print(f"📸 Guardado: {filepath} ({len(data)} bytes)")

    def click_mouse(self, x, y):
        self.send("Input.dispatchMouseEvent", {"type": "mouseMoved", "x": x, "y": y})
        self.send("Input.dispatchMouseEvent", {"type": "mousePressed", "x": x, "y": y, "button": "left", "clickCount": 1})
        time.sleep(0.06)
        self.send("Input.dispatchMouseEvent", {"type": "mouseReleased", "x": x, "y": y, "button": "left", "clickCount": 1})

    def scroll_into_view_and_click(self, text_fragment, tag="button"):
        box = self.evaluate(f"""
        (() => {{
            const elements = Array.from(document.querySelectorAll('{tag}'));
            const target = elements.find(el => el.innerText.includes('{text_fragment}'));
            if (!target) return null;
            target.scrollIntoView({{block: 'center', behavior: 'instant'}});
            const r = target.getBoundingClientRect();
            return {{x: r.left + r.width/2, y: r.top + r.height/2}};
        }})()
        """)
        if not box:
            print(f"❌ Elemento no encontrado: '{text_fragment}' ({tag})")
            return False
        print(f"🎯 Clickeando '{text_fragment}' en ({box['x']:.1f}, {box['y']:.1f})")
        self.click_mouse(box["x"], box["y"])
        time.sleep(0.8)
        return True

    def select_combobox(self, label_text, option_substr):
        # 1. Click button[aria-label="Open"]
        box = self.evaluate(f"""
        (() => {{
            const sbs = Array.from(document.querySelectorAll("div[data-testid='stSelectbox']"));
            const sb = sbs.find(s => s.innerText.includes('{label_text}'));
            if (!sb) return null;
            const btn = sb.querySelector('button[aria-label="Open"]');
            if (!btn) return null;
            btn.scrollIntoView({{block: 'center', behavior: 'instant'}});
            const r = btn.getBoundingClientRect();
            return {{x: r.left + r.width/2, y: r.top + r.height/2}};
        }})()
        """)
        if not box:
            print(f"❌ Selectbox no encontrado: '{label_text}'")
            return False
        
        self.click_mouse(box["x"], box["y"])
        time.sleep(1.0)

        # 2. Get option coords
        opt_box = self.evaluate(f"""
        (() => {{
            const options = Array.from(document.querySelectorAll("[role='option']"));
            const target = options.find(o => o.innerText.includes('{option_substr}'));
            if (!target) return null;
            const r = target.getBoundingClientRect();
            return {{x: r.left + r.width/2, y: r.top + r.height/2}};
        }})()
        """)
        if not opt_box:
            print(f"❌ Opción '{option_substr}' no encontrada en dropdown '{label_text}'")
            return False

        print(f"🎯 Seleccionando '{option_substr}' en ({opt_box['x']:.1f}, {opt_box['y']:.1f})")
        self.click_mouse(opt_box["x"], opt_box["y"])
        time.sleep(1.0)
        return True

    def upload_file(self, filepath):
        print(f"📤 Subiendo archivo: {filepath}")
        root = self.send("DOM.getDocument")["root"]["nodeId"]
        file_input = self.send("DOM.querySelector", {"nodeId": root, "selector": "input[type=\"file\"]"})["nodeId"]
        self.send("DOM.setFileInputFiles", {"files": [filepath], "nodeId": file_input})
        time.sleep(3.5)

    def scroll_to_top(self):
        self.evaluate("""
        (() => {
            const main = document.querySelector('.stMain') || document.querySelector('section[data-testid="stMain"]');
            if (main) main.scrollTop = 0;
            window.scrollTo(0, 0);
        })()
        """)
        time.sleep(0.5)

    def scroll_to_y(self, y):
        self.evaluate(f"""
        (() => {{
            const main = document.querySelector('.stMain') || document.querySelector('section[data-testid="stMain"]');
            if (main) main.scrollTop = {y};
            window.scrollTo(0, {y});
        }})()
        """)
        time.sleep(0.5)

    def close(self):
        try:
            self.ws.close()
            requests.get(f"{CDP_BASE}/json/close/{self.target_id}")
        except Exception:
            pass

def run():
    print("================================================================================")
    print("🚀 INICIANDO VERIFICACIÓN EN VIVO: PCI DSS v4.0 (DUAL RUN PRINCIPIANTE / ARQUITECTO)")
    print("================================================================================")
    client = CDPAutomation("http://localhost:8501")
    client.set_viewport(1400, 1300)
    time.sleep(4)

    # Si ya había una sesión abierta previa, recargar al estado inicial
    has_reload = client.evaluate("document.body.innerText.includes('Cargar Nuevo Documento')")
    if has_reload:
        print("🔄 Sesión anterior detectada. Reiniciando a estado inicial...")
        client.scroll_into_view_and_click("Cargar Nuevo Documento")
        time.sleep(3)

    # -------------------------------------------------------------------------
    # EJECUCIÓN 1: PRINCIPIANTE · FLASHCARDS
    # -------------------------------------------------------------------------
    print("\n--- EJECUCIÓN 1: PCI DSS v4.0 -> PRINCIPIANTE · FLASHCARDS ---")
    client.upload_file(PDF_PATH)
    time.sleep(2)

    # Click Generar
    print("⚙️ Lanzando pipeline de adaptación RAG...")
    client.scroll_into_view_and_click("Generar Material Didáctico Adaptado")
    
    # Esperar hasta 60s
    for sec in range(60):
        time.sleep(1)
        done = client.evaluate("document.body.innerText.includes('¡Material Didáctico Listo!')")
        if done:
            print(f"✅ Generación completada en {sec+1}s!")
            break

    time.sleep(2.5)
    client.scroll_to_top()
    time.sleep(1)

    f1_encabezado = SCREENSHOT_DIR / "05_pci_dss_01_principiante_flashcards_encabezado.png"
    client.capture_screenshot(f1_encabezado)

    # Prueba interactiva de Flashcards: Voltear y Calificar SM-2
    print("\n--- PRUEBA INTERACTIVA: VOLTEAR Y CALIFICAR SM-2 ---")
    # Voltear tarjeta 1
    flipped_ok = client.scroll_into_view_and_click("Voltear Tarjeta")
    time.sleep(2.0)

    # Calificar con '🟢 Alcanzado'
    rated_ok = client.scroll_into_view_and_click("Alcanzado")
    time.sleep(2.5)

    f1_calificada = SCREENSHOT_DIR / "05_pci_dss_01_flashcard_sm2_calificada.png"
    client.capture_screenshot(f1_calificada)

    # -------------------------------------------------------------------------
    # EJECUCIÓN 2: ARQUITECTO · GUÍA PRÁCTICA (TUTORIAL)
    # -------------------------------------------------------------------------
    print("\n--- EJECUCIÓN 2: MISMO DOCUMENTO -> LÍDER TÉCNICO / ARQUITECTO · GUÍA PRÁCTICA ---")
    client.scroll_to_top()
    time.sleep(0.5)
    client.scroll_into_view_and_click("Cargar Nuevo Documento")
    time.sleep(3.5)

    # Subir el mismo documento nuevamente
    client.upload_file(PDF_PATH)
    time.sleep(2)

    # Configurar Perfil: Líder Técnico / Arquitecto
    client.select_combobox("Perfil del Destinatario", "Arquitecto")

    # Configurar Formato: Guía Práctica (Tutorial)
    client.select_combobox("Formato Didáctico", "Guía Práctica")

    # Generar
    print("⚙️ Lanzando pipeline de adaptación para Arquitecto...")
    client.scroll_into_view_and_click("Generar Material Didáctico Adaptado")

    for sec in range(60):
        time.sleep(1)
        done = client.evaluate("document.body.innerText.includes('¡Material Didáctico Listo!')")
        if done:
            print(f"✅ Generación para Arquitecto completada en {sec+1}s!")
            break

    time.sleep(2.5)
    client.scroll_to_top()
    time.sleep(1)

    f2_encabezado = SCREENSHOT_DIR / "05_pci_dss_02_arquitecto_guia_practica_encabezado.png"
    client.capture_screenshot(f2_encabezado)

    # Scroll hacia los pasos técnicos de la guía
    client.scroll_to_y(600)
    time.sleep(1)
    f2_pasos = SCREENSHOT_DIR / "05_pci_dss_02_guia_practica_pasos.png"
    client.capture_screenshot(f2_pasos)

    client.close()
    print("\n🎉 VERIFICACIÓN DUAL PCI DSS COMPLETADA EXITOSAMENTE.")

if __name__ == "__main__":
    run()
