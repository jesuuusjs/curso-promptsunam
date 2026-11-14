import { useEffect, useState } from "react";
import { api, type Calificado } from "./api";
import Actividad from "./Actividad";
import type { Bloque, Curso, Elemento, Leccion } from "./types";

// El avance se recuerda en este navegador (si el navegador lo permite).
const CLAVE = "curso-prompts-sencillo:v2";

interface Avance {
  actual: number; // índice de la lección que se está viendo
  notas: Record<number, number>; // mejor calificación APROBADA de cada lección (id → 0-10)
}

function leerAvance(): Avance {
  try {
    const guardado = JSON.parse(localStorage.getItem(CLAVE) ?? "");
    if (typeof guardado.actual === "number" && typeof guardado.notas === "object") return guardado;
  } catch {
    /* sin datos guardados */
  }
  return { actual: 0, notas: {} };
}

export default function App() {
  const [curso, setCurso] = useState<Curso | null>(null);
  const [error, setError] = useState(false);
  const [avance, setAvance] = useState(leerAvance);
  const [verFinal, setVerFinal] = useState(false);

  useEffect(() => {
    api.curso().then(setCurso).catch(() => setError(true));
  }, []);

  useEffect(() => {
    try {
      localStorage.setItem(CLAVE, JSON.stringify(avance));
    } catch {
      /* el navegador no deja guardar: no pasa nada */
    }
  }, [avance]);

  if (error) return <p className="aviso">No se pudo conectar con el servidor. ¿Está corriendo Python?</p>;
  if (!curso) return <p className="aviso">Cargando curso…</p>;

  const lecciones = curso.lecciones;
  const total = lecciones.length;
  const minima = curso.calificacion_minima;
  const aprobada = (l: Leccion) => avance.notas[l.id] !== undefined;
  // Una lección se desbloquea cuando la anterior está aprobada
  const desbloqueada = (i: number) => i === 0 || aprobada(lecciones[i - 1]);
  const aprobadas = lecciones.filter(aprobada).length;
  const terminado = aprobadas === total;

  const actual = Math.min(avance.actual, total - 1);
  const leccion = lecciones[actual];
  const minutos = lecciones.reduce((s, l) => s + l.minutos, 0);
  const porcentaje = Math.round((aprobadas / total) * 100);

  const irA = (i: number) => {
    if (!desbloqueada(i)) return;
    setVerFinal(false);
    setAvance((a) => ({ ...a, actual: i }));
    window.scrollTo({ top: 0, behavior: "smooth" });
  };

  // Guarda la calificación si aprobó (se queda con la mejor)
  const alCalificar = (r: Calificado) => {
    if (!r.aprobado) return;
    setAvance((a) => ({
      ...a,
      notas: { ...a.notas, [leccion.id]: Math.max(r.calificacion, a.notas[leccion.id] ?? 0) },
    }));
  };

  const siguiente = () => {
    if (!aprobada(leccion)) return;
    if (actual === total - 1) {
      setVerFinal(true);
      window.scrollTo({ top: 0, behavior: "smooth" });
    } else irA(actual + 1);
  };

  return (
    <>
      <header className="cabecera">
        <div className="contenedor">
          <p className="cabecera__escuela">UNAM · FES Cuautitlán · Licenciatura en Informática</p>
          <h1>{curso.titulo}</h1>
          <p className="cabecera__desc">{curso.descripcion}</p>
          <p className="chips">
            <span>{total} lecciones</span>
            <span>{minutos} minutos</span>
            <span>Aprueba cada lección con {minima} o más</span>
            <span>Sólo para aprender · sin constancia</span>
          </p>
        </div>
      </header>

      <div className="contenedor cuerpo">
        <nav className="indice" aria-label="Lecciones">
          <div className="avance">
            <span>
              Aprobadas: {aprobadas} de {total}
            </span>
            <div className="avance__barra">
              <b style={{ width: `${porcentaje}%` }} />
            </div>
          </div>
          <ol>
            {lecciones.map((l, i) => {
              const abierta = desbloqueada(i);
              const nota = avance.notas[l.id];
              const activa = i === actual && !verFinal;
              return (
                <li key={l.id}>
                  <button
                    className={`${activa ? "activa" : ""} ${nota !== undefined ? "hecha" : ""}`}
                    onClick={() => irA(i)}
                    disabled={!abierta}
                    aria-current={activa ? "step" : undefined}
                    title={abierta ? l.titulo : "Aprueba la lección anterior para desbloquearla"}
                  >
                    <span className="indice__num">{nota !== undefined ? "✓" : abierta ? l.id : "🔒"}</span>
                    <span className="indice__texto">
                      {l.titulo}
                      <small>
                        {l.minutos} min
                        {nota !== undefined && ` · Calificación ${nota.toFixed(1)}`}
                        {!abierta && " · Bloqueada"}
                      </small>
                    </span>
                  </button>
                </li>
              );
            })}
          </ol>
          {terminado && !verFinal && (
            <button className="boton boton--claro indice__final" onClick={() => setVerFinal(true)}>
              Ver mis resultados
            </button>
          )}
        </nav>

        <main className="tarjeta">
          {verFinal && terminado ? (
            <Final
              curso={curso}
              notas={avance.notas}
              onReiniciar={() => {
                setAvance({ actual: 0, notas: {} });
                setVerFinal(false);
              }}
            />
          ) : (
            <article key={leccion.id}>
              <p className="etiqueta">
                Lección {leccion.id} de {total} · {leccion.minutos} min
              </p>
              <h2>{leccion.titulo}</h2>

              <div className="meta">
                <b>Vas a aprender:</b> {leccion.meta}
              </div>

              {leccion.bloques.map((b, i) => (
                <BloqueVista key={i} bloque={b} elementos={curso.elementos} />
              ))}

              <div className="recuerda">
                <b>Recuerda</b>
                <p>{leccion.recuerda}</p>
              </div>

              <section className="actividad">
                <h3>
                  Actividad <span className="actividad__req">Calificación mínima: {minima}</span>
                </h3>
                <Actividad
                  leccionId={leccion.id}
                  actividad={leccion.actividad}
                  elementos={curso.elementos}
                  minima={minima}
                  alCalificar={alCalificar}
                />
              </section>

              <div className="botones">
                <button className="boton boton--claro" onClick={() => irA(actual - 1)} disabled={actual === 0}>
                  ← Anterior
                </button>
                <button className="boton" onClick={siguiente} disabled={!aprobada(leccion)}>
                  {actual === total - 1 ? "Terminar curso ✓" : "Siguiente lección →"}
                </button>
              </div>
              {!aprobada(leccion) && (
                <p className="candado">
                  🔒 Aprueba la actividad con {minima} o más para{" "}
                  {actual === total - 1 ? "terminar el curso" : "pasar a la siguiente lección"}.
                </p>
              )}
            </article>
          )}
        </main>
      </div>

      <footer className="pie">
        <div className="contenedor">
          <p>{curso.institucion}</p>
          <p className="pie__nota">Universidad Nacional Autónoma de México</p>
        </div>
      </footer>
    </>
  );
}

