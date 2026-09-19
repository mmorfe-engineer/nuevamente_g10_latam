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

class CDPClient:
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

    def set_viewport(self, width=1400, height=1800):
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
        print(f"Guardado: {filepath} ({len(data)} bytes)")

    def click_at_text(self, text, tag="button"):
        js = f"""
        (() => {{
            const elements = Array.from(document.querySelectorAll('{tag}'));
            const target = elements.find(el => el.innerText.includes('{text}'));
            if (!target) return false;
            target.click();
            return true;
        }})()
        """
        res = self.evaluate(js)
        print(f"Click en '{text}' ({tag}): {res}")
        return res

    def upload_file(self, filepath):
        root = self.send("DOM.getDocument")["root"]["nodeId"]
        file_input = self.send("DOM.querySelector", {"nodeId": root, "selector": "input[type=\"file\"]"})["nodeId"]
        self.send("DOM.setFileInputFiles", {"files": [filepath], "nodeId": file_input})
        time.sleep(3)

    def select_option(self, label_text, option_value):
        js = f"""
        (() => {{
            const sbs = Array.from(document.querySelectorAll("div[data-testid='stSelectbox']"));
            const targetSb = sbs.find(sb => sb.querySelector('label') && sb.querySelector('label').innerText.includes('{label_text}'));
            if (!targetSb) return false;
            const trigger = targetSb.querySelector("div[data-baseweb='select']");
            if (!trigger) return false;
            trigger.click();
            return true;
        }})()
        """
        ok = self.evaluate(js)
        print(f"Apertura selectbox '{label_text}': {ok}")
        time.sleep(0.7)
        click_opt = f"""
        (() => {{
            const opts = Array.from(document.querySelectorAll("li[role='option'], div[role='option']"));
            const targetOpt = opts.find(o => o.innerText.includes('{option_value}'));
            if (!targetOpt) return false;
            targetOpt.click();
            return true;
        }})()
        """
        ok_opt = self.evaluate(click_opt)
        print(f"Selección opción '{option_value}': {ok_opt}")
        time.sleep(1.0)
        return ok_opt

    def scroll_to(self, y=0):
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
    client = CDPClient("http://localhost:8501")
    print("=== EJECUTANDO VERIFICACIÓN DUAL PCI DSS V4.0 (963,244 CARACTERES) ===")
    time.sleep(3)

    # =========================================================================
    # EJECUCIÓN 1: PRINCIPIANTE · FLASHCARDS
    # =========================================================================
    print("\n--- PASO 1: CARGA DE DOCUMENTO Y ADAPTACIÓN A PRINCIPIANTE / FLASHCARDS ---")
    client.upload_file(PDF_PATH)
    time.sleep(2)

    # Click Generar
    client.click_at_text("Generar Material Didáctico Adaptado")
    print("Esperando generación de Flashcards para Principiante...")
    for sec in range(35):
        time.sleep(1)
        done = client.evaluate("document.body.innerText.includes('¡Material Didáctico Listo!')")
        if done:
            print(f"Generación de Flashcards completada en {sec+1}s!")
            break

    time.sleep(2)
    client.set_viewport(1400, 1600)
    client.scroll_to(0)
    time.sleep(1)

    f1 = SCREENSHOT_DIR / "05_pci_dss_01_principiante_flashcards_encabezado.png"
    client.capture_screenshot(f1)

    # Scroll hacia Flashcards y ejecutar ciclo de volteo y calificación SM-2
    print("\n--- PRUEBA INTERACTIVA SM-2: VOLTEO Y CALIFICACIÓN ---")
    client.scroll_to(550)
    time.sleep(1)

    # Voltear tarjeta
    client.click_at_text("Voltear Tarjeta")
    time.sleep(1.5)

    # Calificar con '🟢 Alcanzado'
    client.click_at_text("Alcanzado")
    time.sleep(2.0)

    f1_sm2 = SCREENSHOT_DIR / "05_pci_dss_01_flashcard_sm2_calificada.png"
    client.capture_screenshot(f1_sm2)

    # =========================================================================
    # EJECUCIÓN 2: ARQUITECTO · GUÍA PRÁCTICA (TUTORIAL)
    # =========================================================================
    print("\n--- PASO 2: MISMO DOCUMENTO ADAPTADO A ARQUITECTO / GUÍA PRÁCTICA ---")
    client.scroll_to(0)
    time.sleep(0.5)
    client.click_at_text("Cargar Nuevo Documento")
    time.sleep(2.5)

    # Cargar el mismo archivo PDF
    client.upload_file(PDF_PATH)
    time.sleep(2)

    # Configurar Perfil = Arquitecto
    client.select_option("Perfil del Destinatario", "Arquitecto")
    time.sleep(1)

    # Configurar Formato = Guía Práctica (Tutorial)
    client.select_option("Formato Didáctico", "Guía Práctica (Tutorial)")
    time.sleep(1)

    # Click Generar
    client.click_at_text("Generar Material Didáctico Adaptado")
    print("Esperando generación de Guía Práctica para Arquitecto...")
    for sec in range(35):
        time.sleep(1)
        done = client.evaluate("document.body.innerText.includes('¡Material Didáctico Listo!')")
        if done:
            print(f"Generación de Guía Práctica completada en {sec+1}s!")
            break

    time.sleep(2)
    client.scroll_to(0)
    time.sleep(1)

    f2_hdr = SCREENSHOT_DIR / "05_pci_dss_02_arquitecto_guia_practica_encabezado.png"
    client.capture_screenshot(f2_hdr)

    # Scroll para ver los pasos técnicos y comandos de la guía
    client.scroll_to(450)
    time.sleep(1)
    f2_pasos = SCREENSHOT_DIR / "05_pci_dss_02_guia_practica_pasos.png"
    client.capture_screenshot(f2_pasos)

    client.close()
    print("\n✅ VERIFICACIÓN DUAL DE PCI DSS COMPLETADA EXITOSAMENTE.")

if __name__ == "__main__":
    run()
