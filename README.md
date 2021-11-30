# EOSC-TestSuite Dashboard
The following repository contains source code used in order to create a heroku app for visualizing the results of several workloads across different providers using the [EOSC TestSuite](https://github.com/cern-it-efp/EOSC-Testsuite).
The TestSuite Dashboard pulls the latest results from the S3 container where the json results from each successful run are uploaded and updates the workload performance across different providers based on the latest run.
We have tested the following providers across High Energy Physics Benchmark, PerfSONAR, Data Repatriation and DODAS.
- City Network
- Layershift
- Google Cloud Platform
- IBM Cloud
- Exoscale
- Ionoscloud
- Cloudsigma
- Cloudferro
- OVH
- X-ion

The Dashboard will include results from a few other providers over the coming time.

To launch the dashboard locally:
- `pip install -r requirements.txt`
- `python dataset_pre.py`

To launch the dashboard on heroku:
- `sudo snap install heroku --classic`
- `heroku login`
- Using your heroku credentials log into Heroku CLI
- `git clone https://github.com/cern-it-efp/test-suite-results-dashboard`
- `cd test-suite-results-dashboard`
- `heroku create`
- `git push heroku main`
