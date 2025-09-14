# services/frontend/Dockerfile

# 1. Build Stage: Install dependencies and build the app
FROM node:20-alpine AS builder
WORKDIR /app
COPY package.json pnpm-lock.yaml ./
RUN npm install -g pnpm && pnpm install
COPY . .
RUN pnpm run build

# 2. Production Stage: Copy only the necessary built files
FROM node:20-alpine AS runner
WORKDIR /app

# The Next.js build output now includes a standalone server, which is perfect for containers.
COPY --from=builder /app/public ./public
COPY --from=builder /app/.next/standalone ./
COPY --from=builder /app/.next/static ./.next/static

EXPOSE 3000
ENV PORT 3000

# Command to run the optimized Next.js server
CMD ["node", "server.js"]