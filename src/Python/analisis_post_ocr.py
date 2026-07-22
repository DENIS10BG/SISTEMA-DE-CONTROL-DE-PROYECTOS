"""
================================================================================
📊 ANÁLISIS ESTRUCTURAL POST-OCR - VERSIÓN DEFINITIVA (LEMATIZACIÓN CONDICIONAL)
================================================================================
- Lematizador Táctico: Solo quita la 'S' final si el documento es una CARÁTULA.
- Inmunidad de Carátulas: Al ser irrefutables, saltan el Escudo Lookahead.
- Ventana Dinámica: Compara fragmentos exactos y con tolerancia a ruido OCR.
- Excepción Salvavidas: Aprueba documentos si el Objeto Principal coincide.
================================================================================
"""

import json
import re
from pathlib import Path
import difflib
import unicodedata

# ============================================================================
# CONFIGURACIÓN DE RUTAS
# ============================================================================
RUTA_RESULTADOS = Path(r"C:\Users\denis\Downloads\Resultado_Final")
ARCHIVO_JSON_OCR = RUTA_RESULTADOS / "resultados.json"
ARCHIVO_ESTRUCTURA = RUTA_RESULTADOS / "estructura_previa_ocr.json" 
ARCHIVO_SALIDA = RUTA_RESULTADOS / "proyecto_estructurado.json"

def unir_lineas(texto: str) -> str:
    if not texto: return ""
    lineas = texto.split('\n')
    resultado = []
    i = 0
    while i < len(lineas):
        linea = lineas[i].strip()
        if not linea:
            resultado.append('')
            i += 1
            continue
        while i + 1 < len(lineas):
            siguiente = lineas[i+1].strip()
            if not siguiente: break
            if linea[-1] not in ('.', '?', '!', ';'):
                if not re.match(r'^(\d+\.?\s*|[a-zA-Z]\)\s*|\*|\-)', siguiente):
                    linea += ' ' + siguiente
                    i += 1
                    continue
            if siguiente and siguiente[0].islower():
                if linea[-1] not in ('.', '?', '!'):
                    linea += ' ' + siguiente
                    i += 1
                    continue
            break
        resultado.append(linea)
        i += 1
    return '\n'.join(resultado)

def limpiar_texto(texto: str) -> str:
    """Limpia tildes y repara símbolos. (La eliminación de la 'S' ya no es global)."""
    if not texto: return ""
    
    texto = re.sub(r'\bFO[RMN]+\b\.?\s*(\d+)', r'FORMULARIO NRO \1', texto, flags=re.IGNORECASE)
    texto = re.sub(r'\bFO[RMN]+\b\.?', 'FORMULARIO ', texto, flags=re.IGNORECASE)
    texto = re.sub(r'\bN\s*[?°º\_\*\.]*2?\s*0*(\d+)', r'NRO \1', texto, flags=re.IGNORECASE)
    
    texto = unicodedata.normalize('NFKD', texto).encode('ASCII', 'ignore').decode('utf-8')
    texto = re.sub(r'[^\w\s]', ' ', texto)
    return texto.strip().upper()

