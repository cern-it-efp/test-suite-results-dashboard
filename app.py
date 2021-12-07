import streamlit as st
import PIL
from PIL import Image
import pandas as pd
import io
import os
from datetime import datetime
import plotly.express as px
from st_aggrid import AgGrid
from bokeh.models.widgets import Div

pd.set_option('display.max_columns', None)
#Logo image is not used
image = Image.open('logo_diff.png')
st.set_page_config(page_title='EOSC Testsuite Results Dashboard',page_icon=image,layout='wide',initial_sidebar_state='auto')
#st.write('<style>body { margin: 0; font-family: Arial, Helvetica, sans-serif;} .header{padding: 40px 50%; background: #264899; color: #f1f1f1; position:;top:100;} .header img {float: left; width:100px;height:100px;} .sticky { position: fixed; top: 0; width: 100%;} </style><div class="header" id="myHeader"></div>', unsafe_allow_html=True)

#os.system('python dataset_gen.py')
# simple description
# display media
#st.image(image, caption='source: https://pixabay.com/photos/mario-luigi-yoschi-figures-funny-1557240/',
#           use_column_width=True)
#col1, col2 = st.beta_columns(2)
st.image(image)
#col1.image(image,width = 335)#use_column_width=True

#col2.title('EOSC Testsuite Results Dashboard')

m = st.markdown("""
<style>
div.stButton > button:first-child {
    background-color: #ffc107;
    color:#000000;
}
div.stButton > button:hover {
    background-color: #ffc107;
    color:#000000;
    }
body {
    background-color: lightgoldenrodyellow;
}
div[role="listbox"] ul {
    background-color: #264899;
}
div[data-baseweb="select"] > div {
    background-color: #3b5aa3;
}
</style>""", unsafe_allow_html=True)


#b = st.button("Link to Repository")
st.write('The EOSC Test Suite, developed by [CERN](https://home.cern/),, is intended to be used to test and validate commercial cloud services for research and education workloads. It is being actively used as a validation tool for commercial cloud services procured via European Commission sponsored projects such as [OCRE](https://ocre-project.eu/), [ARCHIVER](https://archiver-project.eu/) and [CloudBank EU](https://ngiatlantic.eu/funded-experiments/cloudbank-eu-ngi)')
st.write('To learn more about EOSC please visit the [EOSC Association website](https://eosc.eu/) for more information.')
if st.button('EOSC Test Suite Repository'):
    js = "window.open('https://github.com/cern-it-efp/EOSC-Testsuite')"  # New tab or window
    js = "window.location.href = 'https://github.com/cern-it-efp/EOSC-Testsuite'"  # Current tab
    html = '<img src onerror="{}">'.format(js)
    div = Div(text=html)
    st.bokeh_chart(div)
#st.write('Please find the the repository [here](https://github.com/cern-it-efp/EOSC-Testsuite).')
st.write('In this webpage we provide results from different runs for several tests run by EOSC test suite across different providers.')
#st.header('Exploratory Data Analysis')
# markdown similar to github md and also has support for some cool graphics
# in form of emojis full list here: https://raw.githubusercontent.com/omnidan/node-emoji/master/lib/emoji.json

df_cpu_bmk = pd.read_csv('/tmp/summary_cpu_bench.csv', names = ['Provider','Flavor','Location','Run Date','Score','Score Per Core','CPU Model','Start Date and Time','End Date and Time'])
df_perfsonar = pd.read_csv('/tmp/summary_perfsonar.csv', names = ['Provider','Flavor','Location','Run Date','Max Latency (ms)','Min Latency (ms)','Mean Latency (ms)','Bandwidth From CERN To Provider (Gbps)','Bandwidth From Provider To CERN (Gbps)'])
df_dodas = pd.read_csv('/tmp/summary_dodas.csv', names=['Provider','Flavor','Location','Run Date','Result'])
df_data_repatriation = pd.read_csv('/tmp/summary_data_repatriation.csv', names=['Provider','Flavor','Location','Run Date','Result'])
df_progan = pd.read_csv('/tmp/summary_progan.csv',names = ['Provider','Flavor','Location','Run Date','Images Amount','Kimg','GPU Type','GPU per Nodes','Time (Minutes)'])
df_cpd = pd.read_csv('/tmp/cpd.csv')

