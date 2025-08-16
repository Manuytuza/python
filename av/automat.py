#!/usr/bin/env python3
# automat.py — Automatiza TWR-0281: descarga "Hoy" y "Este mes" y extrae "Venta Neta"
import os
import time
import shutil
from pathlib import Path
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# ---------------- CONFIG ----------------
# Ajusta estos valores antes de ejecutar
CHQ_FAVORITES_URL = "https://macc-prod-mx-chq.teamworkinsight.com/#/ReportsFavoritesList"
TWR_CODE = "TWR-0281"
# Usa variables de entorno o cambia aquí:
USUARIO = os.getenv("CHQ_USER", "mytusa")
CLAVE = os.getenv("CHQ_PASS", "72461017")
# Ruta donde Chrome descarga archivos
DOWNLOAD_DIR = str(Path.home() / "Downloads")
# Ruta de chromedriver si lo tienes local; deja "" para usar webdriver-manager fallback
CHROMEDRIVER_PATH = "/Users/maccenterarequipa/Documents/chromedriver"
# nombres finales
OUT_HOY = "venta_hoy.xlsx"
OUT_MES = "venta_mes.xlsx"
# equipo vendidos por defecto
EQUIPOS_VENDIDOS = 0

# timeouts
WAIT_SHORT = 2
WAIT_MED = 8
WAIT_LONG = 30

# ------------- HELPERS -------------
def start_driver(download_dir: str, chromedriver_path: str = ""):
    opts = Options()
    prefs = {
        "download.default_directory": download_dir,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "plugins.always_open_pdf_externally": True
    }
    opts.add_experimental_option("prefs", prefs)
    opts.add_argument("--start-maximized")
    # opts.add_argument("--headless=new")  # descomenta si quieres sin UI

    if chromedriver_path and Path(chromedriver_path).exists():
        service = Service(chromedriver_path)
    else:
        # fallback: webdriver-manager (instala chromedriver automáticamente)
        try:
            from webdriver_manager.chrome import ChromeDriverManager
            service = Service(ChromeDriverManager().install())
        except Exception:
            raise RuntimeError("Chromedriver no encontrado y webdriver-manager no disponible.")

    driver = webdriver.Chrome(service=service, options=opts)
    driver.implicitly_wait(2)
    return driver

def files_set(folder: str):
    p = Path(folder)
    return set([f for f in p.iterdir() if f.is_file()])

def wait_for_new_file(before_set, folder: str, timeout=40):
    target = Path(folder)
    waited = 0
    while waited < timeout:
        now = files_set(folder)
        new = now - before_set
        # ignorar archivos temporales incompletos
        incomplete = list(target.glob("*.crdownload")) + list(target.glob("*.part"))
        if new and not incomplete:
            # retornar el file más reciente de 'new'
            new_list = sorted(list(new), key=lambda p: p.stat().st_mtime, reverse=True)
            return new_list[0]
        time.sleep(1)
        waited += 1
    return None

def wait_file_stable(path: Path, checks=3, interval=1.0):
    # Espera que el archivo deje de crecer (escritur estable)
    try:
        last_size = path.stat().st_size
    except Exception:
        return False
    for _ in range(checks):
        time.sleep(interval)
        try:
            s = path.stat().st_size
        except Exception:
            return False
        if s != last_size:
            last_size = s
        else:
            return True
    # última comprobación
    return path.exists()

def choose_run_button(driver):
    # intenta varios selectores conocidos
    cand_selectors = [
        "button[data-bind*='onRunClick']",
        "button[localizedlabel*='Run']",
    ]
    for sel in cand_selectors:
        try:
            el = driver.find_element(By.CSS_SELECTOR, sel)
            if el and el.is_enabled():
                return el
        except Exception:
            pass
    # fallback: por texto
    try:
        buttons = driver.find_elements(By.TAG_NAME, "button")
        for b in buttons:
            if b.text and "ejecut" in b.text.lower() or "run" in b.text.lower():
                return b
    except Exception:
        pass
    return None

