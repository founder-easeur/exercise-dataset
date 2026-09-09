import type { Metadata } from "next";
import { Shell } from "@/components/shell";
import { themeScript } from "@/components/theme";
import "./globals.css";

export const metadata: Metadata = {
  title: "Easeur Exercise Knowledge Base",
  description:
    "Structured stretching, mobility, physiotherapy-oriented and rehabilitation exercise knowledge base with anatomy taxonomy, provenance and review workflows.",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en" suppressHydrationWarning>
      <head>
        <script dangerouslySetInnerHTML={{ __html: themeScript }} />
      </head>
      <body>
        <Shell>{children}</Shell>
      </body>
    </html>
  );
}
