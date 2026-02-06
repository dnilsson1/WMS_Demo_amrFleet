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
ENV PORT=4173

COPY --from=build /app/package.json /app/package-lock.json* ./
RUN npm install --omit=dev

COPY --from=build /app/build /app/build

EXPOSE 4173

CMD ["node", "build"]
