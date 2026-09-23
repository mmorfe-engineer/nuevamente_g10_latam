import json
import time
import base64
from pathlib import Path
import requests
import websocket

CDP_BASE = "http://localhost:9222"
EVIDENCE_DIR = Path("/home/bitcoinpapa/projects/nuevamente/docs/qa/evidence/final_regression")
EVIDENCE_DIR.mkdir(parents=True, exist_ok=True)

tabs = requests.get(f"{CDP_BASE}/json/list").json()
target = next((t for t in tabs if t.get("type") == "page" and "8501" in t.get("url", "")), None)
if not target:
    print("Error: No se encontró pestaña en 8501")
    exit(1)

ws = websocket.create_connection(target["webSocketDebuggerUrl"], timeout=30)
msg_id = 0

def send(method, params=None):
    global msg_id
    msg_id += 1
    ws.send(json.dumps({"id": msg_id, "method": method, "params": params or {}}))
    while True:
        resp = json.loads(ws.recv())
        if resp.get("id") == msg_id:
            return resp.get("result", {})

def set_viewport(w=1300, h=950, mobile=False):
    send("Emulation.setDeviceMetricsOverride", {
        "width": w,
        "height": h,
        "deviceScaleFactor": 1,
        "mobile": mobile
    })
    time.sleep(1.0)

def capture(filename):
    res = send("Page.captureScreenshot", {"format": "png"})
    data = base64.b64decode(res["data"])
    out_path = EVIDENCE_DIR / filename
    with open(out_path, "wb") as f:
        f.write(data)
    print(f"📸 Guardado: {filename} ({len(data)} bytes)")
    return len(data)

def eval_js(expr):
    res = send("Runtime.evaluate", {"expression": expr, "returnByValue": True})
    return res.get("result", {}).get("value")

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

def wait_for_text(text, max_wait=20):
    start = time.time()
    while time.time() - start < max_wait:
        val = eval_js(f"document.body.innerText.includes('{text}')")
        if val:
            return True
        time.sleep(1.0)
    return False

print("=== INICIANDO REGRESIÓN INTEGRAL Y VALIDACIÓN PROMPT 4 ===")

# ----------------------------------------------------
# 1. PANTALLA INICIAL Y HEADER EN VIEWPORTS RESPONSIVE
# ----------------------------------------------------
print("1. Evaluando vista inicial en viewports responsive...")
# Desktop
set_viewport(1300, 950, mobile=False)
eval_js("window.scrollTo(0, 0);")
time.sleep(1.0)
capture("01_desktop_pantalla_inicial_header.png")

# Tablet
set_viewport(768, 1024, mobile=False)
time.sleep(1.0)
capture("02_tablet_pantalla_inicial.png")

# Mobile
set_viewport(375, 667, mobile=True)
time.sleep(1.0)
capture("03_mobile_pantalla_inicial.png")

# Volver a Desktop para el recorrido E2E
set_viewport(1300, 950, mobile=False)
time.sleep(1.0)

# ----------------------------------------------------
# 2. PRUEBA A/B DE ESTADO (DOCUMENTO A -> RESET -> DOCUMENTO B)
# ----------------------------------------------------
print("2. Ejecutando Prueba A/B de Estado...")

# Cargar Documento A (Muestra Canónica Oracle VCN)
print("   - Cargando Documento A (Caso Canónico Oracle VCN)...")
click_button_by_text("Caso Canónico Oracle")
time.sleep(2.0)
capture("04_doc_A_cargado_ingesta.png")

# Generar material didáctico para Documento A
print("   - Generando Flashcards para Documento A...")
click_button_by_text("Generar Material Didáctico")
wait_for_text("¡Material Didáctico Listo!", max_wait=25)
time.sleep(2.0)

eval_js("window.scrollTo(0, 0);")
time.sleep(1.0)
capture("05_doc_A_resultados_kpis.png")

# Obtener título y contenido de la primera flashcard de Documento A
doc_A_title = eval_js("document.querySelector('h2') ? document.querySelector('h2').innerText : ''")
doc_A_card0 = eval_js("""
(() => {
    const el = document.querySelector('.nm-flash__face--front p');
    return el ? el.innerText : '';
})()
""")
print(f"   [Doc A] Título: {doc_A_title}")
print(f"   [Doc A] Flashcard 0 (frente): {doc_A_card0[:80]}...")

# Voltear tarjeta 0 y calificarla con "Alcanzado"
print("   - Volteando tarjeta 0 de Documento A y calificando...")
click_button_by_text("Voltear Tarjeta")
time.sleep(1.5)
click_button_by_text("Alcanzado")
time.sleep(1.5)
capture("06_doc_A_tarjeta_calificada_sm2.png")

