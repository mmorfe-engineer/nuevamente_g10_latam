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
        # Cerrar pestañas viejas si existen
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

    def capture_screenshot(self, filepath):
        params = {"format": "png"}
        res = self.send("Page.captureScreenshot", params)
        data = base64.b64decode(res["data"])
        with open(filepath, "wb") as f:
            f.write(data)
        print(f"Saved: {filepath} ({len(data)} bytes)")

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
        print(f"Clicked on '{text}' ({tag}): {res}")
        return res

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

def main():
    client = CDPClient("http://localhost:8501")
    print("Conectado a Streamlit en http://localhost:8501...")
    time.sleep(3)

    # 1. Seleccionar 'Pegar Texto Libre'
    print("Seleccionando 'Pegar Texto Libre'...")
    client.evaluate("Array.from(document.querySelectorAll('div[data-testid=\"stRadio\"] label')).find(l => l.innerText.includes('Pegar Texto Libre')).click()")
    time.sleep(2)

    # 2. Inyectar documento extenso de 120,000 caracteres (~150 fragmentos)
    print("Inyectando documento extenso (~120,000 caracteres)...")
    doc_paragraph = (
        "En la arquitectura de nube Oracle Cloud Infrastructure (OCI), una Virtual Cloud Network (VCN) "
        "constituye una red privada y aislada definida por software. Permite gobernar subredes públicas y privadas, "
        "tablas de enrutamiento con Internet Gateways y NAT Gateways, Service Gateways para Object Storage, "
        "y listas de seguridad (Security Lists) o Network Security Groups (NSG) para reglas stateful y stateless. "
    )
    doc_extenso = doc_paragraph * 500  # ~120,000 caracteres
    doc_json = json.dumps(doc_extenso)

    inject_js = f"""
    (() => {{
        const ta = document.querySelector('textarea');
        if (!ta) return false;
        const proto = window.HTMLTextAreaElement.prototype;
        const nativeSetter = Object.getOwnPropertyDescriptor(proto, 'value').set;
        nativeSetter.call(ta, {doc_json});
        ta.dispatchEvent(new Event('input', {{ bubbles: true }}));
        ta.dispatchEvent(new Event('change', {{ bubbles: true }}));
        ta.focus();
        ta.dispatchEvent(new KeyboardEvent('keydown', {{ key: 'Enter', ctrlKey: true, bubbles: true }}));
        ta.blur();
        return true;
    }})()
    """
    client.evaluate(inject_js)
    time.sleep(3)

    # Capturar 1: Aviso de documento extenso en Paso 1
    client.scroll_to(450)
    time.sleep(1)
    f_aviso = SCREENSHOT_DIR / "01_aviso_documento_extenso_80chunks.png"
    client.capture_screenshot(f_aviso)

    # Capturar 2: Paso 3 con estimación previa sobre el botón
    client.scroll_to(800)
    time.sleep(1)
    f_step3_aviso = SCREENSHOT_DIR / "01_paso3_aviso_tiempo_estimado.png"
    client.capture_screenshot(f_step3_aviso)

    # 3. Disparar generación
    print("Iniciando generación con botón principal...")
    client.click_at_text("Generar Material Didáctico Adaptado")
    
    # Capturar Fase 1 en progreso y restantes en espera
    time.sleep(0.8)
    f_fase1 = SCREENSHOT_DIR / "02_indicador_fase1_progreso.png"
    client.capture_screenshot(f_fase1)

    # Capturar Fase 2 en progreso con conteo de fragmentos
    time.sleep(2.0)
    f_fase2 = SCREENSHOT_DIR / "02_indicador_fase2_conteo_fragmentos.png"
    client.capture_screenshot(f_fase2)

    # Esperar finalización de la generación (<30 segundos)
    print("Esperando finalización de la generación...")
    for sec in range(35):
        time.sleep(1)
        done = client.evaluate("document.body.innerText.includes('¡Material Didáctico Listo!')")
        if done:
            print(f"¡Generación de Lote #1 completada con éxito en {sec+1}s!")
            break

    time.sleep(2)

    # Capturar 3A: Tab 1 Encabezado y KPIs en vivo
    client.scroll_to(0)
    time.sleep(1)
    f_tab1_kpis = SCREENSHOT_DIR / "03_tab1_encabezado_kpis.png"
    client.capture_screenshot(f_tab1_kpis)

    # Capturar 3B: Banner de porción procesada declarada y Flashcards
    client.scroll_to(480)
    time.sleep(1)
    f_tab1_porcion = SCREENSHOT_DIR / "03_resultados_porcion_declarada_tab1.png"
    client.capture_screenshot(f_tab1_porcion)

    # Capturar 3C: Botones SM-2 y botón '➕ Lote Adicional'
    client.scroll_to(900)
    time.sleep(1)
    f_tab1_lote_btn = SCREENSHOT_DIR / "03_flashcards_lote_adicional_visible.png"
    client.capture_screenshot(f_tab1_lote_btn)

    # 4. Probar y capturar el avance con '➕ Lote Adicional'
    print("Haciendo clic en '➕ Lote Adicional'...")
    client.click_at_text("Lote Adicional")
    
    # Esperar procesamiento del lote 2 (<25s)
    print("Esperando procesamiento del Lote #2...")
    for sec in range(30):
        time.sleep(1)
        is_lote2 = client.evaluate("document.body.innerText.includes('Lote representativo #2')")
        if is_lote2:
            print(f"¡Lote #2 procesado con éxito en {sec+1}s!")
            break

    time.sleep(2)
    client.scroll_to(480)
    time.sleep(1)
    f_lote2 = SCREENSHOT_DIR / "04_lote2_adicional_procesado.png"
    client.capture_screenshot(f_lote2)

    client.close()
    print("\n✅ TODAS LAS CAPTURAS DEL FLUJO DINÁMICO COMPLETADAS CON ÉXITO.")

if __name__ == "__main__":
    main()
