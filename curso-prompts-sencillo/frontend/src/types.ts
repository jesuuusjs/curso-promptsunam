// Tipos que coinciden con lo que responde el servidor de Python.

export type Clave = "rol" | "objetivo" | "contexto" | "instrucciones" | "restricciones" | "formato";

export interface Elemento {
  clave: Clave;
  nombre: string;
  pregunta: string;
  ejemplo: string;
}

export type Bloque =
  | { tipo: "parrafo"; texto: string }
  | { tipo: "dato"; cifra: string; texto: string; fuente: string }
  | { tipo: "lista"; titulo: string; items: string[] }
  | { tipo: "cinco" }
  | { tipo: "comparar"; malo: string; malo_nota: string; bueno: string; bueno_nota: string };

export interface Pregunta {
  id: string;
  pregunta: string;
  opciones: string[];
}

export type Actividad =
  | { tipo: "preguntas"; preguntas: Pregunta[] }
  | { tipo: "analizador"; instruccion: string; texto_inicial: string }
  | { tipo: "constructor"; instruccion: string };

export interface Leccion {
  id: number;
  titulo: string;
  minutos: number;
  meta: string;
  bloques: Bloque[];
  recuerda: string;
  actividad: Actividad;
}

export interface Curso {
  titulo: string;
  descripcion: string;
  institucion: string;
  aviso: string;
  calificacion_minima: number;
  elementos: Elemento[];
  lecciones: Leccion[];
}
