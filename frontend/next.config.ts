import type { NextConfig } from "next";

const backend = process.env.BACKEND_URL || "http://127.0.0.1:8000";

const nextConfig: NextConfig = {
  // Arena/e2b preview proxies the dev server under a different origin.
  allowedDevOrigins: ["*.e2b.app"],
  async rewrites() {
    // Frontend calls relative /api/... and /static/... — the dev server
    // proxies both to FastAPI (API data + project-owned illustrations).
    return [
      {
        source: "/api/:path*",
        destination: `${backend}/api/:path*`,
      },
      {
        source: "/static/:path*",
        destination: `${backend}/static/:path*`,
      },
    ];
  },
};

export default nextConfig;
