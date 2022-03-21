FROM python:3.6-slim

ENV HOME=/app

RUN mkdir -p $HOME

COPY requirements.txt $HOME

WORKDIR $HOME

RUN python -m pip install --upgrade pip && \
    pip install --upgrade setuptools wheel && \
    pip install -r requirements.txt

EXPOSE 5017

COPY . $HOME

# Entrypoint
CMD ["gunicorn", "--log-level", "warning", "--capture-output", "--enable-stdio-inheritance", "--workers", "4", "--bind", "0.0.0.0:5017", "api:app"]
