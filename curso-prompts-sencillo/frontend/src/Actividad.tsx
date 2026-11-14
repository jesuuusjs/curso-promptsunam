// Las 3 clases de actividad: preguntas, analizador y constructor de prompts.
import { useState, type ReactNode } from "react";
import { api, type Analisis, type Calificado, type Evaluacion, type Revision } from "./api";
import type { Actividad as TActividad, Clave, Elemento, Pregunta } from "./types";

type AlCalificar = (resultado: Calificado) => void;

export default function Actividad({
  leccionId,
  actividad,
  elementos,
  minima,
  alCalificar,
}: {
  leccionId: number;
  actividad: TActividad;
  elementos: Elemento[];
  minima: number;
  alCalificar: AlCalificar;
}) {
  if (actividad.tipo === "preguntas")
    return <Preguntas leccionId={leccionId} preguntas={actividad.preguntas} minima={minima} alCalificar={alCalificar} />;
  if (actividad.tipo === "analizador")
    return (
      <Analizador instruccion={actividad.instruccion} inicial={actividad.texto_inicial} minima={minima} alCalificar={alCalificar} />
    );
  return <Constructor instruccion={actividad.instruccion} elementos={elementos} minima={minima} alCalificar={alCalificar} />;
}

/* ---------------- Preguntas de opción múltiple ---------------- */
function Preguntas({
  leccionId,
  preguntas,
  minima,
  alCalificar,
}: {
  leccionId: number;
  preguntas: Pregunta[];
  minima: number;
  alCalificar: AlCalificar;
}) {
  const [elegidas, setElegidas] = useState<Record<string, number>>({});
  const [revision, setRevision] = useState<Revision | null>(null);
  const completas = preguntas.every((p) => elegidas[p.id] !== undefined);

  const revisar = async () => {
    const r = await api.revisar(leccionId, elegidas);
    setRevision(r);
    alCalificar(r);
  };

  return (
    <div>
      {preguntas.map((p, i) => {
        const r = revision?.detalle.find((d) => d.id === p.id);
        return (
          <fieldset key={p.id} className="pregunta" disabled={!!revision}>
            <legend>
              {preguntas.length > 1 && `${i + 1}. `}
              {p.pregunta}
            </legend>
            {p.opciones.map((op, j) => {
              let clase = "opcion";
              if (elegidas[p.id] === j) clase += " opcion--elegida";
              if (r && j === r.correcta) clase += " opcion--bien";
              else if (r && elegidas[p.id] === j) clase += " opcion--mal";
              return (
                <label key={j} className={clase}>
                  <input
                    type="radio"
                    name={p.id}
                    checked={elegidas[p.id] === j}
                    onChange={() => setElegidas((e) => ({ ...e, [p.id]: j }))}
                  />
                  {op}
                </label>
              );
            })}
            {r && <p className={r.acierto ? "nota nota--bien" : "nota nota--mal"}>{r.explicacion}</p>}
          </fieldset>
        );
      })}

      {revision ? (
        <div className="resultado">
          <Calificacion calificacion={revision.calificacion} aprobado={revision.aprobado} minima={minima}>
            {revision.aciertos} de {revision.total} correctas
          </Calificacion>
          <button
            className="boton boton--claro"
            onClick={() => {
              setElegidas({});
              setRevision(null);
            }}
          >
            Intentar otra vez
          </button>
        </div>
      ) : (
        <button className="boton" disabled={!completas} onClick={revisar}>
          Revisar respuestas
        </button>
      )}
    </div>
  );
}

