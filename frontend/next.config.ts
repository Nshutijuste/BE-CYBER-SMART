import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  /* config options here */
  allowedDevOrigins: [
    "192.168.8.111",
    "192.168.8.111:3000",
    "10.10.1.137",
    "10.10.1.137:3000",
    "localhost",
    "localhost:3000",
    "127.0.0.1",
    "127.0.0.1:3000",
  ],
  experimental: {
    agentFeedback: true,
    // eslint-disable-next-line @typescript-eslint/ban-ts-comment
    // @ts-ignore
    agentUpgrade: "security",
  },
  async rewrites() {
    const api = process.env.API_ORIGIN ?? "http://127.0.0.1:8001";
    return [{ source: "/api/:path*", destination: `${api}/api/:path*` }];
  },
  turbopack: {
    rules: {
      "*.css": {
        loaders: ["@tailwindcss/turbopack"],
        as: "*.css",
      },
    },
  },
};

export default nextConfig;