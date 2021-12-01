FROM python:3.6
WORKDIR /tmp
RUN apt-get update -y
RUN apt-get install -y nano wget
RUN wget https://raw.githubusercontent.com/cern-it-efp/test-suite-results-dashboard/main/requirements.txt
RUN pip install -r requirements.txt
EXPOSE 8501
EXPOSE 80
ENTRYPOINT echo 'Cloning repository...' && \
           git clone -q https://github.com/cern-it-efp/test-suite-results-dashboard.git && \
           cd test-suite-results-dashboard ; sleep infinity
