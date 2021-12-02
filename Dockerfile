FROM python:3.6
WORKDIR /tmp
RUN apt-get update -y
RUN apt-get install -y nano wget
RUN wget https://raw.githubusercontent.com/cern-it-efp/test-suite-results-dashboard/main/requirements.txt
ENV HOME="/tmp"
RUN pip install -r requirements.txt
EXPOSE 8501
EXPOSE 80
RUN mkdir /tmp/.streamlit
RUN wget https://raw.githubusercontent.com/cern-it-efp/test-suite-results-dashboard/main/.streamlit/config.toml
RUN wget https://raw.githubusercontent.com/cern-it-efp/test-suite-results-dashboard/main/.streamlit/credentials.toml
RUN mv config.toml /tmp/.streamlit/
RUN mv credentials.toml /tmp/.streamlit/
RUN pip install --upgrade streamlit
ENTRYPOINT echo 'Cloning repository...' && \
           git clone -q https://github.com/cern-it-efp/test-suite-results-dashboard.git && \
           cd test-suite-results-dashboard ; sleep infinity