def click_date_option(driver, option_texts):
    """
    option_texts: lista de variantes a buscar (ej. ['Hoy', 'Today'])
    hace click en el selector de fecha y elige la opción que coincida.
    """
    # selector del span que muestra el filtro actual (según tu HTML)
    try:
        span = WebDriverWait(driver, WAIT_MED).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "span[data-bind*='getSelectedValueDescription'], span[title]"))
        )
        span.click()
    except Exception:
        # intentar abrir cualquier dropdown cercano
        try:
            # alternativa: hacer click sobre el control padre
            control = driver.find_element(By.CSS_SELECTOR, "div.date-filter, div.report-date, .date-picker")
            control.click()
        except Exception:
            pass

    # esperar que aparezcan opciones (li, div, button...)
    time.sleep(0.6)
    candidates = driver.find_elements(By.XPATH, "//li | //ul//li | //div[contains(@class,'dropdown')]//div | //button")
    option_texts_lower = [t.lower() for t in option_texts]
    for elem in candidates:
        try:
            txt = (elem.text or "").strip().lower()
            if not txt:
                continue
            for opt in option_texts_lower:
                if opt in txt:
                    try:
                        elem.click()
                        return True
                    except Exception:
                        # intentar con JS click
                        driver.execute_script("arguments[0].click();", elem)
                        return True
        except Exception:
            continue
    return False

def find_column_name(df: pd.DataFrame, keywords):
    cols = list(df.columns)
    cols_lower = [c.lower() for c in cols]
    # Score by occurrences of keywords
    best = None
    best_score = 0
    for i, c in enumerate(cols_lower):
        score = sum(1 for k in keywords if k in c)
        if score > best_score:
            best_score = score
            best = cols[i]
    return best

def clean_to_float_series(s):
    def clean_val(v):
        try:
            if pd.isna(v):
                return None
            if isinstance(v, (int, float)):
                return float(v)
            st = str(v)
            # eliminar símbolos y letras
            st = st.replace("S/.", "").replace("S/", "").replace("$", "").replace(",", "").strip()
            # dejar solo números, punto y signo
            st = "".join(ch for ch in st if ch.isdigit() or ch in ".-")
            if st == "" or st in ("-", "--"):
                return None
            return float(st)
        except Exception:
            return None
    return s.map(clean_val)

