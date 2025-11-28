FROM python:3.12.12-alpine3.22

WORKDIR /app

RUN apk add --no-cache git
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN apk add --no-cache libzbar

CMD [ "python", "./main.py" ]