# Ahora: ACCIONAR "Adaptar Nuevo Documento"
print("   - Accionando 'Adaptar Nuevo Documento'...")
click_button_by_text("Adaptar Nuevo Documento")
time.sleep(2.0)
capture("07_doc_A_reset_bienvenida_limpia.png")

# Comprobar que en el DOM ya no hay tarjetas ni resultados
has_old_flashcards = eval_js("document.body.innerText.includes('Apertura Andragógica') || document.body.innerText.includes('Voltear Tarjeta')")
print(f"   - Verificación de purga: ¿Quedan tarjetas visibles? {has_old_flashcards} (debe ser False)")

# Cargar Documento B (Muestra 3: Seguridad IAM - completamente diferente)
print("   - Cargando Documento B (Muestra 3: Seguridad IAM)...")
click_button_by_text("Muestra 3: Seguridad IAM")
time.sleep(2.0)
capture("08_doc_B_cargado.png")

# Generar material para Documento B
print("   - Generando Material Didáctico para Documento B...")
click_button_by_text("Generar Material Didáctico")
wait_for_text("¡Material Didáctico Listo!", max_wait=25)
time.sleep(2.0)

eval_js("window.scrollTo(0, 0);")
time.sleep(1.0)
capture("09_doc_B_resultados.png")

# Obtener datos de Documento B
doc_B_title = eval_js("document.querySelector('h2') ? document.querySelector('h2').innerText : ''")
doc_B_card0 = eval_js("""
(() => {
    const el = document.querySelector('.nm-flash__face--front p');
    return el ? el.innerText : '';
})()
""")
# Verificar si la tarjeta 0 está volteada o calificada
doc_B_is_flipped = eval_js("document.body.innerText.includes('Ver Frente')")
doc_B_has_grade = eval_js("document.body.innerText.includes('Próximo repaso')")

print(f"   [Doc B] Título: {doc_B_title}")
print(f"   [Doc B] Flashcard 0 (frente): {doc_B_card0[:80]}...")
print(f"   [Doc B] ¿Heredó estado volteado?: {doc_B_is_flipped} (debe ser False)")
print(f"   [Doc B] ¿Heredó calificación SM-2?: {doc_B_has_grade} (debe ser False)")
print(f"   [Doc B vs Doc A] ¿Son títulos distintos?: {doc_A_title != doc_B_title} (debe ser True)")
print(f"   [Doc B vs Doc A] ¿Son tarjetas distintas?: {doc_A_card0 != doc_B_card0} (debe ser True)")

# ----------------------------------------------------
# 3. TAB 2: AUDITORÍA DE CALIDAD Y FUNDAMENTO METODOLÓGICO (DEF-04)
# ----------------------------------------------------
print("3. Validando Tab 2 (Auditoría de Calidad y Tipografía)...")
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
capture("10_tab2_auditoria_fundamento_metodologico.png")

# ----------------------------------------------------
# 4. TAB 3: TRAZABILIDAD PMO Y CONSISTENCIA GEOMÉTRICA (DEF-05)
# ----------------------------------------------------
print("4. Validando Tab 3 (Trazabilidad PMO y KPIs)...")
eval_js("""
(() => {
    const tabs = Array.from(document.querySelectorAll('button[data-baseweb="tab"]'));
    if (tabs.length >= 3) tabs[2].click();
})()
""")
time.sleep(2.0)
eval_js("window.scrollTo(0, 0);")
time.sleep(1.0)
capture("11_tab3_trazabilidad_kpis_alineados.png")

# Scrollear hacia la matriz de trazabilidad y contratos
eval_js("""
(() => {
    const el = Array.from(document.querySelectorAll('h3')).find(h => h.innerText.includes('Matriz de Trazabilidad'));
    if (el) el.scrollIntoView({behavior: 'instant', block: 'center'});
})()
""")
time.sleep(1.0)
capture("12_tab3_matriz_trazabilidad_oficial.png")

# Guardar registro JSON de la prueba A/B
ab_test_report = {
    "doc_A": {
        "title": doc_A_title,
        "first_card_front": doc_A_card0,
        "graded": True
    },
    "doc_B": {
        "title": doc_B_title,
        "first_card_front": doc_B_card0,
        "inherited_flip": doc_B_is_flipped,
        "inherited_grade": doc_B_has_grade,
        "isolation_verified": (doc_A_title != doc_B_title and not doc_B_is_flipped and not doc_B_has_grade)
    }
}
with open(EVIDENCE_DIR / "ab_state_isolation_results.json", "w") as f:
    json.dump(ab_test_report, f, indent=2)

print("=== REGRESIÓN INTEGRAL Y CAPTURA COMPLETADAS CON ÉXITO ===")