# --------------- FLUJO ---------------
def main():
    Path(DOWNLOAD_DIR).mkdir(parents=True, exist_ok=True)
    driver = start_driver(DOWNLOAD_DIR, CHROMEDRIVER_PATH)
    wait = WebDriverWait(driver, WAIT_LONG)

    try:
        print("Abriendo CHQ (favoritos)...")
        driver.get(CHQ_FAVORITES_URL)
        time.sleep(2)

        # --- LOGIN (si aparece formulario) ---
        try:
            # usa tus selectores concretos
            user_input = None
            pass_input = None
            try:
                user_input = driver.find_element(By.CSS_SELECTOR, "input.loginInput")
                pass_input = driver.find_element(By.CSS_SELECTOR, "input.passwordInput")
            except Exception:
                # otros intentos (id/name)
                try:
                    user_input = driver.find_element(By.ID, "username")
                    pass_input = driver.find_element(By.ID, "password")
                except Exception:
                    pass

            if user_input and pass_input:
                print("Haciendo login...")
                user_input.clear(); user_input.send_keys(USUARIO)
                pass_input.clear(); pass_input.send_keys(CLAVE)
                # click al botón ingresar
                try:
                    btn = driver.find_element(By.CSS_SELECTOR, "button[data-bind*='onSingInClick']")
                    btn.click()
                except Exception:
                    pass
                time.sleep(3)
        except Exception as e:
            print("Login: error (puede que ya estés logueado):", e)

        # --- Asegurar que estamos en la lista de Favorites ---
        driver.get(CHQ_FAVORITES_URL)
        time.sleep(2)

        # --- Abrir TWR-0281 ---
        print(f"Buscando TWR {TWR_CODE} y abriendo...")
        try:
            el = None
            try:
                el = wait.until(EC.element_to_be_clickable((By.XPATH, f"//td[contains(., '{TWR_CODE}')]")))
            except Exception:
                # búsqueda alternativa
                elems = driver.find_elements(By.XPATH, f"//*[contains(text(), '{TWR_CODE}')]")
                el = elems[0] if elems else None
            if not el:
                print(f"No encontré {TWR_CODE} en favoritos. Asegúrate que esté en tu lista.")
                return
            el.click()
            time.sleep(2)
        except Exception as e:
            print("Error al abrir TWR:", e)
            return

        # --- Función que corre el reporte para una lista de textos de fecha ---
        def run_for(option_texts, out_name):
            print(f"\n--- Ejecutando para: {option_texts} ---")
            # limpiar archivos previos candidatos para evitar confusiones
            before = files_set(DOWNLOAD_DIR)

            # seleccionar la fecha en el dropdown
            ok = click_date_option(driver, option_texts)
            if not ok:
                print("No pude seleccionar la opción de fecha (busqué):", option_texts)
                # continuamos e intentamos ejecutar de todas formas

            time.sleep(0.8)
            # presionar ejecutar/run
            run_btn = choose_run_button(driver)
            if not run_btn:
                print("No encontré botón 'Ejecutar' (run).")
            else:
                try:
                    run_btn.click()
                except Exception:
                    driver.execute_script("arguments[0].click();", run_btn)

            # esperar que aparezca la opción de exportar (a veces aparece un botón)
            time.sleep(2)
            # intentar hacer click en un botón de export/download
            try:
                # intentos de botones exportar por texto
                export_btn = None
                export_candidates = driver.find_elements(By.XPATH, "//button") + driver.find_elements(By.XPATH, "//a")
                for x in export_candidates:
                    txt = (x.text or "").strip().lower()
                    if any(k in txt for k in ("excel", "export", "descargar", "download", "exportar")):
                        export_btn = x
                        break
                if export_btn:
                    try:
                        export_btn.click()
                    except Exception:
                        driver.execute_script("arguments[0].click();", export_btn)
            except Exception:
                pass

            # esperar descarga nueva
            new_file = wait_for_new_file(before, DOWNLOAD_DIR, timeout=60)
            if not new_file:
                print("No detecté archivo nuevo tras ejecutar el reporte.")
                return None
            # renombrar a nombre esperado (sobrescribe si existe)
            target = Path(DOWNLOAD_DIR) / out_name
            try:
                if target.exists():
                    target.unlink()
                shutil.move(str(new_file), str(target))
                # esperar a que archivo esté estable
                ok = wait_file_stable(target, checks=4, interval=0.8)
                if not ok:
                    print("Advertencia: el archivo puede no estar completamente escrito aún:", target)
                print("Descargado y renombrado a:", target)
                return target
            except Exception as e:
                print("Error renombrando/moviendo archivo:", e)
                return None

        # Ejecutar para Hoy (intenta variantes en español/inglés)
        file_hoy = run_for(["Hoy", "Today"], OUT_HOY)
        # Re-abrir el mismo TWR (en algunos sistemas el reporte queda en la misma vista; si no, recargar)
        time.sleep(1)
        # Ejecutar para Este Mes
        file_mes = run_for(["Este mes", "This Month", "This month", "Este Mes"], OUT_MES)

        # --- Procesar los archivos y extraer columna 'Venta Neta' ---
        def extract_venta_neta(path: Path):
            if not path or not path.exists():
                print("Archivo no disponible:", path)
                return 0.0
            try:
                df = pd.read_excel(path)
            except Exception as e:
                print("Error leyendo Excel:", e)
                return 0.0
            # buscar columna por keywords
            keywords = ["venta neta", "venta_neta", "venta", "net sales", "net_sales", "venta net", "venta_neta"]
            col = find_column_name(df, keywords) or find_column_name(df, ["venta", "total", "importe", "amount", "monto"])
            if not col:
                print("No encontré columna 'Venta Neta' ni columna parecida. Columnas disponibles:", list(df.columns)[:10])
                return 0.0
            s = clean_to_float_series(df[col])
            total = s.dropna().sum()
            print(f"Sumé columna '{col}' del archivo {path.name}: {total:,.2f}")
            return float(total)

        venta_hoy = extract_venta_neta(Path(DOWNLOAD_DIR) / OUT_HOY)
        venta_mes = extract_venta_neta(Path(DOWNLOAD_DIR) / OUT_MES)

        print("\n=== RESULTADO FINAL ===")
        print(f"Venta Neta - Hoy: S/. {venta_hoy:,.2f}")
        print(f"Venta Neta - Este mes: S/. {venta_mes:,.2f}")
        print(f"Equipos vendidos (por defecto): {EQUIPOS_VENDIDOS}")

        # aquí puedes devolver/guardar los valores, por ejemplo exportar a CSV
        resumen = {
            "fecha_ejecucion": time.strftime("%Y-%m-%d %H:%M:%S"),
            "venta_hoy": venta_hoy,
            "venta_mes": venta_mes,
            "equipos_vendidos": EQUIPOS_VENDIDOS
        }
        out_csv = Path(DOWNLOAD_DIR) / f"resumen_arequipa_{time.strftime('%Y%m%d_%H%M%S')}.csv"
        pd.DataFrame([resumen]).to_csv(out_csv, index=False)
        print("Resumen guardado en:", out_csv)

    finally:
        print("Cerrando navegador.")
        try:
            driver.quit()
        except Exception:
            pass

if __name__ == "__main__":
    main()

#python3 /Users/maccenterarequipa/Documents/old_vs/platzy/av/automat.py --date 2025-08-12

