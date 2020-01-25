FROM python:3.8.1

COPY . .
RUN pip install -r requirements.txt
ENV SLEEP 1200

CMD ["python", "bot.py"]
