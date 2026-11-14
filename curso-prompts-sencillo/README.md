# Curso corto: Aprende a usar prompts para programar con IA

Versión **sencilla** del curso (≈28 minutos, 5 lecciones), hecha con **React + TypeScript** y **Python (FastAPI)** en un solo proyecto (monolito): el servidor de Python da la API y también muestra la página.

## Cómo ejecutarlo (Windows)

Abre una terminal dentro de la carpeta `curso-prompts-sencillo` y escribe:

```powershell
py -3.14 -m pip install -r requirements.txt
py -3.14 -m uvicorn app.main:app --reload
```

Abre **http://localhost:8000** en tu navegador. Para detenerlo: `Ctrl + C`.

> Si cambias algo en `frontend/src`, recompila con `cd frontend`, `npm install` y `npm run build`.

## Las 5 lecciones

| # | Lección | Min | Actividad |
|---|---|---|---|
| 1 | ¿Qué es un prompt? | 5 | 2 preguntas |
| 2 | Las 5 preguntas antes de escribir | 7 | 5 preguntas |
| 3 | Prompt básico vs. prompt completo | 6 | Analizador: ¿qué le falta al prompt? |
| 4 | Usa la IA con responsabilidad | 4 | 5 preguntas |
| 5 | Escribe tu propio prompt | 6 | Constructor: arma tu prompt y cópialo |

Cada lección tiene la misma forma: **Vas a aprender → explicación → Recuerda → Actividad**.

**Reglas:** cada actividad se califica de 0 a 10 y se aprueba con **8 o más**. Sin aprobar no se puede pasar a la siguiente lección ni terminar el curso (las lecciones siguientes aparecen con candado). Se puede intentar las veces que sea necesario. Al final se muestran las calificaciones y el promedio. El curso es sólo para aprender: no da constancia.

Para cambiar la calificación mínima, edita `CALIFICACION_MINIMA` en `app/contenido.py`.

## Archivos

```
curso-prompts-sencillo/
├── app/
│   ├── contenido.py   ← TODO el texto del curso (edita aquí)
│   ├── evaluador.py   ← revisa los prompts con palabras clave
│   └── main.py        ← servidor: /api/curso, /api/lecciones/{id}/revisar, /api/analizar, /api/evaluar
├── frontend/src/
│   ├── App.tsx        ← la página: encabezado, índice, lección
│   ├── Actividad.tsx  ← preguntas, analizador y constructor
│   ├── api.ts         ← llamadas al servidor
│   ├── types.ts       ← tipos de datos
│   └── styles.css     ← colores UNAM (azul #002B7A y oro #D59F0F)
└── requirements.txt
```

No usa base de datos ni registro: el avance y las calificaciones se recuerdan en el navegador de cada alumno.

## Publicar gratis en Render

1. Sube esta carpeta a un repositorio de GitHub (sin `frontend/node_modules`; la carpeta `frontend/dist` **sí** debe subirse).
2. En https://render.com crea un **Web Service** y conecta el repositorio.
3. Configura:
   - **Language:** Python 3
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   - **Instance Type:** Free
4. Presiona **Deploy**. La versión de Python (3.14) se toma del archivo `.python-version`.

En el plan gratuito el servicio se duerme tras 15 minutos sin visitas y tarda alrededor de un minuto en despertar.