def buscar_pagina_exacta(item: dict, resultados: dict, paginas_excluidas: set, pagina_minima: int, origen: str) -> tuple:
    ultima_pagina_pdf = max((int(k) for k in resultados.keys() if str(k).isdigit()), default=0)
    candidatos = []
    titulo_limpio = limpiar_texto(item.get('titulo', ''))
    
    # =========================================================================
    # LÓGICA 1: BÚSQUEDA PARA EL ÍNDICE
    # =========================================================================
    if origen == 'indice':
        tipo_item = item.get('tipo', 'sub')
        if not titulo_limpio: return None, False
        
        palabras_clave = [p for p in titulo_limpio.split() if len(p) > 2]
        if not palabras_clave: return None, False
        
        for pagina in range(pagina_minima, ultima_pagina_pdf + 1):
            if pagina in paginas_excluidas: continue
            texto = resultados.get(str(pagina), "") or resultados.get(pagina, "")
            if not texto: continue
            
            texto_limpio = limpiar_texto(texto)
            cant_palabras = len(texto_limpio.split())
            
            mejor_ratio_linea = 0
            for linea in texto_limpio.split('\n'):
                if not linea: continue
                ratio = difflib.SequenceMatcher(None, titulo_limpio, linea).ratio()
                if ratio > mejor_ratio_linea: mejor_ratio_linea = ratio
                    
            palabras_texto = texto_limpio.split()
            len_titulo = len(palabras_clave)
            mejor_ratio_ventana = 0
            
            for i in range(len(palabras_texto) - len_titulo + 1):
                for extra in range(3):
                    if i + len_titulo + extra <= len(palabras_texto):
                        fragmento = " ".join(palabras_texto[i:i + len_titulo + extra])
                        ratio = difflib.SequenceMatcher(None, titulo_limpio, fragmento).ratio()
                        if ratio > mejor_ratio_ventana: mejor_ratio_ventana = ratio
                    
            ratio_final = max(mejor_ratio_linea, mejor_ratio_ventana * 0.85)
            
            if ratio_final > 0.70:
                puntaje = ratio_final
                if tipo_item == 'principal':
                    if cant_palabras < 50: puntaje += 0.40
                    elif cant_palabras > 150: puntaje -= 0.30
                if mejor_ratio_linea > mejor_ratio_ventana: puntaje += 0.15 
                
                if pagina == pagina_minima: puntaje += 0.10
                elif pagina <= pagina_minima + 3: puntaje += 0.05
                    
                candidatos.append({'pagina': pagina, 'puntaje': puntaje})

    # =========================================================================
    # LÓGICA 2: BÚSQUEDA PARA EL INVENTARIO (Metadatos Duales + Densidad)
    # =========================================================================
    elif origen == 'inventario':
        datos = item.get('datos', {})
        tipo_doc_raw = str(datos.get('tipo_documento', '')).upper()
        
        es_caratula = False
        if 'CARATULA' in tipo_doc_raw:
            es_caratula = True
            tipo_doc_raw = "" 
            
        for sep in ['DE FECHA', 'FECHA']:
            if sep in tipo_doc_raw:
                tipo_doc_raw = tipo_doc_raw.split(sep)[0]
                break
                
        tipo_doc = limpiar_texto(tipo_doc_raw)
        remitente = limpiar_texto(str(datos.get('remitente', '')))
        dirigido = limpiar_texto(str(datos.get('dirigido_a', '')))
        objeto = limpiar_texto(str(datos.get('objeto', '')))
        
        campos_a_buscar = [c for c in [tipo_doc, remitente, dirigido, objeto] if len(c.split()) > 0]
        if not campos_a_buscar: campos_a_buscar = [titulo_limpio]
            
        numeros_clave = re.findall(r'\d+', titulo_limpio)
        
        # Pre-calculamos el objeto lematizado por si se activa la regla salvavidas
        objeto_comp = re.sub(r'\b([A-Z]{3,})S\b', r'\1', objeto) if es_caratula else objeto
        
        for pagina in range(pagina_minima, ultima_pagina_pdf + 1):
            if pagina in paginas_excluidas: continue
            texto = resultados.get(str(pagina), "") or resultados.get(pagina, "")
            if not texto: continue
            
            texto_limpio = limpiar_texto(texto)
            cant_palabras = len(texto_limpio.split())
            
            if es_caratula and cant_palabras > 80: continue 
            
            if numeros_clave:
                falta_numero = False
                for num in numeros_clave:
                    if not re.search(rf'\b{num}\b', texto_limpio):
                        falta_numero = True
                        break
                if falta_numero: continue 
            
            penalizacion_densidad = 0
            if not es_caratula and cant_palabras > 180:
                penalizacion_densidad = 0.40

            coincidencias_campos = 0
            puntaje_acumulado = 0
            objeto_encontrado_perfecto = False 
            
            for campo in campos_a_buscar:
                # 🛡️ FIX 1: Lematización Simétrica EXCLUSIVA para Carátulas
                if es_caratula:
                    campo_comp = re.sub(r'\b([A-Z]{3,})S\b', r'\1', campo)
                    texto_comp = re.sub(r'\b([A-Z]{3,})S\b', r'\1', texto_limpio)
                else:
                    campo_comp = campo
                    texto_comp = texto_limpio
                
                palabras_campo = [p for p in campo_comp.split() if len(p) > 2]
                if not palabras_campo: continue
                
                coincidencias_palabras = sum(1 for p in palabras_campo if p in texto_comp)
                umbral = max(1, int(len(palabras_campo) * 0.50)) 
                
                if coincidencias_palabras >= umbral:
                    palabras_texto = texto_comp.split()
                    len_campo = len(palabras_campo)
                    mejor_ratio_campo = 0
                    
                    for i in range(len(palabras_texto) - len_campo + 1):
                        for extra in range(3):
                            if i + len_campo + extra <= len(palabras_texto):
                                fragmento = " ".join(palabras_texto[i:i + len_campo + extra])
                                ratio = difflib.SequenceMatcher(None, campo_comp, fragmento).ratio()
                                if ratio > mejor_ratio_campo: mejor_ratio_campo = ratio
                    
                    if mejor_ratio_campo > 0.65:
                        coincidencias_campos += 1
                        puntaje_acumulado += mejor_ratio_campo
                        
                        if campo_comp == objeto_comp and mejor_ratio_campo > 0.85:
                            objeto_encontrado_perfecto = True
            
            campos_requeridos = 1 if es_caratula else min(2, len(campos_a_buscar))
            
            if coincidencias_campos >= campos_requeridos or (coincidencias_campos == 1 and objeto_encontrado_perfecto and len(objeto.split()) >= 2 and cant_palabras < 100):
                puntaje = puntaje_acumulado + (coincidencias_campos * 0.5) - penalizacion_densidad
                
                if pagina == pagina_minima: puntaje += 0.20
                elif pagina <= pagina_minima + 3: puntaje += 0.10
                
                candidatos.append({'pagina': pagina, 'puntaje': puntaje})

    if candidatos:
        candidatos.sort(key=lambda x: x['puntaje'], reverse=True)
        return candidatos[0]['pagina'], True
        
    return None, False