df_cpu_bmk['Provider'] = df_cpu_bmk['Provider'].replace({'google':'google cloud platform'})
df_cpu_bmk['Provider'] = df_cpu_bmk['Provider'].replace({'flexibleengine':'orange'})
df_perfsonar['Provider'] = df_perfsonar['Provider'].replace({'google':'google cloud platform'})
df_perfsonar['Provider'] = df_perfsonar['Provider'].replace({'flexibleengine':'orange'})
df_dodas['Provider'] = df_dodas['Provider'].replace({'google':'google cloud platform'})
df_dodas['Provider'] = df_dodas['Provider'].replace({'flexibleengine':'orange'})
df_data_repatriation['Provider'] = df_data_repatriation['Provider'].replace({'google':'google cloud platform'})
df_data_repatriation['Provider'] = df_data_repatriation['Provider'].replace({'flexibleengine':'orange'})
df_progan['Provider'] = df_progan['Provider'].replace({'google':'google cloud platform'})
df_progan['Provider'] = df_progan['Provider'].replace({'flexibleengine':'orange'})
df_cpd['Vendor'] = df_cpd['Vendor'].replace({'google':'google cloud platform'})
df_cpd['Vendor'] = df_cpd['Vendor'].replace({'flexibleengine':'orange'})

df_perfsonar['Max Latency (ms)'] = 1000*df_perfsonar['Max Latency (ms)']
df_perfsonar['Min Latency (ms)'] = 1000*df_perfsonar['Min Latency (ms)']
df_perfsonar['Mean Latency (ms)'] = 1000*df_perfsonar['Mean Latency (ms)']
df_progan['Time (Minutes)'] = df_progan['Time (Minutes)']/60

df_cpu_bmk = df_cpu_bmk.sort_values(by=['Run Date'],ascending = False)
df_perfsonar = df_perfsonar.sort_values(by=['Run Date'],ascending = False)
df_dodas = df_dodas.sort_values(by=['Run Date'],ascending = False)
df_data_repatriation = df_data_repatriation.sort_values(by=['Run Date'],ascending = False)
df_progan = df_progan.sort_values(by=['Run Date'],ascending = False)

df_data_repatriation.loc[-1] = ['',0,0,0,0]
df_data_repatriation.index = df_data_repatriation.index+1
df_data_repatriation.sort_index(inplace=True)

