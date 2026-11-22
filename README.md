# Heuser College — CRP Programming & Problem Solving Showcase

Repository for the Heuser College Career Readiness Program (CRP) student project showcase portals.

## Structure

- `Heuser27/` — 2026–27 cohort Go showcase server (`heuser27.basilsaeedbari.com`)
- `Heuser28/` — Placeholder for next year's batch

## Features (`Heuser27`)

- **Friv-style Student Arcade Wall (`/`)**: Interactive mosaic of all students with search, homework filters, batch filters, and Instructor Starred Spotlight pinned to the top.
- **Playable Games & Code Viewer (`/student/{id}`)**:
  - Embedded **MakeCode Arcade** viewport for HW1 & HW2
  - In-browser **Python source code viewer** for HW4
  - **Context & Prompt Engineering** deliverables viewer for HW5
  - **Live sandboxed HW6 web games** (Catch Game, Virtual Pet, Pattern Memory) served directly from student `.zip` submissions
  - Links & live preview support for HW7 (GitHub Pages), HW8 (Unconventional Portfolio), and HW9 (Backend Web Apps)
- **IP-Based Voting & Comments**: No login required — 1 vote per IP per project/game, plus visitor comments.
- **Instructor Admin Panel (`/admin`)**:
  - Student × Homework submission matrix (`N / M` completion tracking) & CSV export
  - One-click **Star Student** toggle with optional spotlight note
  - **Upload `.xlsx`** form or **Rescan Disk** to ingest future homework submissions without losing stars, votes, or comments

## Portainer Deployment (`heuser27.basilsaeedbari.com`)

Pushes to `main` automatically build and push `ghcr.io/basilsaeedbari/heuser27:main` via GitHub Actions (`.github/workflows/docker-heuser27.yml`).

Use `Heuser27/docker-compose.yml` in Portainer:

```yaml
version: '3.8'

services:
  heuser27:
    image: ghcr.io/basilsaeedbari/heuser27:main
    container_name: heuser27_web
    restart: unless-stopped
    environment:
      - TZ=Asia/Karachi
      - PORT=8090
      - ADMIN_PASSWORD=heuser27admin
    volumes:
      - heuser27_data:/app/data
    networks:
      - proxy-net
    labels:
      caddy: heuser27.basilsaeedbari.com
      caddy.reverse_proxy: "{{upstreams 8090}}"

networks:
  proxy-net:
    external: true

volumes:
  heuser27_data:
    name: heuser27_data
```

> **Note:** Change `ADMIN_PASSWORD` (and optionally set `SESSION_SECRET`) in Portainer before deploying publicly.