def extraer_titulos_desde_indice(indice: dict) -> list:
    titulos = []
    for num, data in indice.items():
        titulos.append({'id': f"{num}", 'titulo': data.get('titulo', ''), 'tipo': 'principal', 'padre': None})
        for sub in data.get('subniveles', []):
            titulos.append({'id': f"{num}_{sub.get('letra', '')}", 'titulo': sub.get('titulo', ''), 'tipo': 'sub', 'padre': num})
    return titulos

def extraer_titulos_desde_inventario(inventario: list) -> list:
    titulos = []
    for idx, doc in enumerate(inventario):
        titulo = doc.get('objeto') or doc.get('tipo_documento') or f"Documento_{idx}"
        titulos.append({'id': f"inv_{doc.get('nro', '')}_{idx}", 'titulo': titulo, 'tipo': 'inv', 'datos': doc})
    return titulos

def analizar_por_lista(titulos: list, resultados: dict, paginas_excluidas: set, nombre: str, origen: str, rango_inventario: dict = None) -> list:
    docs = []
    
    if origen == 'inventario' and rango_inventario:
        pagina_actual = rango_inventario.get('fin', 1) + 1
    else:
        pagina_actual = 1
        
    for i, item in enumerate(titulos):
        titulo = item.get('titulo', '')
        if not titulo: continue
        
        pagina, exacto = buscar_pagina_exacta(item, resultados, paginas_excluidas, pagina_actual, origen)
            
        # 🛡️ FIX 2: Inmunidad de Carátulas contra el Escudo Lookahead
        es_caratula_actual = False
        if origen == 'inventario':
            es_caratula_actual = 'CARATULA' in str(item.get('datos', {}).get('tipo_documento', '')).upper()

        if pagina and (pagina - pagina_actual > 2):
            if not es_caratula_actual:
                falso_positivo = False
                for step in range(1, 4):
                    if i + step < len(titulos):
                        item_sig = titulos[i+step]
                        p_sig, _ = buscar_pagina_exacta(item_sig, resultados, paginas_excluidas, pagina_actual, origen)
                        
                        if p_sig and p_sig < pagina:
                            falso_positivo = True
                            break 
                            
                if falso_positivo:
                    pagina = None
                    exacto = False
                
        contenido_pag = ""
        if pagina:
            contenido_pag = resultados.get(str(pagina), "") or resultados.get(pagina, "")
            pagina_actual = pagina + 1 

        doc_entry = {
            'id': item.get('id', ''),
            'titulo': titulo,
            'pagina': pagina if pagina else None,
            'encontrado': pagina is not None,
            'exacto': exacto,
            'contenido': contenido_pag
        }
        
        if pagina is None: 
            print(f"⚠️ [{nombre}] FALTANTE: '{titulo[:40]}...'")
        else: 
            print(f"✅ [{nombre}] '{titulo[:40]}...' → página {pagina}")
            
        docs.append(doc_entry)
        
    return docs