# drop down for unique value from a column
provider_name = st.selectbox('Select a Provider from the dropdown below', options=df_data_repatriation.Provider.unique())
if (provider_name!=''):
    df_cpu_bmk = df_cpu_bmk[df_cpu_bmk.Provider !='']
    df_cpu_bmk = df_cpu_bmk.loc[df_cpu_bmk.Provider == provider_name]

    df_cpu_bmk = df_cpu_bmk.drop_duplicates(subset=['Location'], keep='first')
    df_perfsonar = df_perfsonar.loc[df_perfsonar.Provider == provider_name]
    df_perfsonar = df_perfsonar.drop_duplicates(subset=['Location'], keep='first')

    df_dodas = df_dodas.loc[df_dodas.Provider == provider_name]
    df_dodas = df_dodas.drop_duplicates(subset=['Location'], keep='first')

    df_data_repatriation = df_data_repatriation.loc[df_data_repatriation.Provider == provider_name]
    df_data_repatriation = df_data_repatriation.drop_duplicates(subset=['Location'], keep='first')

    df_progan = df_progan.loc[df_progan.Provider == provider_name]
    df_progan = df_progan.drop_duplicates(subset=['Location'], keep='first')
    
    df_cpd = df_cpd.loc[df_cpd.Vendor == provider_name]
    df_perf_rtt = df_perfsonar[['Provider','Flavor','Location','Run Date','Max Latency (ms)','Min Latency (ms)','Mean Latency (ms)']]
    df_perf_bwt = df_perfsonar[['Provider','Flavor','Location','Run Date','Bandwidth From CERN To Provider (Gbps)','Bandwidth From Provider To CERN (Gbps)']]

    #amazon = 'logos/aws.png'
    #azure = 'logos/azure.png'
    #cloudferro = 'logos/cloudferro.png'
    #cloudsigma = 'logos/cloudsigma.png'
    #exoscale = 'logos/exoscale.jpg'
    #google = 'logos/gcp.png'
    #ibm = 'logos/ibm.png'
    #ionoscloud = 'logos/ionos.png'
    #oracle = 'logos/oracle.png'
    #ovh = 'logos/ovh.png'
    #tsystems = 'logos/tsystems.png'
    #xion = 'logos/xion.png'

    logo_image = Image.open('logos/'+str(provider_name)+'.png')
    #logo_image = logo_image.resize((900,400),Image.ANTIALIAS)
    st.image(logo_image,width = 300)
    st.header('Cloud Platform Details')     
    AgGrid(df_cpd, height = 75, fit_columns_on_grid_load=False)
    #st.markdown("""<hr style="height:5px;border:none;color:#ffc107;background-color:#ffc107;" /> """, unsafe_allow_html=True)

    #st.dataframe(df_cpd)
    if (str(provider_name)=="ovh") or (str(provider_name)=="x-ion") or (str(provider_name)=="exoscale") or (str(provider_name)=="orange") or (str(provider_name)=="google cloud platform") or (str(provider_name)=="ionoscloud"):
        st.markdown("""<hr style="height:2px;border:none;color:#ffc107;background-color:#ffc107;" /> """, unsafe_allow_html=True)
        st.header('Cloud Object Storage Benchmark (COSBench)')
        st.write('Benchmarking of Object Storage services based on [COSBench](https://github.com/intel-cloud/cosbench). Each table below shows multiple measurements of metrics such as operation and byte count, average response time, average processing time, throughput, bandwidth and success ratio taken at different moments while performing writing and reading operations. The source of the writing and reading operations is a virtual machine running on the CERN cloud (in Geneva, Switzerland).')
        if st.button('More Information', key = 6):
            js = "window.open('https://eosc-testsuite.readthedocs.io/en/latest/testsCatalog.html#cloud-object-storage-benchmark-cosbench')"  # New tab or window
            js = "window.location.href = 'https://eosc-testsuite.readthedocs.io/en/latest/testsCatalog.html#cloud-object-storage-benchmark-cosbench'"  # Current tab
            html = '<img src onerror="{}">'.format(js)
            div = Div(text=html)
            st.bokeh_chart(div)
            
        if (str(provider_name)=="ovh"):
            df_cost_1 = pd.read_csv('/tmp/ovh.03-12-2021.de.csv')
            df_cost_2 = pd.read_csv('/tmp/ovh.03-12-2021.sbg.csv')
            df_cost_3 = pd.read_csv('/tmp/ovh.03-12-2021.uk.csv')
            df_cost_4 = pd.read_csv('/tmp/ovh.03-12-2021.waw.csv')
            st.subheader('Region: de')
            st.write('Run Date: 03-12-2021')
            AgGrid(df_cost_1, height = 250, fit_columns_on_grid_load=False)
            st.subheader('Region: sbg')
            st.write('Run Date: 03-12-2021')
            AgGrid(df_cost_2, height = 250, fit_columns_on_grid_load=False)
            st.subheader('Region: uk')
            st.write('Run Date: 03-12-2021')
            AgGrid(df_cost_3, height = 250, fit_columns_on_grid_load=False)
            st.subheader('Region: waw')
            st.write('Run Date: 03-12-2021')
            AgGrid(df_cost_4, height = 250, fit_columns_on_grid_load=False)
            
        if (str(provider_name)=="x-ion"):
            df_cost_1 = pd.read_csv('/tmp/xion.06-12-2021.hamburg.csv')
            st.subheader('Region: hamburg')
            st.write('Run Date: 06-12-2021')
            AgGrid(df_cost_1, height = 250, fit_columns_on_grid_load=False)

        if (str(provider_name)=="google cloud platform"):
            df_cost_1 = pd.read_csv('/tmp/google.03-12-2021.default.csv')
            st.subheader('Region: default')
            st.write('Run Date: 03-12-2021')
            AgGrid(df_cost_1, height = 250, fit_columns_on_grid_load=False)

        if (str(provider_name)=="exoscale"):
            df_cost_1 = pd.read_csv('/tmp/exoscale.03-12-2021.at-vie-1.csv')
            df_cost_2 = pd.read_csv('/tmp/exoscale.03-12-2021.ch-gva-2.csv')
            df_cost_3 = pd.read_csv('/tmp/exoscale.03-12-2021.de-fra-1.csv')
            st.subheader('Region: at-vie-1')
            st.write('Run Date: 03-12-2021')
            AgGrid(df_cost_1, height = 250, fit_columns_on_grid_load=False)
            st.subheader('Region: ch-gva-2')
            st.write('Run Date: 03-12-2021')
            AgGrid(df_cost_2, height = 250, fit_columns_on_grid_load=False)
            st.subheader('Region: de-fra-1')
            st.write('Run Date: 03-12-2021')
            AgGrid(df_cost_3, height = 250, fit_columns_on_grid_load=False)

        if (str(provider_name)=="orange"):
            df_cost_1 = pd.read_csv('/tmp/flexibleengine.03-12-2021.eu-west-0.csv')
            st.subheader('Region: eu-west-0')
            st.write('Run Date: 03-12-2021')
            AgGrid(df_cost_1, height = 250, fit_columns_on_grid_load=False)

        if (str(provider_name)=="ionoscloud"):
            df_cost_1 = pd.read_csv('/tmp/ionoscloud.03-12-2021.de-fra.csv')
            st.subheader('Region: de-fra')
            st.write('Run Date: 03-12-2021')
            AgGrid(df_cost_1, height = 250, fit_columns_on_grid_load=False)
        st.markdown("""<hr style="height:2px;border:none;color:#ffc107;background-color:#ffc107;" /> """, unsafe_allow_html=True)

    st.header('Dynamic On Demand Analysis Services test (DODAS) Test Results')
    st.write('DODAS is a system designed to provide a high level of automation in terms of provisioning, creating, managing and accessing a pool of heterogeneous computing and storage resources, by generating clusters on demand for the execution of HTCondor workload management system. DODAS allows to seamlessly join the HTCondor Global Pool of CMS to enable the dynamic extension of existing computing resources. A benefit of such an architecture is that it provides high scaling capabilities and self-healing support that results in a drastic reduction of time and cost, through setup and operational efficiency increases.')
    #st.write('If one wants to deploy this test, the machines in the general cluster (to which such test is deployed), should have rather large disks as the image for this test is 16GB. To set the disk size use the storageCapacity variable from configs.yaml.')
    if st.button('More Information', key = 1):
        js = "window.open('https://eosc-testsuite.readthedocs.io/en/latest/testsCatalog.html#dodas-dynamic-on-demand-analysis-services-test')"  # New tab or window
        js = "window.location.href = 'https://eosc-testsuite.readthedocs.io/en/latest/testsCatalog.html#dodas-dynamic-on-demand-analysis-services-test'"  # Current tab
        html = '<img src onerror="{}">'.format(js)
        div = Div(text=html)
        st.bokeh_chart(div)
    #st.write('[Repository](https://dodas-ts.github.io/dodas-doc/)')
    AgGrid(df_dodas, height = 150, fit_columns_on_grid_load=False)
    st.markdown("""<hr style="height:2px;border:none;color:#ffc107;background-color:#ffc107;" /> """, unsafe_allow_html=True)

    st.header('Data Repatriation Test Results')
    st.write('When using cloud credits, when the credit is exhausted, data can be repatriated or moved to a long-term data storage service. The example used in this test uses Zenodo service maintained by CERN, verifying that the output data can be taken from the cloud provider to Zenodo.')
    if st.button('More Information', key = 2):
        js = "window.open('https://eosc-testsuite.readthedocs.io/en/latest/testsCatalog.html#data-export-from-the-commercial-cloud-provider-to-zenodo')"  # New tab or window
        js = "window.location.href = 'https://eosc-testsuite.readthedocs.io/en/latest/testsCatalog.html#data-export-from-the-commercial-cloud-provider-to-zenodo'"  # Current tab
        html = '<img src onerror="{}">'.format(js)
        div = Div(text=html)
        st.bokeh_chart(div)

    #st.write('[Repository](https://github.com/cern-it-efp/cloud-exporter)')
    AgGrid(df_data_repatriation, height = 150.00001, fit_columns_on_grid_load=False)
    fig_cpu_bmk = px.bar(df_cpu_bmk, x="Location", y=["Score", "Score Per Core"], barmode='group', range_y = (0,300),height=500)
    fig_perfsonar = px.bar(df_perfsonar, x="Location", y=["Min Latency (ms)", "Mean Latency (ms)","Max Latency (ms)"], barmode='group', range_y = (0,50), height=500)
    fig_perfsonar_bandwidth = px.bar(df_perfsonar,x="Location",y=["Bandwidth From CERN To Provider (Gbps)","Bandwidth From Provider To CERN (Gbps)"], barmode='group',range_y=(0,10), height=500)
    fig_progan = px.bar(df_progan,x="Location",y=['Time (Minutes)'], barmode='group', width = 250, height=500)
    st.markdown("""<hr style="height:2px;border:none;color:#ffc107;background-color:#ffc107;" /> """, unsafe_allow_html=True)

    st.header('High Energy Physics CPU Benchmarking Results')
    st.write('Benchmarking relying on a suite containing several High Energy Physics (HEP) based benchmarks.')
    if st.button('More Information', key = 3):
        js = "window.open('https://eosc-testsuite.readthedocs.io/en/latest/testsCatalog.html#cpu-benchmarking')"  # New tab or window
        js = "https://eosc-testsuite.readthedocs.io/en/latest/testsCatalog.html#cpu-benchmarking'"  # Current tab
        html = '<img src onerror="{}">'.format(js)
        div = Div(text=html)
        st.bokeh_chart(div)
    AgGrid(df_cpu_bmk, height = 150.0001, fit_columns_on_grid_load=False)
    #st.write('CPU Model: '+str(df_cpu_bmk.iloc[0,6]))
    st.plotly_chart(fig_cpu_bmk,config= {'displaylogo': False})
    st.markdown("""<hr style="height:2px;border:none;color:#ffc107;background-color:#ffc107;" /> """, unsafe_allow_html=True)

    st.header('Networking performance measurements')
    st.write('perfSONAR is a network measurement toolkit designed to provide federated coverage of paths, and help to establish end-to-end usage expectations.')
    st.write('In this test, a perfSONAR testpoint is created using a containerised approach on the cloud provider infrastructure.')
    if st.button('More Information', key = 4):
        js = "window.open('https://eosc-testsuite.readthedocs.io/en/latest/testsCatalog.html#networking-performance-measurements')"  # New tab or window
        js = "https://eosc-testsuite.readthedocs.io/en/latest/testsCatalog.html#networking-performance-measurements'"  # Current tab
        html = '<img src onerror="{}">'.format(js)
        div = Div(text=html)
        st.bokeh_chart(div)
    #st.write('[Repository](https://github.com/perfsonar/perfsonar-testpoint-docker)')
    st.subheader('perfSONAR Round Trip Time Test Results')
    st.write("Measure the round trip time and related statistics between CERN and the provider.")
    AgGrid(df_perf_rtt, height = 150.001, fit_columns_on_grid_load=False)
    st.plotly_chart(fig_perfsonar,config= {'displaylogo': False})
    st.subheader('perfSONAR Bandwidth Test Results')
    st.write("A test to measure the observed speed of a data transfer and associated statistics between CERN and the provider.")
    AgGrid(df_perf_bwt, height = 150.01, fit_columns_on_grid_load=False)
    st.plotly_chart(fig_perfsonar_bandwidth,config= {'displaylogo': False})
    
    if len(df_progan)>0:
        st.markdown("""<hr style="height:2px;border:none;color:#ffc107;background-color:#ffc107;" /> """, unsafe_allow_html=True)
        st.header('ProGAN Test Results')
        st.write('Algorithm training of an advanced GAN model (ProGAN). This benchmark is run on a single virtual machine, with a single NVIDIA V100 GPU.')
        if st.button('More Information', key = 5):
            js = "window.open('https://eosc-testsuite.readthedocs.io/en/latest/testsCatalog.html#progressive-growing-of-gans-using-gpus')"  # New tab or window
            js = "https://eosc-testsuite.readthedocs.io/en/latest/testsCatalog.html#progressive-growing-of-gans-using-gpus'"  # Current tab
            html = '<img src onerror="{}">'.format(js)
            div = Div(text=html)
            st.bokeh_chart(div)
        AgGrid(df_progan, height = 150.0001, fit_columns_on_grid_load=False)
        #st.plotly_chart(fig_progan,config= {'displaylogo': False})


hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)