ARG PYTHON_IMAGE_NAME
FROM python:${PYTHON_IMAGE_NAME}

WORKDIR /app

RUN pip install --upgrade pip

### Installing pytest on the image as it's not required for the package ###
COPY setup.py README.md pyproject.toml publish.py ./

RUN pip install -e .[dev]

COPY ./ ./