def menu_busqueda(proyecto_data: dict):
    docs_indice = proyecto_data.get('documentos_por_indice', [])
    docs_inventario = proyecto_data.get('documentos_por_inventario', [])
    
    while True:
        print("\n" + "="*60)
        print("📋 SISTEMA DE VALIDACIÓN DOCUMENTAL ESTRUCTURAL")
        print("1. Listar documentos (por ÍNDICE) con estado")
        print("2. Listar documentos (por INVENTARIO) con estado")
        print("3. Buscar documento por título")
        print("4. Mostrar resumen de un documento (por ID)")
        print("5. Resumen global del proyecto")
        print("6. Verificar integridad estructural")
        print("7. Buscar por número de página real")
        print("0. Salir")
        opcion = input("Opción: ").strip()
        
        if opcion == '0': break
        elif opcion == '1':
            print("\n📌 DOCUMENTOS POR ÍNDICE:")
            for d in docs_indice:
                estado = "✅" if d['encontrado'] else "❌"
                pagina = d['pagina'] if d['pagina'] else "---"
                print(f"{estado} {d['id']:10s} {d['titulo'][:50]} (pág. {pagina})")
        elif opcion == '2':
            print("\n📌 DOCUMENTOS POR INVENTARIO:")
            for d in docs_inventario:
                estado = "✅" if d['encontrado'] else "❌"
                pagina = d['pagina'] if d['pagina'] else "---"
                print(f"{estado} {d['id']:10s} {d['titulo'][:50]} (pág. {pagina})")
        elif opcion == '3':
            consulta = input("Escribe parte del título: ").strip().lower()
            encontrados = [d for d in docs_indice + docs_inventario if consulta in d['titulo'].lower()]
            if not encontrados: print("No se encontraron documentos.")
            else:
                for d in encontrados:
                    estado = "✅" if d['encontrado'] else "❌"
                    pagina = d['pagina'] if d['pagina'] else "---"
                    print(f"{estado} {d['id']:10s} {d['titulo']} (pág. {pagina})")
        elif opcion == '4':
            doc_id = input("ID del documento: ").strip()
            for d in docs_indice + docs_inventario:
                if d['id'] == doc_id:
                    estado = "✅" if d['encontrado'] else "❌"
                    print(f"\n{estado} 📄 {d['titulo']}")
                    print(f"Página: {d['pagina'] if d['pagina'] else 'No encontrado'}")
                    print(f"Resumen: {d.get('resumen', 'No disponible')}")
                    break
            else: print("Documento no encontrado.")
        elif opcion == '5':
            print("\n📌 RESUMEN GLOBAL DEL PROYECTO")
            print(proyecto_data.get('resumen_global', 'No disponible'))
        elif opcion == '6':
            integridad = proyecto_data.get('integridad', {})
            print(f"Esperados (índice): {integridad.get('total_indice', 0)} | Encontrados: {integridad.get('encontrados_indice', 0)}")
            print(f"Esperados (inventario): {integridad.get('total_inventario', 0)} | Encontrados: {integridad.get('encontrados_inventario', 0)}")
            if integridad.get('faltantes_indice'): print(f"⚠️ Faltan en índice: {integridad['faltantes_indice']}")
            if integridad.get('faltantes_inventario'): print(f"⚠️ Faltan en inventario: {integridad['faltantes_inventario']}")
            if not integridad.get('faltantes_indice') and not integridad.get('faltantes_inventario'):
                print("✅ Todos los documentos están presentes. Integridad validada.")
        elif opcion == '7':
            try: pagina = int(input("Número de página real: ").strip())
            except ValueError:
                print("Número inválido."); continue
            encontrados = [d for d in docs_indice + docs_inventario if d['pagina'] == pagina]
            if not encontrados: print("No se encontró documento para esa página.")
            else:
                for d in encontrados:
                    estado = "✅" if d['encontrado'] else "❌"
                    print(f"📌 Página {pagina} → {estado} {d['titulo']} (ID: {d['id']})")
        else: print("Opción no válida.")

