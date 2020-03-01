FROM python:3.8.2

RUN rm -rfv develop-eggs dist downloads eggs env parts .cache .scannerwork &&\
    rm -fv .DS_Store .coverage .installed.cfg bootstrap.py .coverage &&\
    find . -name '*.pyc' -exec rm -fv {} \; &&\
    find . -name '*.pyo' -exec rm -fv {} \; &&\
    find . -depth -name '*.egg-info' -exec rm -rfv {} \; &&\
    find . -depth -name '__pycache__' -exec rm -rfv {} \;

COPY ./requirements.txt ./requirements.txt
RUN pip3 install --upgrade pip &&\
    pip3 install wheel &&\
    pip3 install -r requirements.txt &&\
    python3 -m spacy download en_core_web_sm &&\
    python3 -m spacy download nb_core_news_sm

COPY ./src /app
WORKDIR /app

EXPOSE 8085

CMD python ./index.py
