FROM python:3.6
RUN git clone https://github.com/cern-it-efp/test-suite-results-dashboard.git
COPY ../creds.yaml .
RUN pip install pystrich
RUN pip install -r requirements.txt
EXPOSE 8501
EXPOSE 80
CMD [ "python", "./dataset_gen.py" ]