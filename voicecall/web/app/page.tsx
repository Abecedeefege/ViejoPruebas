"use client";

import { useCallback, useEffect, useRef, useState } from "react";
import { AsYouType, parsePhoneNumberFromString } from "libphonenumber-js";

type CallState =
  | "queued"
  | "permission_requested"
  | "calling"
  | "ringing"
  | "accepted"
  | "in_call"
  | "ended"
  | "rejected"
  | "no_answer"
  | "permission_denied"
  | "failed";

interface CallInfo {
  ref: string;
  state: CallState;
  error?: string | null;
}

const LABELS: Record<CallState, { text: string; live: boolean }> = {
  queued: { text: "Preparando la llamada…", live: true },
  permission_requested: {
    text: "Te mandé un pedido de permiso por WhatsApp. Aceptalo y te llamo 📲",
    live: true,
  },
  calling: { text: "Llamando a tu WhatsApp…", live: true },
  ringing: { text: "Sonando… atendé 📞", live: true },
  accepted: { text: "Atendiste, conectando el audio…", live: true },
  in_call: { text: "En llamada — charlá tranquilo 🎙️", live: true },
  ended: { text: "Llamada terminada. ¿Otra ronda?", live: false },
  rejected: { text: "Rechazaste la llamada.", live: false },
  no_answer: { text: "No atendiste. Probá de nuevo cuando quieras.", live: false },
  permission_denied: { text: "Rechazaste el permiso de llamada en WhatsApp.", live: false },
  failed: { text: "Falló la llamada.", live: false },
};

const TERMINAL: CallState[] = ["ended", "rejected", "no_answer", "permission_denied", "failed"];

export default function Home() {
  const [raw, setRaw] = useState("");
  const [busy, setBusy] = useState(false);
  const [call, setCall] = useState<CallInfo | null>(null);
  const [error, setError] = useState<string | null>(null);
  const pollRef = useRef<ReturnType<typeof setInterval> | null>(null);

  const parsed = parsePhoneNumberFromString(raw, "AR");
  const valid = Boolean(parsed?.isValid());

  const stopPolling = useCallback(() => {
    if (pollRef.current) {
      clearInterval(pollRef.current);
      pollRef.current = null;
    }
  }, []);

  useEffect(() => stopPolling, [stopPolling]);

  const poll = useCallback(
    (ref: string) => {
      stopPolling();
      pollRef.current = setInterval(async () => {
        try {
          const res = await fetch(`/api/call?ref=${encodeURIComponent(ref)}`);
          if (!res.ok) return;
          const data: CallInfo = await res.json();
          setCall(data);
          if (TERMINAL.includes(data.state)) stopPolling();
        } catch {
          /* reintenta en el próximo tick */
        }
      }, 2000);
    },
    [stopPolling]
  );

  async function llamame() {
    if (!parsed || busy) return;
    setBusy(true);
    setError(null);
    setCall(null);
    try {
      const res = await fetch("/api/call", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ to: parsed.number }),
      });
      const data = await res.json();
      if (!res.ok) {
        setError(data?.detail ?? `Error ${res.status}`);
        return;
      }
      setCall(data);
      poll(data.ref);
    } catch (e) {
      setError("No pude hablar con el backend. ¿Está corriendo el agente?");
    } finally {
      setBusy(false);
    }
  }

  const label = call ? LABELS[call.state] ?? { text: call.state, live: false } : null;

  return (
    <main className="card">
      <h1>📞 Llamame</h1>
      <p className="subtitle">
        Escribí tu número y un agente de voz te llama por <strong>WhatsApp</strong> para
        pelotear una idea. Impulsado por OpenAI Realtime.
      </p>

      <label htmlFor="tel">Tu número de WhatsApp</label>
      <input
        id="tel"
        type="tel"
        placeholder="+54 9 11 5555-0000"
        value={raw}
        onChange={(e) => setRaw(new AsYouType("AR").input(e.target.value))}
        onKeyDown={(e) => e.key === "Enter" && valid && llamame()}
        autoComplete="tel"
      />

      <button onClick={llamame} disabled={!valid || busy}>
        {busy ? "Iniciando…" : "Llamame por WhatsApp"}
      </button>

      {error && (
        <div className="status error">
          <strong>Ups</strong>
          {error}
        </div>
      )}

      {call && label && (
        <div className="status">
          <strong>
            {label.live && <span className="pulse" />} Estado
          </strong>
          {label.text}
          {call.state === "failed" && call.error ? ` (${call.error})` : null}
        </div>
      )}

      <p className="hint">
        La primera vez WhatsApp te pide autorizar que el agente te llame (permiso válido por 7
        días). Solo se puede llamar a los números habilitados en el servidor.
      </p>
    </main>
  );
}
