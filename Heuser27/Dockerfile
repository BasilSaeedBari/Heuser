# syntax=docker/dockerfile:1

FROM golang:alpine AS builder
WORKDIR /src

COPY go.mod go.sum ./
RUN go mod download

COPY main.go ./
COPY internal/ ./internal/
COPY web/ ./web/

RUN CGO_ENABLED=0 GOOS=linux go build -ldflags="-s -w" -o /out/heuser27 .

FROM alpine:3.21
RUN apk add --no-cache ca-certificates tzdata

WORKDIR /app
COPY . /app/
RUN rm -rf /app/internal /app/web /app/main.go /app/go.mod /app/go.sum /app/Dockerfile /app/docker-compose.yml /app/.dockerignore \
 && mkdir -p /app/data/uploads /app/data/hw6_games
COPY --from=builder /out/heuser27 /app/heuser27

ENV PORT=8090 \
    BASE_DIR=/app \
    DATA_DIR=/app/data \
    TZ=Asia/Karachi

EXPOSE 8090
VOLUME ["/app/data"]

CMD ["/app/heuser27"]
