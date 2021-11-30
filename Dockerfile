FROM python:3.6
ADD my_script.py /
RUN pip install pystrich
RUN pip install -r requirements.txt
EXPOSE 8501
CMD [ "python", "./dataset_gen.py" ]