FROM python:3-alpine

RUN adduser -D worker

USER worker

WORKDIR /home/worker

COPY ./src/ .

ENV PATH="/home/worker/.local/bin:${PATH}"

RUN pip install --user -r requirements.txt

COPY --chown=worker:worker . .

CMD ["python", "main.py"]
