FROM svizor/zoomcamp-model:mlops-3.10.0-slim

RUN pip install -U pip
RUN pip install pipenv

WORKDIR /app

COPY [ "Pipfile", "Pipfile.lock", "./"]

RUN pipenv install --system --deploy

RUN mkdir outputs

COPY [ "starter.py", "./" ]

ENTRYPOINT [ "python", "starter.py", "2022", "4" ]