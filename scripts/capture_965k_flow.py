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

class CDPClient:
    def __init__(self, url="http://localhost:8501"):
        # Cerrar páginas previas
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

    # 1. Subir archivo oficial de 965,086 caracteres
    sample_file = os.path.abspath("data/samples/manual_965k_redes_oci.txt")
    print(f"Cargando archivo de 965,086 caracteres: {sample_file} ...")

    root = client.send("DOM.getDocument")["root"]["nodeId"]
    file_input = client.send("DOM.querySelector", {"nodeId": root, "selector": "input[type=\"file\"]"})["nodeId"]
    client.send("DOM.setFileInputFiles", {"files": [sample_file], "nodeId": file_input})
    time.sleep(4)

    # 2. Capturar Aviso de Documento Extenso y Estimación de Espera
    client.scroll_to(450)
    time.sleep(1)
    f_aviso = SCREENSHOT_DIR / "01_aviso_documento_extenso_80chunks.png"
    client.capture_screenshot(f_aviso)

    client.scroll_to(800)
    time.sleep(1)
    f_step3 = SCREENSHOT_DIR / "01_paso3_aviso_tiempo_estimado.png"
    client.capture_screenshot(f_step3)

    # 3. Iniciar Generación
    print("Pulsando 'Generar Material Didáctico Adaptado'...")
    client.click_at_text("Generar Material Didáctico Adaptado")

    # Capturar Fase 1 en progreso
    time.sleep(0.8)
    f_fase1 = SCREENSHOT_DIR / "02_indicador_fase1_progreso.png"
    client.capture_screenshot(f_fase1)

    # Capturar Fase 2 en progreso con conteo de fragmentos
    time.sleep(2.5)
    f_fase2 = SCREENSHOT_DIR / "02_indicador_fase2_conteo_fragmentos.png"
    client.capture_screenshot(f_fase2)

    # 4. Esperar finalización de la generación (<25s)
    print("Esperando finalización de la generación de Lote #1...")
    t_start = time.time()
    for sec in range(40):
        time.sleep(1)
        done = client.evaluate("document.body.innerText.includes('¡Material Didáctico Listo!')")
        if done:
            t_gen = time.time() - t_start
            print(f"¡Lote #1 completado exitosamente en {t_gen:.1f} segundos!")
            break

    time.sleep(2)

    # 5. Capturar Tab 1: Encabezado con KPIs activos
    client.scroll_to(0)
    time.sleep(1)
    f_kpis = SCREENSHOT_DIR / "03_tab1_encabezado_kpis.png"
    client.capture_screenshot(f_kpis)

    # Capturar Tab 1: Banner de Porción Declarada y Apertura Andragógica
    client.scroll_to(350)
    time.sleep(1)
    f_porcion = SCREENSHOT_DIR / "03_resultados_porcion_declarada_tab1.png"
    client.capture_screenshot(f_porcion)

    # Capturar Flashcard y botón de Lote Adicional
    client.scroll_to(700)
    time.sleep(1)
    f_fc = SCREENSHOT_DIR / "03_flashcards_lote_adicional_visible.png"
    client.capture_screenshot(f_fc)

    # 6. Click '➕ Lote Adicional' para procesar siguiente segmento
    print("Pulsando botón '➕ Lote Adicional'...")
    client.click_at_text("Lote Adicional")
    time.sleep(1)

    t_start2 = time.time()
    for sec in range(35):
        time.sleep(1)
        is_lote2 = client.evaluate("document.body.innerText.includes('Lote representativo #2')")
        if is_lote2:
            t_gen2 = time.time() - t_start2
            print(f"¡Lote #2 completado exitosamente en {t_gen2:.1f} segundos!")
            break

    time.sleep(2)
    client.scroll_to(350)
    time.sleep(1)
    f_lote2 = SCREENSHOT_DIR / "04_lote2_adicional_procesado.png"
    client.capture_screenshot(f_lote2)

    client.close()
    print("\n✅ CICLO COMPLETO DEL DOCUMENTO DE 965,086 CARACTERES CAPTURADO CON ÉXITO.")

if __name__ == "__main__":
    main()
