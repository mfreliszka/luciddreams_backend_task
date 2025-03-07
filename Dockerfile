# docker image with poetry 1.8.5 and python 3.11.11 preinstalled
FROM pfeiffermax/python-poetry:1.14.0-poetry1.8.5-python3.11.11-slim-bookworm

# Set the working directory inside the container
WORKDIR /src

# Copy the required files into the container
COPY poetry.lock pyproject.toml /src/

# Install dependencies
RUN poetry config virtualenvs.create false
RUN poetry install

COPY . /src/

# Expose the application port (FastAPI runs on 8000)
EXPOSE 8000

# Start FastAPI with Uvicorn
CMD ["uvicorn", "--host", "0.0.0.0", "--port", "8000", "app.main:app", "--reload"]
