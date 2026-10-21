FROM python:3.12-slim AS common

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1
WORKDIR /app

COPY pyproject.toml README.md ./
COPY src ./src
COPY tests ./tests
COPY evaluation ./evaluation
COPY solutions ./solutions
RUN python -m pip install --no-cache-dir -e '.[test]'

FROM common AS baseline
CMD ["pytest", "-q", "tests"]

FROM common AS fixed
COPY solutions/backoff.py /app/src/retrykit/backoff.py
CMD ["pytest", "-q", "tests", "evaluation"]