def verificar_integridad(esperados: list, encontrados: list) -> dict:
    ids_esperados = {doc['id'] for doc in esperados}
    ids_encontrados = {d['id'] for d in encontrados if d['encontrado']}
    return {
        'faltantes': sorted(list(ids_esperados - ids_encontrados)),
        'total_esperados': len(ids_esperados),
        'total_encontrados': len(ids_encontrados)
    }

def analizar_proyecto():
    if not ARCHIVO_JSON_OCR.exists() or not ARCHIVO_ESTRUCTURA.exists():
        print("❌ Faltan archivos JSON base. Verifica que los scripts previos se ejecutaron.")
        return

    with open(ARCHIVO_JSON_OCR, 'r', encoding='utf-8') as f:
        resultados_raw = json.load(f)
    resultados = {int(k): unir_lineas(v) for k, v in resultados_raw.items() if str(k).isdigit()}
    
    with open(ARCHIVO_ESTRUCTURA, 'r', encoding='utf-8') as f:
        estructura = json.load(f)

    indice = estructura.get('indice', {})
    inventario = estructura.get('inventario', [])
    rangos = estructura.get('rangos_paginas', {})

    paginas_excluidas = set()
    for tipo_rango in ['indice', 'inventario']:
        rango = rangos.get(tipo_rango, {})
        if rango:
            for p in range(rango.get('inicio', 1), rango.get('fin', 1) + 1):
                paginas_excluidas.add(p)

    titulos_indice = extraer_titulos_desde_indice(indice)
    print(f"\n⚙️ Iniciando validación SECUENCIAL por Índice...")
    docs_indice = analizar_por_lista(titulos_indice, resultados, paginas_excluidas, "ÍNDICE", origen="indice")
    
    titulos_inventario = extraer_titulos_desde_inventario(inventario)
    print(f"\n⚙️ Iniciando validación MULTIVARIABLE por Inventario...")
    rango_inv = rangos.get('inventario', {})
    docs_inventario = analizar_por_lista(titulos_inventario, resultados, paginas_excluidas, "INVENTARIO", origen="inventario", rango_inventario=rango_inv)

    for d in docs_indice + docs_inventario:
        d['resumen'] = d['contenido'][:500] if d['contenido'] else "No disponible"

    texto_completo = "\n".join([d['contenido'] for d in docs_indice if d['encontrado']])
    resumen_global = texto_completo[:1000] + "..." if len(texto_completo) > 1000 else texto_completo

    integ_indice = verificar_integridad(titulos_indice, docs_indice)
    integ_inventario = verificar_integridad(titulos_inventario, docs_inventario)

    integridad = {
        'total_indice': integ_indice['total_esperados'], 'encontrados_indice': integ_indice['total_encontrados'],
        'total_inventario': integ_inventario['total_esperados'], 'encontrados_inventario': integ_inventario['total_encontrados'],
        'faltantes_indice': integ_indice['faltantes'], 'faltantes_inventario': integ_inventario['faltantes']
    }

    proyecto_data = {
        'documentos_por_indice': docs_indice, 'documentos_por_inventario': docs_inventario,
        'resumen_global': resumen_global, 'integridad': integridad
    }

    with open(ARCHIVO_SALIDA, 'w', encoding='utf-8') as f:
        json.dump(proyecto_data, f, ensure_ascii=False, indent=2)

    print(f"\n✅ Matriz de validación guardada exitosamente en {ARCHIVO_SALIDA}")
    return proyecto_data

if __name__ == "__main__":
    proyecto = analizar_proyecto()
    if proyecto:
        menu_busqueda(proyecto)