FROM python:3.11.4

COPY . /xls

WORKDIR /xls

EXPOSE 8080

RUN pip3 install --no-cache-dir -r requirements.txt

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]