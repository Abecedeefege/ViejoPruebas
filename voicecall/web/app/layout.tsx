import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Llamame — sparring de ideas por WhatsApp",
  description:
    "Escribí tu número y un agente de voz (OpenAI Realtime) te llama por WhatsApp para pelotear ideas.",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="es">
      <body>{children}</body>
    </html>
  );
}
