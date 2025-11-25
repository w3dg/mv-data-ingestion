FROM astral/uv:python3.12-bookworm-slim

WORKDIR /app

COPY .gitignore .

COPY .python-version .

COPY pyproject.toml .

COPY uv.lock .

# install packages
RUN ["uv", "sync"]

COPY . .

CMD ["uv", "run", "main.py"]
