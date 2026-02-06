# syntax=docker/dockerfile:1
FROM node:20-alpine AS build

WORKDIR /app

COPY package.json package-lock.json* ./
RUN npm install

COPY . .
RUN npm run build

FROM node:20-alpine

WORKDIR /app
ENV NODE_ENV=production

COPY --from=build /app/package.json /app/package-lock.json* ./
RUN npm install --omit=dev

COPY --from=build /app/.svelte-kit /app/.svelte-kit
COPY --from=build /app/build /app/build
COPY --from=build /app/vite.config.js /app/vite.config.js
COPY --from=build /app/svelte.config.js /app/svelte.config.js

EXPOSE 4173

CMD ["npm", "run", "preview", "--", "--host", "0.0.0.0", "--port", "4173"]
