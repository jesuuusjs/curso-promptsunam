"""
Contenido del curso corto (≈28 min): "Aprende a usar prompts para programar con IA".

Todo el curso son 5 lecciones. Cada lección tiene la misma forma:
    meta        → lo que vas a aprender (una frase)
    bloques     → la explicación (párrafos, listas, ejemplos…)
    recuerda    → la idea principal en una frase
    actividad   → preguntas, analizador o constructor de prompts

Para cambiar textos, tiempos o preguntas sólo edita este archivo.
Las respuestas correctas se quedan en el servidor: el navegador no las ve.
"""

from typing import Any

# Los 6 elementos de un prompt (los usa el constructor y el evaluador)
ELEMENTOS: list[dict[str, str]] = [
    {"clave": "rol", "nombre": "Rol", "pregunta": "¿Qué papel debe tomar la IA?",
     "ejemplo": "Actúa como un maestro de programación paciente."},
    {"clave": "objetivo", "nombre": "Objetivo", "pregunta": "¿Qué necesito aprender o resolver?",
     "ejemplo": "Necesito entender cómo funciona el método burbuja."},
    {"clave": "contexto", "nombre": "Contexto", "pregunta": "¿Qué sé y cuál es mi problema?",
     "ejemplo": "Soy estudiante de Programación II, estoy aprendiendo ordenamiento en C y ya sé usar arreglos."},
    {"clave": "instrucciones", "nombre": "Instrucciones", "pregunta": "¿Qué debe hacer la IA?",
     "ejemplo": "Explícamelo paso a paso con un arreglo de 5 números y déjame un ejercicio."},
    {"clave": "restricciones", "nombre": "Restricciones", "pregunta": "¿Qué NO debe hacer la IA?",
     "ejemplo": "No me des la solución del ejercicio."},
    {"clave": "formato", "nombre": "Formato", "pregunta": "¿Cómo quiero la respuesta?",
     "ejemplo": "Usa pasos numerados y código en C con comentarios."},
]

PROMPT_BASICO = "Haz un programa que ordene números de menor a mayor."

PROMPT_ESTRUCTURADO = (
    "Actúa como un maestro de programación. Soy estudiante de Programación II y estoy "
    "aprendiendo algoritmos de ordenamiento en C. Necesito comprender cómo funciona el "
    "método de burbuja. Explícame el procedimiento paso a paso con un arreglo de cinco "
    "números y, al final, plantea un ejercicio para resolverlo por mi cuenta. "
    "No me des la solución del ejercicio."
)

# Calificación mínima (sobre 10) para aprobar la actividad de cada lección
CALIFICACION_MINIMA = 8

CURSO = {
    "titulo": "Aprende a usar prompts para programar con IA",
    "descripcion": (
        "Un curso corto para que la inteligencia artificial te ayude a aprender a programar, "
        "y no sólo te haga la tarea."
    ),
    "institucion": "Licenciatura en Informática · Facultad de Estudios Superiores Cuautitlán · UNAM",
    "aviso": "Este curso es sólo para aprender: no otorga constancia ni calificación oficial.",
}

