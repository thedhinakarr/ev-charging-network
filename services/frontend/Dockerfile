# services/frontend/Dockerfile

# 1. Build Stage
FROM node:20-alpine AS builder
WORKDIR /app
COPY package.json pnpm-lock.yaml ./
RUN npm install -g pnpm && pnpm install
COPY . .
RUN pnpm run build

# 2. Production Stage
FROM node:20-alpine AS runner
WORKDIR /app

COPY --from=builder /app/public ./public
COPY --from=builder /app/.next/standalone ./
COPY --from=builder /app/.next/static ./.next/static

EXPOSE 3000
ENV PORT 3000
# --- ADD THIS LINE ---
# Tell the Next.js server to listen on all network interfaces
ENV HOSTNAME 0.0.0.0

# Command to run the optimized Next.js server
CMD ["node", "server.js"]