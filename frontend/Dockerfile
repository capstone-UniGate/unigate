FROM node:23.4-bookworm-slim

WORKDIR /app

# ref: https://pnpm.io/docker
ENV PNPM_HOME=/pnpm

ENV PATH="$PNPM_HOME:$PATH"

RUN corepack enable

COPY ./ /app/

RUN --mount=type=cache,id=pnpm,target=/pnpm/store pnpm install --frozen-lockfile

CMD ["pnpm", "run", "dev"]
