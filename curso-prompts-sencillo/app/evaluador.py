"""
Evaluador de prompts basado en reglas (no usa ninguna IA externa).

Dos modos:
  - evaluar_campos(): el alumno llenó el constructor pregunta por pregunta.
  - analizar_texto(): el alumno pega un prompt libre y detectamos qué elementos tiene.
"""

import re
import unicodedata

from .contenido import ELEMENTOS

NOMBRES = {e["clave"]: e["nombre"] for e in ELEMENTOS}

# Palabras clave (sin acentos, en minúsculas) que delatan cada elemento.
PISTAS: dict[str, list[str]] = {
    "rol": [
        "actua como", "actue como", "como si fueras", "eres un", "eres una", "asume el rol",
        "toma el rol", "en tu papel de", "experto en", "maestro de", "profesor de", "tutor",
    ],
    "objetivo": [
        "necesito", "quiero", "mi objetivo", "aprender", "comprender", "entender",
        "resolver", "practicar", "repasar", "me gustaria",
    ],
    "contexto": [
        "soy estudiante", "estudio", "estoy aprendiendo", "semestre", "materia", "curso",
        "ya se", "conozco", "tengo conocimientos", "mi nivel", "principiante", "basico",
        "programacion i", "en mi clase", "mi codigo", "me sale el error", "error",
    ],
    "instrucciones": [
        "explicame", "explica", "muestrame", "muestra", "plantea", "propon", "dame",
        "genera", "compara", "revisa", "corrige", "analiza", "describe", "guiame", "indica",
        "haz ", "escribe",
    ],
    "restricciones": [
        "no me des", "no des", "no uses", "no utilices", "no incluyas", "evita", "sin usar",
        "maximo", "como maximo", "no mas de", "unicamente", "solo con", "no resuelvas",
    ],
    "formato": [
        "tabla", "lista", "paso a paso", "pasos numerados", "vinetas", "codigo comentado",
        "comentado", "parrafo", "diagrama", "ejemplo", "ejercicio", "presenta", "en formato",
    ],
}

LENGUAJES = [
    "python", "java", "javascript", "typescript", "c++", "c#", "sql", "php", "kotlin",
    "go", "rust", "html", "css", "react", " en c ", " en c.", " en c,",
]

CONSEJOS: dict[str, str] = {
    "rol": "Empieza con \"Actúa como…\" (por ejemplo, un maestro de programación paciente).",
    "objetivo": "Di qué necesitas aprender o resolver con un verbo claro: comprender, practicar, depurar…",
    "contexto": "Cuenta tu nivel, la materia, el lenguaje y lo que ya sabes o intentaste.",
    "instrucciones": "Indica acciones concretas: explica paso a paso, compara, revisa mi código, plantea un ejercicio…",
    "restricciones": "Pon límites que te obliguen a razonar, como \"no me des la solución completa\".",
    "formato": "Pide una forma de presentación: pasos numerados, tabla, código comentado, ejemplo pequeño…",
}


def normalizar(texto: str) -> str:
    sin_acentos = unicodedata.normalize("NFD", texto.lower())
    sin_acentos = "".join(c for c in sin_acentos if unicodedata.category(c) != "Mn")
    return re.sub(r"\s+", " ", f" {sin_acentos} ")


def _tiene(texto_norm: str, clave: str) -> list[str]:
    return [p for p in PISTAS[clave] if p in texto_norm]


def nivel(puntaje: int) -> str:
    if puntaje >= 80:
        return "Estructurado"
    if puntaje >= 50:
        return "En desarrollo"
    return "Básico"


def ensamblar(campos: dict[str, str]) -> str:
    """Une los campos en un solo prompt listo para copiar."""
    partes: list[str] = []

    def limpio(clave: str) -> str:
        return campos.get(clave, "").strip().rstrip(".")

    if rol := limpio("rol"):
        partes.append(rol if normalizar(rol).strip().startswith("actua") else f"Actúa como {rol}")
    if contexto := limpio("contexto"):
        partes.append(contexto)
    if objetivo := limpio("objetivo"):
        partes.append(objetivo)
    if instrucciones := limpio("instrucciones"):
        partes.append(instrucciones)
    if restricciones := limpio("restricciones"):
        partes.append(restricciones)
    if formato := limpio("formato"):
        partes.append(formato)
    return ". ".join(partes) + ("." if partes else "")


def evaluar_campos(campos: dict[str, str]) -> dict:
    """Califica cada respuesta del constructor (0-100) y da sugerencias."""
    resultados = []
    for e in ELEMENTOS:
        clave = e["clave"]
        valor = campos.get(clave, "").strip()
        norm = normalizar(valor)
        palabras = len(valor.split())

        if not valor:
            puntos, estado, nota = 0, "falta", f"Falta el {e['nombre'].lower()}. {CONSEJOS[clave]}"
        elif palabras < (2 if clave == "rol" else 4):
            puntos, estado, nota = 40, "mejorable", f"Muy breve. {CONSEJOS[clave]}"
        else:
            puntos, estado, nota = 80, "bien", "Bien planteado."
            # Bonificaciones específicas por elemento
            if clave == "contexto":
                menciona_lenguaje = any(l in norm for l in LENGUAJES)
                if menciona_lenguaje and _tiene(norm, "contexto"):
                    puntos, nota = 100, "Excelente: indicas tu nivel y el lenguaje."
                elif not menciona_lenguaje:
                    nota = "Bien, pero menciona el lenguaje de programación que usas."
                else:
                    nota = "Bien, añade qué sabes ya o en qué materia/semestre estás."
            elif clave == "restricciones":
                if any(p in norm for p in ("solucion", "resuelvas", "respuesta completa", "codigo completo")):
                    puntos, nota = 100, "Excelente: tu restricción te obliga a razonar."
                else:
                    nota = "Bien. Para aprender, considera pedir que no te den la solución completa."
            elif _tiene(norm, clave):
                puntos, nota = 100, "Excelente."
            else:
                nota = f"Correcto. {CONSEJOS[clave]}"

        resultados.append(
            {"clave": clave, "nombre": e["nombre"], "puntos": puntos, "estado": estado, "nota": nota}
        )

    puntaje = round(sum(r["puntos"] for r in resultados) / len(resultados))
    return {
        "puntaje": puntaje,
        "nivel": nivel(puntaje),
        "elementos": resultados,
        "prompt_final": ensamblar(campos),
    }


def analizar_texto(texto: str) -> dict:
    """Detecta qué elementos contiene un prompt escrito libremente."""
    norm = normalizar(texto)
    resultados = []
    for e in ELEMENTOS:
        clave = e["clave"]
        encontradas = _tiene(norm, clave)
        if clave == "contexto" and any(l in norm for l in LENGUAJES):
            encontradas.append("lenguaje de programación")
        presente = bool(encontradas)
        resultados.append(
            {
                "clave": clave,
                "nombre": e["nombre"],
                "presente": presente,
                "pistas": encontradas[:3],
                "nota": "Detectado." if presente else CONSEJOS[clave],
            }
        )

    presentes = sum(r["presente"] for r in resultados)
    puntaje = round(presentes / len(resultados) * 100)
    palabras = len(texto.split())
    if palabras < 12 and puntaje > 50:  # un texto muy corto no puede estar tan completo
        puntaje = 50
    return {
        "puntaje": puntaje,
        "nivel": nivel(puntaje),
        "palabras": palabras,
        "elementos": resultados,
    }
