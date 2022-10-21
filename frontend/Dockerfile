FROM python:3.9
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt

EXPOSE 8501
ENTRYPOINT ["streamlit", "run"]
CMD ["frontend.py"]