FROM python:3.12-slim AS builder
WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt --target=/app/dependencies

FROM python:3.12-slim
WORKDIR /app
COPY --from=builder /app/dependencies /app/dependencies
COPY ./app.py ./
COPY ./static ./
COPY ./templates ./
COPY . .
ENV PYTHONPATH=/app/dependencies
ENV PATH="/app/dependencies/bin:$PATH"
EXPOSE 8000
ENTRYPOINT ["gunicorn"]
CMD ["--bind","0.0.0.0:8000","app:app"]