function BloqueVista({ bloque, elementos }: { bloque: Bloque; elementos: Elemento[] }) {
  switch (bloque.tipo) {
    case "parrafo":
      return <p className="parrafo">{bloque.texto}</p>;
    case "dato":
      return (
        <div className="dato">
          <strong>{bloque.cifra}</strong>
          <span>
            {bloque.texto}
            <small>Fuente: {bloque.fuente}</small>
          </span>
        </div>
      );
    case "lista":
      return (
        <div className="lista">
          <b>{bloque.titulo}</b>
          <ul>
            {bloque.items.map((it) => (
              <li key={it}>{it}</li>
            ))}
          </ul>
        </div>
      );
    case "cinco":
      return (
        <ol className="cinco">
          {elementos.map((e, i) => (
            <li key={e.clave}>
              <span className="cinco__num">{i === 0 ? "★" : i}</span>
              <div>
                <b>
                  {e.nombre}
                  {i === 0 && <em> (opcional, va al inicio)</em>}
                </b>
                <p>{e.pregunta}</p>
                <code>{e.ejemplo}</code>
              </div>
            </li>
          ))}
        </ol>
      );
    case "comparar":
      return (
        <div className="comparar">
          <div className="comparar__caja comparar__caja--malo">
            <b>✕ Prompt básico</b>
            <p className="prompt">{bloque.malo}</p>
            <p>{bloque.malo_nota}</p>
          </div>
          <div className="comparar__caja comparar__caja--bueno">
            <b>✓ Prompt completo</b>
            <p className="prompt">{bloque.bueno}</p>
            <p>{bloque.bueno_nota}</p>
          </div>
        </div>
      );
  }
}

function Final({
  curso,
  notas,
  onReiniciar,
}: {
  curso: Curso;
  notas: Record<number, number>;
  onReiniciar: () => void;
}) {
  const valores = curso.lecciones.map((l) => notas[l.id] ?? 0);
  const promedio = valores.reduce((s, n) => s + n, 0) / valores.length;
  const plantilla = curso.elementos.map((e) => `${e.nombre}: ${e.pregunta}`).join("\n");

  return (
    <div className="final">
      <p className="final__icono" aria-hidden>
        🎉
      </p>
      <h2>¡Terminaste el curso!</h2>
      <p className="parrafo">Aprobaste las {curso.lecciones.length} lecciones. Estos son tus resultados:</p>

      <table className="notas">
        <thead>
          <tr>
            <th>Lección</th>
            <th>Calificación</th>
          </tr>
        </thead>
        <tbody>
          {curso.lecciones.map((l) => (
            <tr key={l.id}>
              <td>
                {l.id}. {l.titulo}
              </td>
              <td>{(notas[l.id] ?? 0).toFixed(1)}</td>
            </tr>
          ))}
        </tbody>
        <tfoot>
          <tr>
            <td>Promedio</td>
            <td>{promedio.toFixed(1)}</td>
          </tr>
        </tfoot>
      </table>

      <p className="parrafo">Antes de tu próxima pregunta a la IA, repasa esta lista:</p>
      <pre className="prompt prompt--grande">{plantilla}</pre>
      <p className="final__aviso">{curso.aviso}</p>
      <button className="boton boton--claro" onClick={onReiniciar}>
        Volver a empezar
      </button>
    </div>
  );
}
