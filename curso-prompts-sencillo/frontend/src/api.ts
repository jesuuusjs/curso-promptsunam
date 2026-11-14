// Funciones para hablar con el servidor de Python.
import type { Clave, Curso } from "./types";

async function pedir<T>(ruta: string, datos?: unknown): Promise<T> {
  const resp = await fetch(`/api${ruta}`, {
    method: datos ? "POST" : "GET",
    headers: { "Content-Type": "application/json" },
    body: datos ? JSON.stringify(datos) : undefined,
  });
  if (!resp.ok) throw new Error(`Error ${resp.status}`);
  return resp.json();
}

// Toda actividad devuelve una calificación de 0 a 10 y si aprobó
export interface Calificado {
  calificacion: number;
  aprobado: boolean;
}

export interface Revision extends Calificado {
  aciertos: number;
  total: number;
  detalle: { id: string; correcta: number; acierto: boolean; explicacion: string }[];
}

export interface Analisis extends Calificado {
  puntaje: number;
  nivel: string;
  elementos: { clave: Clave; nombre: string; presente: boolean; nota: string }[];
}

export interface Evaluacion extends Calificado {
  puntaje: number;
  nivel: string;
  prompt_final: string;
  elementos: { clave: Clave; nombre: string; estado: "falta" | "mejorable" | "bien"; nota: string }[];
}

export const api = {
  curso: () => pedir<Curso>("/curso"),
  revisar: (leccionId: number, respuestas: Record<string, number>) =>
    pedir<Revision>(`/lecciones/${leccionId}/revisar`, { respuestas }),
  analizar: (texto: string) => pedir<Analisis>("/analizar", { texto }),
  evaluar: (campos: Record<Clave, string>) => pedir<Evaluacion>("/evaluar", campos),
};