LECCIONES: list[dict[str, Any]] = [
    # ------------------------------------------------------------------ 1
    {
        "id": 1,
        "titulo": "¿Qué es un prompt?",
        "minutos": 5,
        "meta": "Saber qué es un prompt y por qué importa cómo lo escribes.",
        "bloques": [
            {"tipo": "parrafo", "texto": (
                "Hoy muchos estudiantes usan inteligencia artificial (IA) como ChatGPT, Claude o Gemini "
                "para hacer tareas. Pero usarla no es lo mismo que aprovecharla para aprender."
            )},
            {"tipo": "dato", "cifra": "37.2 %",
             "texto": "de los estudiantes de la UNAM no está seguro de cómo usar la IA para aprender.",
             "fuente": "Gaceta UNAM, 2026"},
            {"tipo": "parrafo", "texto": (
                "Un prompt es lo que le escribes a la IA: tu pregunta o tu instrucción. "
                "Según la Dirección General de Bibliotecas de la UNAM, es «un conjunto de instrucciones "
                "estructuradas que se le da a una inteligencia artificial»."
            )},
            {"tipo": "parrafo", "texto": (
                "Si tu prompt es vago, la respuesta también lo será. Si tu prompt es claro y completo, "
                "la IA te puede explicar como un buen maestro."
            )},
        ],
        "recuerda": "Un prompt es la instrucción que le das a la IA. Mientras más claro, mejor la respuesta.",
        "actividad": {
            "tipo": "preguntas",
            "preguntas": [
                {
                    "id": "1a",
                    "pregunta": "¿Qué es un prompt?",
                    "opciones": [
                        "Un lenguaje de programación",
                        "La instrucción o pregunta que le escribes a la IA",
                        "Un programa que instala la IA",
                    ],
                    "correcta": 1,
                    "explicacion": "Un prompt es la instrucción que le das a la IA.",
                },
                {
                    "id": "1b",
                    "pregunta": "¿Qué pasa si tu prompt es vago o incompleto?",
                    "opciones": [
                        "La IA adivina exactamente lo que quieres",
                        "La respuesta también será vaga o poco útil",
                        "La IA se niega a responder",
                    ],
                    "correcta": 1,
                    "explicacion": "Si el prompt es vago, la respuesta también lo será.",
                },
            ],
        },
    },
    # ------------------------------------------------------------------ 2
    {
        "id": 2,
        "titulo": "Las 5 preguntas antes de escribir",
        "minutos": 7,
        "meta": "Conocer las 5 preguntas que te ayudan a escribir un buen prompt.",
        "bloques": [
            {"tipo": "parrafo", "texto": (
                "Antes de escribirle a la IA, respóndete estas 5 preguntas. Cada respuesta es una parte "
                "de tu prompt. Además, puedes empezar diciéndole a la IA qué papel tomar: "
                "«Actúa como un maestro de programación»."
            )},
            {"tipo": "cinco"},
        ],
        "recuerda": "Objetivo, contexto, instrucciones, restricciones y formato (y el rol al inicio).",
        "actividad": {
            "tipo": "preguntas",
            "preguntas": [
                {
                    "id": "2a",
                    "pregunta": "«Soy estudiante de primer semestre y ya sé usar ciclos for» es…",
                    "opciones": ["El objetivo", "El contexto", "El formato"],
                    "correcta": 1,
                    "explicacion": "Cuenta lo que sabes y tu situación: eso es el contexto.",
                },
                {
                    "id": "2b",
                    "pregunta": "«No me des la solución» es…",
                    "opciones": ["Una restricción", "Un rol", "Un objetivo"],
                    "correcta": 0,
                    "explicacion": "Le dice a la IA lo que NO debe hacer: es una restricción.",
                },
                {
                    "id": "2c",
                    "pregunta": "«Explícalo en una tabla» es…",
                    "opciones": ["El contexto", "Las instrucciones", "El formato"],
                    "correcta": 2,
                    "explicacion": "Dice cómo quieres ver la respuesta: es el formato.",
                },
                {
                    "id": "2d",
                    "pregunta": "¿Qué parte responde «¿Qué necesito aprender o resolver?»",
                    "opciones": ["Las restricciones", "El objetivo", "El rol"],
                    "correcta": 1,
                    "explicacion": "Lo que necesitas aprender o resolver es tu objetivo.",
                },
                {
                    "id": "2e",
                    "pregunta": "«Actúa como un maestro de programación» es…",
                    "opciones": ["El rol", "El formato", "El contexto"],
                    "correcta": 0,
                    "explicacion": "Le dice a la IA qué papel tomar: es el rol.",
                },
            ],
        },
    },
    # ------------------------------------------------------------------ 3
    {
        "id": 3,
        "titulo": "Prompt básico vs. prompt completo",
        "minutos": 6,
        "meta": "Ver la diferencia entre un prompt pobre y uno bien hecho.",
        "bloques": [
            {"tipo": "parrafo", "texto": "Mira estos dos prompts sobre el mismo tema: ordenar números."},
            {"tipo": "comparar",
             "malo": PROMPT_BASICO,
             "malo_nota": "No dice el lenguaje, ni qué sabes, ni que quieres aprender. La IA sólo te dará código.",
             "bueno": PROMPT_ESTRUCTURADO,
             "bueno_nota": "Tiene rol, contexto, objetivo, instrucciones y una restricción. La IA te enseñará."},
            {"tipo": "parrafo", "texto": (
                "El segundo prompt no sólo te da una solución: te explica y te deja practicar "
                "para que compruebes si de verdad aprendiste."
            )},
        ],
        "recuerda": "Un prompt completo convierte a la IA en un maestro, no en una máquina de respuestas.",
        "actividad": {
            "tipo": "analizador",
            "instruccion": (
                "Este es el prompt básico. Presiona «Revisar» para ver qué le falta. "
                "Agrégale lo que falta y vuelve a revisar hasta sacar 8 o más."
            ),
            "texto_inicial": PROMPT_BASICO,
        },
    },
    # ------------------------------------------------------------------ 4
    {
        "id": 4,
        "titulo": "Usa la IA con responsabilidad",
        "minutos": 4,
        "meta": "Evitar que la IA piense por ti.",
        "bloques": [
            {"tipo": "parrafo", "texto": (
                "La IA no es mala. El problema es depender de ella: si sólo copias el código, no aprendes "
                "por qué funciona y dejas de practicar tu razonamiento."
            )},
            {"tipo": "lista", "titulo": "Buenas costumbres", "items": [
                "Intenta resolver el problema primero y comparte tu intento con la IA.",
                "Pide explicaciones y ejercicios, no sólo el código terminado.",
                "Revisa lo que te responde: la IA también se equivoca.",
                "Sigue las reglas de tu profesor sobre el uso de IA.",
            ]},
        ],
        "recuerda": "Usa la IA para entender, no para copiar.",
        "actividad": {
            "tipo": "preguntas",
            "preguntas": [
                {
                    "id": "4a",
                    "pregunta": "¿Cuál es el mayor riesgo de copiar el código de la IA sin leerlo?",
                    "opciones": [
                        "Que el código quede muy largo",
                        "Que no aprendas a razonar ni entiendas por qué funciona",
                        "Que la computadora se haga lenta",
                    ],
                    "correcta": 1,
                    "explicacion": "Si sólo copias, no desarrollas tu razonamiento ni tu pensamiento crítico.",
                },
                {
                    "id": "4b",
                    "pregunta": "¿Qué es mejor para aprender?",
                    "opciones": [
                        "Pedir la solución completa",
                        "Compartir tu intento y pedir que te explique tu error",
                        "Usar la primera respuesta sin revisarla",
                    ],
                    "correcta": 1,
                    "explicacion": "Al compartir tu intento, la IA te guía y tú sigues pensando.",
                },
                {
                    "id": "4c",
                    "pregunta": "¿La IA siempre tiene la razón?",
                    "opciones": [
                        "Sí, nunca se equivoca",
                        "No, hay que revisar lo que responde",
                        "Sólo se equivoca en temas de historia",
                    ],
                    "correcta": 1,
                    "explicacion": "La IA también se equivoca: siempre revisa su respuesta.",
                },
                {
                    "id": "4d",
                    "pregunta": "¿Qué conviene hacer antes de pedirle ayuda a la IA?",
                    "opciones": [
                        "Intentar resolver el problema por tu cuenta",
                        "Nada, preguntar de inmediato",
                        "Copiar la tarea de un compañero",
                    ],
                    "correcta": 0,
                    "explicacion": "Tu intento te hace pensar y además le da contexto a la IA.",
                },
                {
                    "id": "4e",
                    "pregunta": "Según el curso, ¿para qué debes usar la IA?",
                    "opciones": [
                        "Para copiar el código más rápido",
                        "Para entender y practicar",
                        "Para no tener que estudiar",
                    ],
                    "correcta": 1,
                    "explicacion": "Usa la IA para entender, no para copiar.",
                },
            ],
        },
    },
    # ------------------------------------------------------------------ 5
    {
        "id": 5,
        "titulo": "Escribe tu propio prompt",
        "minutos": 6,
        "meta": "Armar un prompt completo para un tema de programación.",
        "bloques": [
            {"tipo": "parrafo", "texto": (
                "Ahora te toca. Elige un tema que estés viendo en clase (o uno de estos) y responde "
                "las preguntas. Al final tendrás un prompt listo para copiar en tu IA favorita."
            )},
            {"tipo": "lista", "titulo": "Ideas de temas", "items": [
                "La diferencia entre while y do-while en C.",
                "Cómo recorrer una matriz en Java.",
                "Por qué mi función recursiva en Python nunca termina.",
            ]},
        ],
        "recuerda": "Usa esta misma estructura cada vez que le pidas ayuda a la IA.",
        "actividad": {
            "tipo": "constructor",
            "instruccion": (
                "Llena cada casilla con tu propio tema. Puedes ver un ejemplo en gris dentro de cada una. "
                "Tu prompt necesita 8 o más para aprobar."
            ),
        },
    },
]


def lecciones_publicas() -> list[dict[str, Any]]:
    """Las lecciones SIN las respuestas correctas."""
    resultado = []
    for lec in LECCIONES:
        copia = {**lec, "actividad": dict(lec["actividad"])}
        if copia["actividad"]["tipo"] == "preguntas":
            copia["actividad"]["preguntas"] = [
                {"id": p["id"], "pregunta": p["pregunta"], "opciones": p["opciones"]}
                for p in lec["actividad"]["preguntas"]
            ]
        resultado.append(copia)
    return resultado


def buscar_leccion(leccion_id: int) -> dict[str, Any] | None:
    return next((l for l in LECCIONES if l["id"] == leccion_id), None)