/* ---------------- Analizador: ¿qué le falta a mi prompt? ---------------- */
function Analizador({
  instruccion,
  inicial,
  minima,
  alCalificar,
}: {
  instruccion: string;
  inicial: string;
  minima: number;
  alCalificar: AlCalificar;
}) {
  const [texto, setTexto] = useState(inicial);
  const [analisis, setAnalisis] = useState<Analisis | null>(null);

  return (
    <div>
      <p className="instruccion">{instruccion}</p>
      <textarea
        rows={5}
        value={texto}
        onChange={(e) => {
          setTexto(e.target.value);
          setAnalisis(null);
        }}
        aria-label="Tu prompt"
      />
      <button
        className="boton"
        disabled={!texto.trim()}
        onClick={async () => {
          const r = await api.analizar(texto);
          setAnalisis(r);
          alCalificar(r);
        }}
      >
        Revisar
      </button>

      {analisis && (
        <div className="revision">
          <Calificacion calificacion={analisis.calificacion} aprobado={analisis.aprobado} minima={minima}>
            Nivel: {analisis.nivel}
          </Calificacion>
          <ul className="cotejo">
            {analisis.elementos.map((e) => (
              <li key={e.clave} className={e.presente ? "si" : "no"}>
                <span aria-hidden>{e.presente ? "✓" : "✕"}</span>
                <div>
                  <b>{e.nombre}</b>
                  {!e.presente && <p>{e.nota}</p>}
                </div>
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}

/* ---------------- Constructor: arma tu prompt paso a paso ---------------- */
function Constructor({
  instruccion,
  elementos,
  minima,
  alCalificar,
}: {
  instruccion: string;
  elementos: Elemento[];
  minima: number;
  alCalificar: AlCalificar;
}) {
  const vacio = Object.fromEntries(elementos.map((e) => [e.clave, ""])) as Record<Clave, string>;
  const [campos, setCampos] = useState(vacio);
  const [evaluacion, setEvaluacion] = useState<Evaluacion | null>(null);
  const [copiado, setCopiado] = useState(false);

  const notas = Object.fromEntries((evaluacion?.elementos ?? []).map((e) => [e.clave, e]));
  const hayTexto = Object.values(campos).some((v) => v.trim());

  const copiar = async () => {
    try {
      await navigator.clipboard.writeText(evaluacion!.prompt_final);
      setCopiado(true);
      setTimeout(() => setCopiado(false), 1500);
    } catch {
      /* el navegador no permite copiar */
    }
  };

  return (
    <div>
      <p className="instruccion">{instruccion}</p>
      {elementos.map((e, i) => {
        const n = notas[e.clave];
        return (
          <label key={e.clave} className="campo">
            <span>
              <b>
                {i + 1}. {e.nombre}
              </b>{" "}
              — {e.pregunta}
            </span>
            <textarea
              rows={2}
              placeholder={e.ejemplo}
              value={campos[e.clave]}
              onChange={(ev) => {
                setCampos((c) => ({ ...c, [e.clave]: ev.target.value }));
                setEvaluacion(null);
              }}
            />
            {n && n.estado !== "bien" && <span className="nota nota--mal">{n.nota}</span>}
          </label>
        );
      })}
      <button
        className="boton"
        disabled={!hayTexto}
        onClick={async () => {
          const r = await api.evaluar(campos);
          setEvaluacion(r);
          alCalificar(r);
        }}
      >
        Ver mi prompt
      </button>

      {evaluacion && (
        <div className="revision">
          <Calificacion calificacion={evaluacion.calificacion} aprobado={evaluacion.aprobado} minima={minima}>
            Nivel: {evaluacion.nivel}
          </Calificacion>
          <p className="etiqueta">Tu prompt:</p>
          <p className="prompt">{evaluacion.prompt_final}</p>
          <button className="boton boton--claro" onClick={copiar}>
            {copiado ? "¡Copiado!" : "Copiar prompt"}
          </button>
        </div>
      )}
    </div>
  );
}

function Calificacion({
  calificacion,
  aprobado,
  minima,
  children,
}: {
  calificacion: number;
  aprobado: boolean;
  minima: number;
  children: ReactNode;
}) {
  return (
    <div className={`calificacion ${aprobado ? "calificacion--bien" : "calificacion--mal"}`}>
      <strong>{calificacion.toFixed(1)}</strong>
      <span>
        de 10 · {children}
        <small>
          {aprobado
            ? "¡Aprobada! Ya puedes pasar a la siguiente lección."
            : `Necesitas ${minima} o más para continuar. Revisa y vuelve a intentarlo.`}
        </small>
      </span>
    </div>
  );
}
