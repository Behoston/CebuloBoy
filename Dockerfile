FROM python:3.7-alpine
WORKDIR /code
ENV PYTHONPATH ${PYTHONPATH}:/code
RUN apk --update add --no-cache --virtual build-dependencies \
    linux-headers \
    gcc \
    musl-dev \
    make \
    libxml2 \
    g++ \
    libxml2-dev \
    libxslt-dev \
    && pip install --upgrade pip
COPY requirements.txt /code/requirements.txt
RUN pip install -r requirements.txt
COPY . /code
CMD python models.py && python app.py
