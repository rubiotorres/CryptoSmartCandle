FROM python
COPY ./project /app
ADD ./requirements.txt ./requirements.txt
RUN pip install -r requirements.txt

WORKDIR /app
CMD ["python", "main.py"]
