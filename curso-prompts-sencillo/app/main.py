"""
Servidor del curso (monolito): FastAPI da la API en /api y también
muestra la página de React ya compilada (frontend/dist).

Ejecutar:  uvicorn app.main:app --reload
"""

from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from .contenido import CALIFICACION_MINIMA, CURSO, ELEMENTOS, buscar_leccion, lecciones_publicas
from .evaluador import analizar_texto, evaluar_campos

DIST = Path(__file__).resolve().parent.parent / "frontend" / "dist"

app = FastAPI(title="Curso corto de prompts")


class Respuestas(BaseModel):
    respuestas: dict[str, int]


class Texto(BaseModel):
    texto: str = Field(min_length=1, max_length=4000)


class Campos(BaseModel):
    rol: str = Field(default="", max_length=600)
    objetivo: str = Field(default="", max_length=600)
    contexto: str = Field(default="", max_length=1200)
    instrucciones: str = Field(default="", max_length=1200)
    restricciones: str = Field(default="", max_length=600)
    formato: str = Field(default="", max_length=600)


@app.get("/api/curso")
def curso():
    """Todo el curso en una sola respuesta."""
    return {
        **CURSO,
        "calificacion_minima": CALIFICACION_MINIMA,
        "elementos": ELEMENTOS,
        "lecciones": lecciones_publicas(),
    }


def calificar(puntaje_100: float) -> dict:
    """Convierte un puntaje de 0-100 a calificación de 0-10 y dice si aprueba."""
    calificacion = round(puntaje_100 / 10, 1)
    return {"calificacion": calificacion, "aprobado": calificacion >= CALIFICACION_MINIMA}


@app.post("/api/lecciones/{leccion_id}/revisar")
def revisar(leccion_id: int, envio: Respuestas):
    """Revisa las preguntas de una lección y devuelve qué estuvo bien."""
    leccion = buscar_leccion(leccion_id)
    if not leccion or leccion["actividad"]["tipo"] != "preguntas":
        raise HTTPException(404, "Esta lección no tiene preguntas")
    detalle = [
        {
            "id": p["id"],
            "correcta": p["correcta"],
            "acierto": envio.respuestas.get(p["id"]) == p["correcta"],
            "explicacion": p["explicacion"],
        }
        for p in leccion["actividad"]["preguntas"]
    ]
    aciertos = sum(d["acierto"] for d in detalle)
    return {"aciertos": aciertos, "total": len(detalle), "detalle": detalle, **calificar(aciertos * 100 / len(detalle))}


@app.post("/api/analizar")
def analizar(entrada: Texto):
    resultado = analizar_texto(entrada.texto)
    return {**resultado, **calificar(resultado["puntaje"])}


@app.post("/api/evaluar")
def evaluar(campos: Campos):
    resultado = evaluar_campos(campos.model_dump())
    return {**resultado, **calificar(resultado["puntaje"])}


# ---------- Página web (React compilado) ----------
if DIST.exists():
    app.mount("/assets", StaticFiles(directory=DIST / "assets"), name="assets")

    @app.get("/{ruta:path}", include_in_schema=False)
    def pagina(ruta: str):
        archivo = DIST / ruta
        if ruta and archivo.is_file():
            return FileResponse(archivo)
        return FileResponse(DIST / "index.html")
