FROM python:3.6
WORKDIR /tmp
RUN git clone https://github.com/cern-it-efp/test-suite-results-dashboard.git
WORKDIR /tmp/test-suite-results-dashboard
RUN pip install pystrich
RUN pip install -r requirements.txt
RUN apt-get update -y
RUN apt-get install -y nano
EXPOSE 8501
EXPOSE 80
CMD [ "sleep", "infinity" ]