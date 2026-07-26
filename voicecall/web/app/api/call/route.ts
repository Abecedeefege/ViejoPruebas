// Proxy autenticado hacia el backend de voz (voicecall/agent).
// El token vive solo en el server de Next: el browser nunca lo ve.

export const dynamic = "force-dynamic";

const AGENT_URL = process.env.AGENT_URL ?? "http://localhost:8000";
const AGENT_API_TOKEN = process.env.AGENT_API_TOKEN ?? "";

const authHeaders = {
  Authorization: `Bearer ${AGENT_API_TOKEN}`,
  "Content-Type": "application/json",
};

export async function POST(request: Request) {
  const body = await request.json().catch(() => ({}));
  const res = await fetch(`${AGENT_URL}/calls`, {
    method: "POST",
    headers: authHeaders,
    body: JSON.stringify({ to: body?.to ?? "" }),
    cache: "no-store",
  });
  return Response.json(await res.json().catch(() => ({})), { status: res.status });
}

export async function GET(request: Request) {
  const ref = new URL(request.url).searchParams.get("ref");
  if (!ref) {
    return Response.json({ detail: "falta ref" }, { status: 400 });
  }
  const res = await fetch(`${AGENT_URL}/calls/${encodeURIComponent(ref)}`, {
    headers: authHeaders,
    cache: "no-store",
  });
  return Response.json(await res.json().catch(() => ({})), { status: res.status });
}
