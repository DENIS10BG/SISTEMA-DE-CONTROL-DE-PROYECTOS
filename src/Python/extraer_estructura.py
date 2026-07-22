import cv2
import json
import re
import numpy as np
import pytesseract
from pdf2image import convert_from_path
from pathlib import Path

# ============================================================================
# CONFIGURACIÓN
# ============================================================================
PDF_PATH = r"C:\Users\denis\Downloads\proyecto_ocr_2.pdf"
OUTPUT_DIR = Path(r"C:\Users\denis\Downloads\Resultado_Final")
OUTPUT_JSON = OUTPUT_DIR / "estructura_previa_ocr.json"
TEMPLATES_DIR = Path(r"C:\Users\denis\Downloads\Plantillas_Referencia")

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
ALLOWED_EXTENSIONS = {'.jpg', '.jpeg', '.png'}

# ============================================================================
# 1. VISIÓN ARTIFICIAL: COMPARACIÓN MULTI-PLANTILLA Y PAGINACIÓN
# ============================================================================
def cargar_plantillas(directorio, prefijo):
    plantillas_cargadas = []
    if not directorio.exists(): return plantillas_cargadas
    archivos = sorted(list(directorio.glob(f"{prefijo}*")))
    orb = cv2.ORB_create(nfeatures=1000)
    for ruta in archivos:
        if ruta.suffix.lower() in ALLOWED_EXTENSIONS:
            img = cv2.imread(str(ruta), cv2.IMREAD_GRAYSCALE)
            if img is not None:
                kp, des = orb.detectAndCompute(img, None)
                if des is not None:
                    plantillas_cargadas.append({'nombre': ruta.name, 'descriptors': des})
    return plantillas_cargadas

def calcular_maxima_similitud(img_pagina, plantillas_referencia):
    if not plantillas_referencia: return 0, "Ninguna"
    pagina_cv = cv2.cvtColor(np.array(img_pagina), cv2.COLOR_RGB2BGR)
    pagina_gris = cv2.cvtColor(pagina_cv, cv2.COLOR_BGR2GRAY)
    orb = cv2.ORB_create(nfeatures=1000)
    _, des_pag = orb.detectAndCompute(pagina_gris, None)
    if des_pag is None: return 0, "Ninguna"
    
    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
    max_score = 0
    mejor_plantilla = "Ninguna"
    
    for plantilla in plantillas_referencia:
        try:
            matches = bf.match(plantilla['descriptors'], des_pag)
            buenas = [m for m in matches if m.distance < 50]
            if len(buenas) > max_score:
                max_score = len(buenas)
                mejor_plantilla = plantilla['nombre']
        except cv2.error:
            continue
    return max_score, mejor_plantilla

