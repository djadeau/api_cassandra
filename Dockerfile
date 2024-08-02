ARG py_version=3.12.4
ARG wolfi_version=latest

FROM chainguard/wolfi-base:${wolfi_version} AS python_base

ARG py_version

RUN apk add --no-cache --no-check-certificate python3~${py_version} tzdata


FROM python_base AS builder

ARG py_version

ENV LANG=C.UTF-8 LC_ALL=C.UTF-8 PYTHONUNBUFFERED=1

RUN apk add --no-cache --no-check-certificate python3-dev~${py_version} gcc glibc-dev uv

ENV VIRTUAL_ENV=/opt/venv PATH="/opt/venv/bin:$PATH"

COPY requirements.txt .

RUN uv venv /opt/venv && uv pip install --compile --no-cache -r requirements.txt


FROM python_base

ENV LANG=C.UTF-8 LC_ALL=C.UTF-8 PYTHONUNBUFFERED=1 

COPY --from=builder /opt/venv /opt/venv

WORKDIR /app

COPY ./app /app/app
COPY ./scripts /app/scripts

RUN find /app/scripts -type f -iname "*.sh" -exec chmod a+x {} +
RUN python -m compileall
RUN mkdir -p /var/log/api && chown -R nonroot:0 /var/log/api && chmod -R g+w /var/log/api

USER nonroot

ENV PATH=/opt/venv/bin:$PATH LANG=C.UTF-8 LC_ALL=C.UTF-8 PYTHONUNBUFFERED=1 PYTHONPATH=/app:/opt/venv TZ=UTC

CMD ["./scripts/run.sh"]