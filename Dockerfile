FROM python:3.7

ENV HOME=/app

RUN mkdir -p $HOME

COPY requirements.txt $HOME

WORKDIR $HOME

RUN python -m pip install --upgrade pip && \
    pip install --upgrade setuptools wheel && \
    pip install -r requirements.txt

EXPOSE 5017

COPY . $HOME

# Sobe a aplicação com log sem buffer
ENTRYPOINT ["python", "-u", "api.py"]
