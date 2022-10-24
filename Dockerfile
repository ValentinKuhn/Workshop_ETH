FROM jupyter/minimal-notebook
COPY frontend/requirements.txt .
RUN pip install -r requirements.txt

EXPOSE 8888

ENV JUPYTER_ENABLE_LAB="yes"

ENTRYPOINT ["start-notebook.sh"]
CMD ["--NotebookApp.token=''", "--NotebookApp.password=''"]