def tiene_tabla(img_pagina):
    """Usa OpenCV para detectar si la página tiene una estructura de tabla visible, basada en conteo estricto de celdas"""
    pagina_cv = cv2.cvtColor(np.array(img_pagina), cv2.COLOR_RGB2BGR)
    gray = cv2.cvtColor(pagina_cv, cv2.COLOR_BGR2GRAY)
    thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)
    
    horizontales = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, cv2.getStructuringElement(cv2.MORPH_RECT, (100, 1)))
    verticales = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, cv2.getStructuringElement(cv2.MORPH_RECT, (1, 100)))
    
    tabla_mask = cv2.add(horizontales, verticales)
    contornos_tabla, _ = cv2.findContours(tabla_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    celdas = 0
    for c in contornos_tabla:
        x, y, w, h = cv2.boundingRect(c)
        area = w * h
        # Tolerancia amplia: desde cuadritos pequeños hasta columnas gigantes
        if 500 < area < 400000: 
            celdas += 1
            
    # Una carátula vacía no llegará jamás a 10 celdas internas. Una tabla real, sí.
    return celdas >= 10

def obtener_paginacion(img_pagina):
    """Escanea exclusivamente el 10% inferior de la hoja buscando el patrón de paginación '1 - 3' o '3 / 3'"""
    pagina_cv = cv2.cvtColor(np.array(img_pagina), cv2.COLOR_RGB2BGR)
    h, w = pagina_cv.shape[:2]
    
    # Recortar solo la parte de abajo para evitar ruido del resto del documento
    recorte_inferior = pagina_cv[int(h*0.90):h, 0:w]
    gray = cv2.cvtColor(recorte_inferior, cv2.COLOR_BGR2GRAY)
    
    # Escalado 2x para leer números pequeños y limpieza con Otsu
    gray = cv2.resize(gray, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    
    texto = pytesseract.image_to_string(thresh, lang='spa', config='--psm 6')
    
    # Regex estricto para: número (1 o 2 dígitos) + guión/barra + número (1 o 2 dígitos)
    match = re.search(r'\b(\d{1,2})\s*[-/]\s*(\d{1,2})\b', texto)
    if match:
        pag_actual = int(match.group(1))
        pag_total = int(match.group(2))
        # Filtro de cordura: La página actual no puede ser mayor a la total
        if 0 < pag_actual <= pag_total and pag_total <= 20:
            return pag_actual, pag_total
    return None, None

def identificar_rangos(images, plantillas_indice, plantillas_inventario):
    pag_indice = None
    max_score_i = 0
    
    inicio_inventario = None
    max_score_inv = 0

    # 1. Encontrar la página principal de Índice y de Inicio de Inventario
    for i, img in enumerate(images):
        pag_num = i + 1
        score_i, _ = calcular_maxima_similitud(img, plantillas_indice)
        
        umbral_indice = max_score_i + 15 if pag_indice else 25
        if score_i > umbral_indice:
            max_score_i = score_i
            pag_indice = pag_num
            
        score_inv, _ = calcular_maxima_similitud(img, plantillas_inventario)
        
        umbral_inv = max_score_inv + 15 if inicio_inventario else 25
        if score_inv > umbral_inv:
            max_score_inv = score_inv
            inicio_inventario = pag_num

    fin_inventario = inicio_inventario
    
    # 2. Rango del Inventario utilizando paginación + escaneo geométrico de respaldo
    if inicio_inventario:
        # Intentar leer paginación en la hoja 1 del inventario
        p_act, p_tot = obtener_paginacion(images[inicio_inventario - 1])
        
        if p_tot:
            print(f"      -> ¡Paginación detectada! El inventario consta de {p_tot} hojas.")
            fin_inventario = inicio_inventario + p_tot - 1
            fin_inventario = min(fin_inventario, len(images))
        else:
            print("      -> No se detectó paginación en la hoja 1. Escaneando geometría página a página...")
            for j in range(inicio_inventario, len(images)):
                if pag_indice and (j + 1) == pag_indice: break
                
                # Comprobar la paginación de la hoja actual (Ej. si lee "3 - 3", sabe que es el final)
                p_act_b, p_tot_b = obtener_paginacion(images[j])
                if p_tot_b and p_act_b == p_tot_b:
                    print(f"      -> Final de paginación encontrado: Hoja {p_act_b} de {p_tot_b}.")
                    fin_inventario = j + 1
                    break
                    
                # Si no hay paginación, confiar en el detector de cuadrículas de tabla
                if tiene_tabla(images[j]):
                    fin_inventario = j + 1
                else:
                    break # Se rompió la tabla (ya no hay celdas), termina el inventario

    return pag_indice, inicio_inventario, fin_inventario

# ============================================================================
# 2. EXTRACCIÓN OCR DE ÍNDICE
# ============================================================================
def extraer_indice_ocr_desde_texto(texto: str) -> dict:
    lineas = texto.split('\n')
    indice = {}
    nivel_actual = None
    
    for linea in lineas:
        linea = linea.strip()
        if not linea: continue
        
        linea = re.sub(r'N\s*[*%2°@]+\s*(\d+)', r'Nº \1', linea)
        linea = re.sub(r'\s+', ' ', linea)
        
        m_principal = re.match(r'^.*?(\d+)\s*[\.\-]\s*(.+)$', linea)
        if m_principal:
            num = int(m_principal.group(1))
            if num == 0: continue 
            
            nivel_actual = num
            indice[nivel_actual] = {
                'tipo': 'principal', 
                'numero': num, 
                'titulo': m_principal.group(2).strip(), 
                'subniveles': []
            }
            continue
            
        m_sub = re.match(r'^.*?([a-zA-Z])\s*[\)\.\-\]\}]\s*(.+)$', linea)
        if m_sub and nivel_actual is not None:
            if nivel_actual in indice:
                indice[nivel_actual]['subniveles'].append({
                    'letra': m_sub.group(1).lower(), 
                    'titulo': m_sub.group(2).strip()
                })
                
    return indice

# ============================================================================
# 3. EXTRACCIÓN OCR DE TABLAS DE INVENTARIO (PURIFICACIÓN ULTRA-AGRESIVA)
# ============================================================================
def ocr_celda(img_celda, es_numero=False):
    if img_celda.size == 0 or img_celda.shape[0] <= 0 or img_celda.shape[1] <= 0:
        return ""
        
    if es_numero:
        config = '--psm 7 -c tessedit_char_whitelist=0123456789'
    else:
        config = '--psm 6' 
        
    texto = pytesseract.image_to_string(img_celda, lang='spa', config=config).strip()
    texto = re.sub(r'\s+', ' ', texto) 
    
    # ------------------------------------------------------------------
    # 🛡️ LIMPIEZA DE "ALUCINACIONES" DEL OCR (MODO BRUTAL)
    # ------------------------------------------------------------------
    texto = re.sub(r'\bFORM\b\.?\s*', 'FORMULARIO ', texto, flags=re.IGNORECASE)
    texto = re.sub(r'\bN\s*[\?\°\º\_\*O0o2\.\,]*\s*(\d+)', r'Nº \1', texto, flags=re.IGNORECASE)
    
    # 🔥 ELIMINADOR BRUTAL PARA EL "CONVENIO 5"
    # Busca la palabra CONVENIO seguida de un 5, sin importar qué basura haya en medio,
    # y lo reemplaza pura y exclusivamente por "CONVENIO"
    texto = re.sub(r'ESTAS\s+CONVENIO', 'CONVENIO', texto, flags=re.IGNORECASE)
    texto = re.sub(r'CONVENIO\s*5.*', 'CONVENIO', texto, flags=re.IGNORECASE)
    
    # 🔥 CORTADORAS TÁCTICAS
    texto = re.sub(r'(POLIZAS DE SEGURO).*', r'\1', texto, flags=re.IGNORECASE)
    texto = re.sub(r'(LICENCIA AMBIENTAL).*', r'\1', texto, flags=re.IGNORECASE)
    texto = re.sub(r'(PLANOS)\s*[:;\[\]A-Za-z0-9\s]*$', r'\1', texto, flags=re.IGNORECASE)
    
    # Eliminar símbolos basura generados por los bordes negros
    texto = re.sub(r'[\[\]\|\}\{><]+', '', texto)
    texto = texto.strip(':;,-_ ')
    # ------------------------------------------------------------------
    
    return texto.strip()

def extraer_tabla_inventario_ocr(img_pagina):
    print("      -> Procesando tabla con OpenCV: Aplicando recorte asimétrico...")
    pagina_cv = cv2.cvtColor(np.array(img_pagina), cv2.COLOR_RGB2BGR)
    gray = cv2.cvtColor(pagina_cv, cv2.COLOR_BGR2GRAY)
    
    thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)
    
    horiz_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (50, 1))
    vert_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 50))
    
    horizontales = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, horiz_kernel, iterations=2)
    verticales = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, vert_kernel, iterations=2)
    
    kernel_refuerzo = np.ones((3, 3), np.uint8)
    horizontales = cv2.dilate(horizontales, kernel_refuerzo, iterations=1)
    verticales = cv2.dilate(verticales, kernel_refuerzo, iterations=1)
    
    tabla_mask = cv2.add(horizontales, verticales)
    
    kernel_borrado = np.ones((9, 9), np.uint8)
    lineas_gruesas = cv2.dilate(tabla_mask, kernel_borrado, iterations=2)
    
    gray_sin_lineas = gray.copy()
    gray_sin_lineas[lineas_gruesas == 255] = 255 
    
    # Threshold estricto contra fantasmas
    _, img_ocr_limpia = cv2.threshold(gray_sin_lineas, 150, 255, cv2.THRESH_BINARY)
    
    contornos, _ = cv2.findContours(tabla_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    celdas_bboxes = []
    for c in contornos:
        x, y, w, h = cv2.boundingRect(c)
        if 100 < (w * h) < 500000:
            celdas_bboxes.append((x, y, w, h))
            
    if not celdas_bboxes: return []

    celdas_bboxes.sort(key=lambda b: b[1])
    
    filas = []
    fila_actual = [celdas_bboxes[0]]
    for caja in celdas_bboxes[1:]:
        x, y, w, h = caja
        centro_y = y + (h / 2.0)
        x0, y0, w0, h0 = fila_actual[0]
        
        if (y0 - 10) <= centro_y <= (y0 + h0 + 10):
            fila_actual.append(caja)
        else:
            filas.append(fila_actual)
            fila_actual = [caja]
    filas.append(fila_actual)
    
    datos_inventario = []
    
    for fila in filas:
        fila.sort(key=lambda b: b[0]) 
        if len(fila) < 5: continue
            
        textos_fila = []
        for i, (x, y, w, h) in enumerate(fila):
            
            # 🛡️ FIX ANTI-MORDIDAS: Recorte asimétrico.
            # Cortamos más fuerte abajo (margen_y_abajo = 12) para no tocar las letras de la fila inferior
            margen_x = 12
            margen_y_arriba = 6
            margen_y_abajo = 14 
            
            y_start = max(0, y + margen_y_arriba)
            y_end = min(img_ocr_limpia.shape[0], y + h - margen_y_abajo)
            x_start = max(0, x + margen_x)
            x_end = min(img_ocr_limpia.shape[1], x + w - margen_x)
            
            if y_end <= y_start or x_end <= x_start:
                textos_fila.append("")
                continue
                
            recorte = img_ocr_limpia[y_start:y_end, x_start:x_end]
            
            es_nro = (i == 0)
            texto_celda = ocr_celda(recorte, es_numero=es_nro)
            textos_fila.append(texto_celda)
            
        try:
            nro_str = textos_fila[0]
            if not re.search(r'\d+', nro_str): continue 
            
            nro = int(re.search(r'\d+', nro_str).group())
            fila_data = {
                "nro": nro,
                "codigo": textos_fila[1] if len(textos_fila) > 1 else "",
                "tipo_documento": textos_fila[2] if len(textos_fila) > 2 else "",
                "remitente": textos_fila[3] if len(textos_fila) > 3 else "",
                "dirigido_a": textos_fila[4] if len(textos_fila) > 4 else "",
                "objeto": textos_fila[5] if len(textos_fila) > 5 else "",
                "nro_fojas": textos_fila[6] if len(textos_fila) > 6 else "",
                "nro_folio": textos_fila[7] if len(textos_fila) > 7 else "",
                "obs": textos_fila[8] if len(textos_fila) > 8 else ""
            }
            datos_inventario.append(fila_data)
        except Exception as e:
            continue

    return datos_inventario

def extraer_tabla_inventario_ocr(img_pagina):
    print("      -> Procesando tabla con OpenCV y Tesseract (OCR celda por celda)...")
    pagina_cv = cv2.cvtColor(np.array(img_pagina), cv2.COLOR_RGB2BGR)
    gray = cv2.cvtColor(pagina_cv, cv2.COLOR_BGR2GRAY)
    
    thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)
    
    horiz_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (40, 1))
    vert_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 40))
    
    horizontales = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, horiz_kernel, iterations=2)
    verticales = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, vert_kernel, iterations=2)
    
    tabla_mask = cv2.add(horizontales, verticales)
    contornos, _ = cv2.findContours(tabla_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    celdas_bboxes = []
    for c in contornos:
        x, y, w, h = cv2.boundingRect(c)
        area = w * h
        if 1000 < area < 400000:
            celdas_bboxes.append((x, y, w, h))
            
    if not celdas_bboxes:
        return []

    celdas_bboxes.sort(key=lambda b: b[1])
    
    filas = []
    fila_actual = [celdas_bboxes[0]]
    for caja in celdas_bboxes[1:]:
        if abs(caja[1] - fila_actual[-1][1]) < 15:
            fila_actual.append(caja)
        else:
            filas.append(fila_actual)
            fila_actual = [caja]
    filas.append(fila_actual)
    
    datos_inventario = []
    
    for fila in filas:
        fila.sort(key=lambda b: b[0])
        
        if len(fila) < 5:
            continue
            
        textos_fila = []
        for (x, y, w, h) in fila:
            margen_y = min(3, h // 4)
            margen_x = min(3, w // 4)
            recorte = gray[y+margen_y : y+h-margen_y, x+margen_x : x+w-margen_x]
            
            texto_celda = ocr_celda(recorte)
            textos_fila.append(texto_celda)
            
        try:
            nro_str = textos_fila[0]
            if not re.search(r'\d+', nro_str): continue 
            
            nro = int(re.search(r'\d+', nro_str).group())
            fila_data = {
                "nro": nro,
                "codigo": textos_fila[1] if len(textos_fila) > 1 else "",
                "tipo_documento": textos_fila[2] if len(textos_fila) > 2 else "",
                "remitente": textos_fila[3] if len(textos_fila) > 3 else "",
                "dirigido_a": textos_fila[4] if len(textos_fila) > 4 else "",
                "objeto": textos_fila[5] if len(textos_fila) > 5 else "",
                "nro_fojas": textos_fila[6] if len(textos_fila) > 6 else "",
                "nro_folio": textos_fila[7] if len(textos_fila) > 7 else "",
                "obs": textos_fila[8] if len(textos_fila) > 8 else ""
            }
            datos_inventario.append(fila_data)
        except Exception as e:
            continue

    return datos_inventario

# ============================================================================
# 4. MAIN
# ============================================================================
def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    if not TEMPLATES_DIR.exists(): TEMPLATES_DIR.mkdir(parents=True, exist_ok=True)
    
    plantillas_i = cargar_plantillas(TEMPLATES_DIR, "INDICE_")
    plantillas_inv = cargar_plantillas(TEMPLATES_DIR, "INVENTARIO_")

    print("1. Convirtiendo PDF a imágenes...")
    images = convert_from_path(PDF_PATH, first_page=1, last_page=15, dpi=300)
    
    print("2. Identificando rangos...")
    pag_indice, inicio_inv, fin_inv = identificar_rangos(images, plantillas_i, plantillas_inv)
    
    estructura = {"indice": {}, "inventario": [], "rangos_paginas": {}}
    
    if pag_indice:
        print(f"✅ Índice en PÁGINA {pag_indice}. Aplicando OCR mejorado...")
        estructura["rangos_paginas"]["indice"] = {"inicio": pag_indice, "fin": pag_indice}
        
        config_ocr = '--psm 6' 
        
        img_pagina = images[pag_indice-1]
        img_cv = cv2.cvtColor(np.array(img_pagina), cv2.COLOR_RGB2BGR)
        gray = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)
        
        gray = cv2.resize(gray, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
        
        texto_indice_completo = pytesseract.image_to_string(gray, lang='spa', config=config_ocr)
        estructura["indice"] = extraer_indice_ocr_desde_texto(texto_indice_completo)
        
    if inicio_inv:
        print(f"✅ Inventario detectado desde PÁGINA {inicio_inv} hasta {fin_inv}.")
        estructura["rangos_paginas"]["inventario"] = {"inicio": inicio_inv, "fin": fin_inv}
        
        todas_las_filas = []
        for p in range(inicio_inv, fin_inv + 1):
            print(f"   -> Extrayendo datos de la página {p}...")
            filas_pagina = extraer_tabla_inventario_ocr(images[p-1])
            todas_las_filas.extend(filas_pagina)
            
        estructura["inventario"] = todas_las_filas
        
    with open(OUTPUT_JSON, 'w', encoding='utf-8') as f:
        json.dump(estructura, f, ensure_ascii=False, indent=2)
    print(f"🎯 JSON Guardado Exitosamente en: {OUTPUT_JSON}")

if __name__ == '__main__':
    main()