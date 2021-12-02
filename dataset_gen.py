import io
import os
import pandas as pd
import numpy as np
import json
import gc
import glob
from pathlib import Path
import boto3

#f = open(".streamlit/config.toml","w+")
#f.write('[theme]\n base="light"\n primaryColor="#ffc107"\n backgroundColor="#264899"\n secondaryBackgroundColor="#264899"\n textColor="#fafafa"\n font="sans serif"')
#f.close()

import yaml

with open("/tmp/creds.yaml", 'r') as inputfile:
    s3_creds = yaml.load(inputfile, Loader=yaml.FullLoader)

OPENSTACK_ACC = s3_creds["OPENSTACK_ACC"]
OPENSTACK_KEY = s3_creds["OPENSTACK_KEY"]

my_file = Path("/tmp/summary_perfsonar.csv")
my_file_new = Path("/tmp/cpd.csv")
if my_file.is_file()==True or my_file_new.is_file()==True:
   os.system("rm -r /tmp/*.csv")

client_s3=boto3.client(
    "s3",
    aws_access_key_id=OPENSTACK_ACC,
    aws_secret_access_key=OPENSTACK_KEY,
    endpoint_url="https://s3.cern.ch"
)

cloud_platform_details = "Cloud Platforms Details - Sheet1_min.csv"
obj_cpd=client_s3.get_object(Bucket='ocre-results', Key=cloud_platform_details)
df_cpd = pd.read_csv(io.BytesIO(obj_cpd['Body'].read()))
df_cpd.to_csv('/tmp/cpd.csv',index=False)

for key in client_s3.list_objects(Bucket='ocre-results')['Contents']:
    #print(str(str(key['Key']).split('/')[-1]).split('.')[-1])
    if(str(key['Key']).split('/')[0]=="google" or str(key['Key']).split('/')[0]=="aws" or str(key['Key']).split('/')[0]=="cloudferro" or str(key['Key']).split('/')[0]=="cloudsigma" or str(key['Key']).split('/')[0]=="azurerm" or str(key['Key']).split('/')[0]=="exoscale" or str(key['Key']).split('/')[0]=="ionoscloud" or str(key['Key']).split('/')[0]=="oci" or str(key['Key']).split('/')[0]=="opentelekomcloud" or str(key['Key']).split('/')[0]=="ovh" or str(key['Key']).split('/')[0]=="ibm" or str(key['Key']).split('/')[0]=="citynetwork" or str(key['Key']).split('/')[0]=="x-ion" or str(key['Key']).split('/')[0]=="flexibleengine"):

        if(str(key['Key']).split('/')[-2]!="detailed") and str(str(key['Key']).split('/')[-1]).split('.')[-1]=="json":
            source_general = str(key['Key']).split('/')[0]+"/"+str(key['Key']).split('/')[1]+"/general.json"
            print(str(key['Key']).split('/')[0]+"/"+str(key['Key']).split('/')[1]+"/general.json")
            obj_general=client_s3.get_object(Bucket='ocre-results',Key=source_general)
            df_general = json.load(io.BytesIO(obj_general['Body'].read()))
            gc.collect()

            if str(df_general["testsCatalog"]["cpuBenchmarking"]["run"])=="True":
                print("Fetching CPU Benchmarking Results "+str(str(key['Key']).split('/')[1]))
                source_cpu_bench = str(key['Key']).split('/')[0]+"/"+str(key['Key']).split('/')[1]+"/detailed/cpu_benchmarking.json"
                obj_cpu_bench=client_s3.get_object(Bucket='ocre-results',Key=source_cpu_bench)
                df_cpu_bench = json.load(io.BytesIO(obj_cpu_bench['Body'].read()))
                gc.collect()
                with open('/tmp/summary_cpu_bench.csv', 'a+') as f:                        
                    if(str(key['Key']).split('/')[0]=="cloudferro"):
                        f.write(str(key['Key']).split('/')[0]+", "+str(df_general["info"]["flavor"])+', '+"waw_pl"+", "+str(key['Key']).split('/')[1]+", "+str(df_cpu_bench["profiles"]["hepscore"]["score"])+", "+str(df_cpu_bench["profiles"]["hepscore"]["score_per_core"])+", "+str(df_cpu_bench["host"]["HW"]["CPU"]["CPU_Model"])+",  "+str(df_cpu_bench["profiles"]["hepscore"]["environment"]["start_at"])+",  "+str(df_cpu_bench["profiles"]["hepscore"]["environment"]["end_at"])+"\n")
                    elif(str(key['Key']).split('/')[0]=="ionoscloud"):
                        f.write(str(key['Key']).split('/')[0]+", "+str(df_general["info"]["flavor"]["cores"])+'-'+str(df_general["info"]["flavor"]["ram"])+", "+df_general["info"]["location"]+", "+str(key['Key']).split('/')[1]+", "+str(df_cpu_bench["profiles"]["hepscore"]["score"])+", "+str(df_cpu_bench["profiles"]["hepscore"]["score_per_core"])+",  "+str(df_cpu_bench["host"]["HW"]["CPU"]["CPU_Model"]).replace(",", " ")+",   "+str(df_cpu_bench["profiles"]["hepscore"]["environment"]["start_at"])+",  "+str(df_cpu_bench["profiles"]["hepscore"]["environment"]["end_at"])+"\n")
                    elif(str(key['Key']).split('/')[0]=="cloudsigma"):
                        f.write(str(key['Key']).split('/')[0]+", "+str(round((-41*df_general["info"]["flavor"]["cpu"]-90)/-120000,0))+'-'+str(round(df_general["info"]["flavor"]["memory"]/1000000000,1))+", "+df_general["info"]["location"]+", "+str(key['Key']).split('/')[1]+", "+str(df_cpu_bench["profiles"]["hepscore"]["score"])+", "+str(df_cpu_bench["profiles"]["hepscore"]["score_per_core"])+",  "+str(df_cpu_bench["host"]["HW"]["CPU"]["CPU_Model"]).replace(",", " ")+",   "+str(df_cpu_bench["profiles"]["hepscore"]["environment"]["start_at"])+",  "+str(df_cpu_bench["profiles"]["hepscore"]["environment"]["end_at"])+"\n")                    
                    elif(str(key['Key']).split('/')[0]=="ovh" or str(key['Key']).split('/')[0]=="citynetwork"):
                        f.write(str(key['Key']).split('/')[0]+", "+str(df_general["info"]["flavor"])+", "+df_general["info"]["region"]+", "+str(key['Key']).split('/')[1]+", "+str(df_cpu_bench["profiles"]["hepscore"]["score"])+", "+str(df_cpu_bench["profiles"]["hepscore"]["score_per_core"])+",  "+str(df_cpu_bench["host"]["HW"]["CPU"]["CPU_Model"]).replace(",", " ")+",   "+str(df_cpu_bench["profiles"]["hepscore"]["environment"]["start_at"])+",  "+str(df_cpu_bench["profiles"]["hepscore"]["environment"]["end_at"])+"\n")                    
                    elif(str(key['Key']).split('/')[0]=="ibm"):
                        if(str(df_general["info"]).find("'region'")!=-1):
                            f.write(str(key['Key']).split('/')[0]+", "+str(df_general["info"]["flavor"])+", "+df_general["info"]["region"]+", "+str(key['Key']).split('/')[1]+", "+str(df_cpu_bench["profiles"]["hepscore"]["score"])+", "+str(df_cpu_bench["profiles"]["hepscore"]["score_per_core"])+",  "+str(df_cpu_bench["host"]["HW"]["CPU"]["CPU_Model"]).replace(",", " ")+",   "+str(df_cpu_bench["profiles"]["hepscore"]["environment"]["start_at"])+",  "+str(df_cpu_bench["profiles"]["hepscore"]["environment"]["end_at"])+"\n")                    
                        elif(str(df_general["info"]).find("'datacenter'")!=-1):
                            f.write(str(key['Key']).split('/')[0]+", "+str(df_general["info"]["flavor"])+", "+df_general["info"]["datacenter"]+", "+str(key['Key']).split('/')[1]+", "+str(df_cpu_bench["profiles"]["hepscore"]["score"])+", "+str(df_cpu_bench["profiles"]["hepscore"]["score_per_core"])+",  "+str(df_cpu_bench["host"]["HW"]["CPU"]["CPU_Model"]).replace(",", " ")+",   "+str(df_cpu_bench["profiles"]["hepscore"]["environment"]["start_at"])+",  "+str(df_cpu_bench["profiles"]["hepscore"]["environment"]["end_at"])+"\n")                     
                    elif(str(key['Key']).split('/')[0]=="x-ion" or str(key['Key']).split('/')[0]=="flexibleengine"):
                        f.write(str(key['Key']).split('/')[0]+", "+str(df_general["info"]["flavor"])+", "+df_general["info"]["availabilityZone"]+", "+str(key['Key']).split('/')[1]+", "+str(df_cpu_bench["profiles"]["hepscore"]["score"])+", "+str(df_cpu_bench["profiles"]["hepscore"]["score_per_core"])+",  "+str(df_cpu_bench["host"]["HW"]["CPU"]["CPU_Model"]).replace(",", " ")+",   "+str(df_cpu_bench["profiles"]["hepscore"]["environment"]["start_at"])+",  "+str(df_cpu_bench["profiles"]["hepscore"]["environment"]["end_at"])+"\n")                    
                    else:
                        f.write(str(key['Key']).split('/')[0]+", "+str(df_general["info"]["flavor"])+', '+df_general["info"]["zone"]+", "+str(key['Key']).split('/')[1]+", "+str(df_cpu_bench["profiles"]["hepscore"]["score"])+", "+str(df_cpu_bench["profiles"]["hepscore"]["score_per_core"])+", "+str(df_cpu_bench["host"]["HW"]["CPU"]["CPU_Model"])+",  "+str(df_cpu_bench["profiles"]["hepscore"]["environment"]["start_at"])+", "+str(df_cpu_bench["profiles"]["hepscore"]["environment"]["end_at"])+"\n")
                    f.close
                gc.collect()

            if str(df_general["testsCatalog"]["perfsonarTest"]["run"])=="True":
                print("Fetching PerfSONAR Test Results "+str(key['Key']).split('/')[1])
                source_perfsonar = str(key['Key']).split('/')[0]+"/"+str(key['Key']).split('/')[1]+"/detailed/perfsonar_results.json"
                obj_perfsonar=client_s3.get_object(Bucket='ocre-results', Key=source_perfsonar)
                df_perfsonar = json.load(io.BytesIO(obj_perfsonar['Body'].read()))            
                obj_general=client_s3.get_object(Bucket='ocre-results', Key=source_general)
                df_general = json.load(io.BytesIO(obj_general['Body'].read()))
                gc.collect()

                with open('/tmp/summary_perfsonar.csv', 'a+') as f:
                    if(str(key['Key']).split('/')[0]=="cloudferro"):
                        if df_perfsonar[3]['succeeded']!=False:
                            f.write(str(key['Key']).split('/')[0]+", "+str(df_general["info"]["flavor"])+', '+"waw_pl"+", "+str(key['Key']).split('/')[1]+", "+str(str(df_perfsonar[0]["max"]).replace("PT","")).replace("S","")+", "+str(str(df_perfsonar[0]["mean"]).replace("PT","")).replace("S","")+", "+str(str(df_perfsonar[0]["min"]).replace("PT","")).replace("S","")+", "+str(df_perfsonar[3]['summary']['summary']['throughput-bits']/1000000000)+", "+str(df_perfsonar[4]['summary']['summary']['throughput-bits']/1000000000)+"\n")
                    elif(str(key['Key']).split('/')[0]=="ionoscloud"):
                        if df_perfsonar[3]['succeeded']!=False:
                            f.write(str(key['Key']).split('/')[0]+", "+str(df_general["info"]["flavor"]["cores"])+'-'+str(df_general["info"]["flavor"]["ram"])+", "+df_general["info"]["location"]+", "+str(key['Key']).split('/')[1]+", "+str(str(df_perfsonar[0]["max"]).replace("PT","")).replace("S","")+", "+str(str(df_perfsonar[0]["mean"]).replace("PT","")).replace("S","")+", "+str(str(df_perfsonar[0]["min"]).replace("PT","")).replace("S","")+", "+str(df_perfsonar[3]['summary']['summary']['throughput-bits']/1000000000)+","+str(df_perfsonar[4]['summary']['summary']['throughput-bits']/1000000000)+"\n")                    
                    elif(str(key['Key']).split('/')[0]=="cloudsigma"):
                        if df_perfsonar[3]['succeeded']!=False:
                            f.write(str(key['Key']).split('/')[0]+", "+str(round((-41*df_general["info"]["flavor"]["cpu"]-90)/-120000,0))+'-'+str(round(df_general["info"]["flavor"]["memory"]/1000000000,1))+", "+df_general["info"]["location"]+", "+str(key['Key']).split('/')[1]+", "+str(str(df_perfsonar[0]["max"]).replace("PT","")).replace("S","")+", "+str(str(df_perfsonar[0]["mean"]).replace("PT","")).replace("S","")+", "+str(str(df_perfsonar[0]["min"]).replace("PT","")).replace("S","")+", "+str(df_perfsonar[3]['summary']['summary']['throughput-bits']/1000000000)+","+str(df_perfsonar[4]['summary']['summary']['throughput-bits']/1000000000)+"\n")                    
                    elif(str(key['Key']).split('/')[0]=="ovh"):
                        if((str(key['Key']).split('/')[1]!="04-10-2021_19-14-41") and (str(key['Key']).split('/')[1].find("25-10-2021")==-1)):
                            if df_perfsonar[3]['succeeded']!=False:
                                f.write(str(key['Key']).split('/')[0]+", "+str(df_general["info"]["flavor"])+', '+df_general["info"]["region"]+", "+str(key['Key']).split('/')[1]+", "+str(str(df_perfsonar[0]["max"]).replace("PT","")).replace("S","")+", "+str(str(df_perfsonar[0]["mean"]).replace("PT","")).replace("S","")+", "+str(str(df_perfsonar[0]["min"]).replace("PT","")).replace("S","")+", "+str(df_perfsonar[3]['summary']['summary']['throughput-bits']/1000000000)+", "+str(df_perfsonar[4]['summary']['summary']['throughput-bits']/1000000000)+"\n")                            
                        elif(str(key['Key']).split('/')[1]=="04-10-2021_19-14-41" or (str(key['Key']).split('/')[1].find("25-10-2021")!=-1)):
                            if df_perfsonar[3]['succeeded']!=False:
                                f.write(str(key['Key']).split('/')[0]+", "+str(df_general["info"]["flavor"])+', '+df_general["info"]["region"]+", "+str(key['Key']).split('/')[1]+", "+str(str(df_perfsonar[0]["max"]).replace("PT","")).replace("S","")+", "+str(str(df_perfsonar[0]["mean"]).replace("PT","")).replace("S","")+", "+str(str(df_perfsonar[0]["min"]).replace("PT","")).replace("S","")+", "+str(df_perfsonar[4]['summary']['summary']['throughput-bits']/1000000000)+", "+str(df_perfsonar[5]['summary']['summary']['throughput-bits']/1000000000)+"\n")                            
                    elif(str(key['Key']).split('/')[0]=="ibm"):
                        if(str(df_general["info"]).find("'region'")!=-1):
                            if df_perfsonar[4]['succeeded']!=False:
                                f.write(str(key['Key']).split('/')[0]+", "+str(df_general["info"]["flavor"])+', '+df_general["info"]["region"]+", "+str(key['Key']).split('/')[1]+", "+str(str(df_perfsonar[0]["max"]).replace("PT","")).replace("S","")+", "+str(str(df_perfsonar[0]["mean"]).replace("PT","")).replace("S","")+", "+str(str(df_perfsonar[0]["min"]).replace("PT","")).replace("S","")+", "+str(df_perfsonar[4]['summary']['summary']['throughput-bits']/1000000000)+", "+str(df_perfsonar[5]['summary']['summary']['throughput-bits']/1000000000)+"\n")                            
                        elif(str(df_general["info"]).find("'datacenter'")!=-1):
                            if df_perfsonar[3]['succeeded']!=False:
                                f.write(str(key['Key']).split('/')[0]+", "+str(df_general["info"]["flavor"])+', '+df_general["info"]["datacenter"]+", "+str(key['Key']).split('/')[1]+", "+str(str(df_perfsonar[0]["max"]).replace("PT","")).replace("S","")+", "+str(str(df_perfsonar[0]["mean"]).replace("PT","")).replace("S","")+", "+str(str(df_perfsonar[0]["min"]).replace("PT","")).replace("S","")+", "+str(df_perfsonar[3]['summary']['summary']['throughput-bits']/1000000000)+", "+str(df_perfsonar[4]['summary']['summary']['throughput-bits']/1000000000)+"\n")                            
                    elif(str(key['Key']).split('/')[0]=="x-ion"):
                        if df_perfsonar[3]['succeeded']!=False:                        
                            f.write(str(key['Key']).split('/')[0]+", "+str(df_general["info"]["flavor"])+', '+df_general["info"]["availabilityZone"]+", "+str(key['Key']).split('/')[1]+", "+str(str(df_perfsonar[0]["max"]).replace("PT","")).replace("S","")+", "+str(str(df_perfsonar[0]["mean"]).replace("PT","")).replace("S","")+", "+str(str(df_perfsonar[0]["min"]).replace("PT","")).replace("S","")+", "+str(df_perfsonar[3]['summary']['summary']['throughput-bits']/1000000000)+", "+str(df_perfsonar[4]['summary']['summary']['throughput-bits']/1000000000)+"\n")                            
                    elif(str(key['Key']).split('/')[0]=="exoscale"):
                        if df_perfsonar[3]['succeeded']!=False:
                            if((str(key['Key']).split('/')[1].find("11-11-2021")!=-1)):
                                f.write(str(key['Key']).split('/')[0]+", "+str(df_general["info"]["flavor"])+', '+df_general["info"]["zone"]+", "+str(key['Key']).split('/')[1]+", "+str(str(df_perfsonar[0]["max"]).replace("PT","")).replace("S","")+", "+str(str(df_perfsonar[0]["mean"]).replace("PT","")).replace("S","")+", "+str(str(df_perfsonar[0]["min"]).replace("PT","")).replace("S","")+", "+str(df_perfsonar[4]['summary']['summary']['throughput-bits']/1000000000)+", "+str(df_perfsonar[5]['summary']['summary']['throughput-bits']/1000000000)+"\n")                            
                            else:
                                f.write(str(key['Key']).split('/')[0]+", "+str(df_general["info"]["flavor"])+', '+df_general["info"]["zone"]+", "+str(key['Key']).split('/')[1]+", "+str(str(df_perfsonar[0]["max"]).replace("PT","")).replace("S","")+", "+str(str(df_perfsonar[0]["mean"]).replace("PT","")).replace("S","")+", "+str(str(df_perfsonar[0]["min"]).replace("PT","")).replace("S","")+", "+str(df_perfsonar[3]['summary']['summary']['throughput-bits']/1000000000)+","+str(df_perfsonar[4]['summary']['summary']['throughput-bits']/1000000000)+"\n") 
                    elif(str(key['Key']).split('/')[0]=="citynetwork"):
                        if df_perfsonar[4]['succeeded']!=False:
                            f.write(str(key['Key']).split('/')[0]+", "+str(df_general["info"]["flavor"])+', '+df_general["info"]["region"]+", "+str(key['Key']).split('/')[1]+", "+str(str(df_perfsonar[0]["max"]).replace("PT","")).replace("S","")+", "+str(str(df_perfsonar[0]["mean"]).replace("PT","")).replace("S","")+", "+str(str(df_perfsonar[0]["min"]).replace("PT","")).replace("S","")+", "+str(df_perfsonar[4]['summary']['summary']['throughput-bits']/1000000000)+", "+str(df_perfsonar[5]['summary']['summary']['throughput-bits']/1000000000)+"\n")
                    elif(str(key['Key']).split('/')[0]=="flexibleengine"):
                        if df_perfsonar[4]['succeeded']!=False:
                            f.write(str(key['Key']).split('/')[0]+", "+str(df_general["info"]["flavor"])+', '+df_general["info"]["availabilityZone"]+", "+str(key['Key']).split('/')[1]+", "+str(str(df_perfsonar[0]["max"]).replace("PT","")).replace("S","")+", "+str(str(df_perfsonar[0]["mean"]).replace("PT","")).replace("S","")+", "+str(str(df_perfsonar[0]["min"]).replace("PT","")).replace("S","")+", "+str(df_perfsonar[4]['summary']['summary']['throughput-bits']/1000000000)+", "+str(df_perfsonar[5]['summary']['summary']['throughput-bits']/1000000000)+"\n")
                    else:
                        if df_perfsonar[3]['succeeded']!=False:                        
                            f.write(str(key['Key']).split('/')[0]+", "+str(df_general["info"]["flavor"])+', '+df_general["info"]["zone"]+", "+str(key['Key']).split('/')[1]+", "+str(str(df_perfsonar[0]["max"]).replace("PT","")).replace("S","")+", "+str(str(df_perfsonar[0]["mean"]).replace("PT","")).replace("S","")+", "+str(str(df_perfsonar[0]["min"]).replace("PT","")).replace("S","")+", "+str(df_perfsonar[3]['summary']['summary']['throughput-bits']/1000000000)+","+str(df_perfsonar[4]['summary']['summary']['throughput-bits']/1000000000)+"\n") 
                    f.close
                gc.collect()

            if str(df_general["testsCatalog"]["dodasTest"]["run"])=="True":
                print("Fetching DODAS Test Results "+str(key['Key']).split('/')[1])
                source_dodas = str(key['Key']).split('/')[0]+"/"+str(key['Key']).split('/')[1]+"/detailed/dodas_results.json"
                obj_dodas=client_s3.get_object(Bucket='ocre-results', Key=source_dodas)
                df_dodas = json.load(io.BytesIO(obj_dodas['Body'].read()))            
                obj_general=client_s3.get_object(Bucket='ocre-results', Key=source_general)
                df_general = json.load(io.BytesIO(obj_general['Body'].read()))
                gc.collect()

                with open('/tmp/summary_dodas.csv', 'a+') as f:
                    if(str(key['Key']).split('/')[0]=="cloudferro"):
                        f.write(str(key['Key']).split('/')[0]+", "+str(df_general["info"]["flavor"])+', '+"waw_pl"+", "+str(key['Key']).split('/')[1]+", "+str(df_dodas["result"])+"\n")
                    elif(str(key['Key']).split('/')[0]=="ionoscloud"):
                        f.write(str(key['Key']).split('/')[0]+", "+str(df_general["info"]["flavor"]["cores"])+'-'+str(df_general["info"]["flavor"]["ram"]/1000)+", "+df_general["info"]["location"]+", "+str(key['Key']).split('/')[1]+", "+str(df_dodas["result"])+"\n")                    
                    elif(str(key['Key']).split('/')[0]=="cloudsigma"):
                        f.write(str(key['Key']).split('/')[0]+", "+str(round((-41*df_general["info"]["flavor"]["cpu"]-90)/-120000,0))+'-'+str(round(df_general["info"]["flavor"]["memory"]/1000000000,1))+", "+df_general["info"]["location"]+", "+str(key['Key']).split('/')[1]+", "+str(df_dodas["result"])+"\n")                    
                    elif(str(key['Key']).split('/')[0]=="ovh" or str(key['Key']).split('/')[0]=="citynetwork"):
                        f.write(str(key['Key']).split('/')[0]+", "+str(df_general["info"]["flavor"])+', '+df_general["info"]["region"]+", "+str(key['Key']).split('/')[1]+", "+str(df_dodas["result"])+"\n")
                    elif(str(key['Key']).split('/')[0]=="ibm"):
                        if(str(df_general["info"]).find("'region'")!=-1):
                            f.write(str(key['Key']).split('/')[0]+", "+str(df_general["info"]["flavor"])+', '+df_general["info"]["region"]+", "+str(key['Key']).split('/')[1]+", "+str(df_dodas["result"])+"\n")
                        elif(str(df_general["info"]).find("'datacenter'")!=-1):
                            f.write(str(key['Key']).split('/')[0]+", "+str(df_general["info"]["flavor"])+', '+df_general["info"]["datacenter"]+", "+str(key['Key']).split('/')[1]+", "+str(df_dodas["result"])+"\n")

                    elif(str(key['Key']).split('/')[0]=="x-ion" or str(key['Key']).split('/')[0]=="flexibleengine"):
                        f.write(str(key['Key']).split('/')[0]+", "+str(df_general["info"]["flavor"])+', '+df_general["info"]["availabilityZone"]+", "+str(key['Key']).split('/')[1]+", "+str(df_dodas["result"])+"\n")
                    
                    else:
                        f.write(str(key['Key']).split('/')[0]+", "+str(df_general["info"]["flavor"])+', '+df_general["info"]["zone"]+", "+str(key['Key']).split('/')[1]+", "+str(df_dodas["result"])+"\n") 
                    f.close
                gc.collect()

            if str(df_general["testsCatalog"]["dataRepatriationTest"]["run"])=="True":
                print("Fetching Data Repatriation Test Results "+str(key['Key']).split('/')[1])
                source_data_repatriation = str(key['Key']).split('/')[0]+"/"+str(key['Key']).split('/')[1]+"/detailed/data_repatriation_test.json"
                obj_data_repatriation=client_s3.get_object(Bucket='ocre-results', Key=source_data_repatriation)
                df_data_repatriation = json.load(io.BytesIO(obj_data_repatriation['Body'].read()))            
                obj_general=client_s3.get_object(Bucket='ocre-results', Key=source_general)
                df_general = json.load(io.BytesIO(obj_general['Body'].read()))
                gc.collect()

                with open('/tmp/summary_data_repatriation.csv', 'a+') as f:
                    if(str(key['Key']).split('/')[0]=="cloudferro"):
                        f.write(str(key['Key']).split('/')[0]+", "+str(df_general["info"]["flavor"])+', '+"waw_pl"+", "+str(key['Key']).split('/')[1]+", "+str(df_data_repatriation["result"])+"\n")
                    elif(str(key['Key']).split('/')[0]=="ionoscloud"):
                        f.write(str(key['Key']).split('/')[0]+", "+str(df_general["info"]["flavor"]["cores"])+'-'+str(df_general["info"]["flavor"]["ram"])+", "+df_general["info"]["location"]+", "+str(key['Key']).split('/')[1]+", "+str(df_data_repatriation["result"])+"\n")                    
                    elif(str(key['Key']).split('/')[0]=="cloudsigma"):
                        f.write(str(key['Key']).split('/')[0]+", "+str(round((-41*df_general["info"]["flavor"]["cpu"]-90)/-120000,0))+'-'+str(round(df_general["info"]["flavor"]["memory"]/1000000000,1))+", "+df_general["info"]["location"]+", "+str(key['Key']).split('/')[1]+", "+str(df_data_repatriation["result"])+"\n")                    
                    elif(str(key['Key']).split('/')[0]=="ovh" or str(key['Key']).split('/')[0]=="citynetwork"):
                        f.write(str(key['Key']).split('/')[0]+", "+str(df_general["info"]["flavor"])+', '+df_general["info"]["region"]+", "+str(key['Key']).split('/')[1]+", "+str(df_data_repatriation["result"])+"\n")
                    elif(str(key['Key']).split('/')[0]=="ibm"):
                        if(str(df_general["info"]).find("'region'")!=-1):
                            f.write(str(key['Key']).split('/')[0]+", "+str(df_general["info"]["flavor"])+', '+str(df_general["info"]['region'])+", "+str(key['Key']).split('/')[1]+", "+str(df_data_repatriation["result"])+"\n")                    
                        elif(str(df_general["info"]).find("'datacenter'")!=-1):
                            f.write(str(key['Key']).split('/')[0]+", "+str(df_general["info"]["flavor"])+', '+str(df_general["info"]['datacenter'])+", "+str(key['Key']).split('/')[1]+", "+str(df_data_repatriation["result"])+"\n")                    

                    elif(str(key['Key']).split('/')[0]=="x-ion" or str(key['Key']).split('/')[0]=="flexibleengine"):
                        f.write(str(key['Key']).split('/')[0]+", "+str(df_general["info"]["flavor"])+', '+df_general["info"]["availabilityZone"]+", "+str(key['Key']).split('/')[1]+", "+str(df_data_repatriation["result"])+"\n")                    
                    
                    else:
                        f.write(str(key['Key']).split('/')[0]+", "+str(df_general["info"]["flavor"])+', '+df_general["info"]["zone"]+", "+str(key['Key']).split('/')[1]+", "+str(df_data_repatriation["result"])+"\n") 
                    f.close
                gc.collect()

            if str(df_general["testsCatalog"]["proGANTest"]["run"])=="True":
                print("Fetching proGAN Test Results "+str(key['Key']).split('/')[1])
                source_progan = str(key['Key']).split('/')[0]+"/"+str(key['Key']).split('/')[1]+"/detailed/time.json"
                obj_progan=client_s3.get_object(Bucket='ocre-results', Key=source_progan)
                df_progan = json.load(io.BytesIO(obj_progan['Body'].read()))            
                obj_general=client_s3.get_object(Bucket='ocre-results', Key=source_general)
                df_general = json.load(io.BytesIO(obj_general['Body'].read()))
                gc.collect()

                with open('/tmp/summary_progan.csv', 'a+') as f:                    
                    if(str(key['Key']).split('/')[0]=="ovh"):
                        f.write(str(key['Key']).split('/')[0]+", "+str(df_general["testsCatalog"]["proGANTest"]["flavor"])+', '+str(df_general["info"]["region"])+", "+str(key['Key']).split('/')[1]+", "+str(df_general["testsCatalog"]["proGANTest"]["images_amount"])+", "+str(df_general["testsCatalog"]["proGANTest"]["kimg"])+", nvidia-tesla-v100"+", 1"+", "+str(df_progan["time"])+"\n")
                    elif(str(key['Key']).split('/')[0]=="flexibleengine"):
                        f.write(str(key['Key']).split('/')[0]+", "+str(df_general["testsCatalog"]["proGANTest"]["flavor"])+', '+str(df_general["info"]["availabilityZone"])+", "+str(key['Key']).split('/')[1]+", "+str(df_general["testsCatalog"]["proGANTest"]["images_amount"])+", "+str(df_general["testsCatalog"]["proGANTest"]["kimg"])+", nvidia-tesla-v100"+", 1"+", "+str(df_progan["time"])+"\n")                   
                    else:
                        f.write(str(key['Key']).split('/')[0]+", "+str(df_general["testsCatalog"]["proGANTest"]["flavor"])+', '+str(df_general["info"]["zone"])+", "+str(key['Key']).split('/')[1]+", "+str(df_general["testsCatalog"]["proGANTest"]["images_amount"])+", "+str(df_general["testsCatalog"]["proGANTest"]["kimg"])+", "+str(df_general["info"]["gpuType"])+", "+str(df_general["info"]["gpusPerNode"])+", "+str(df_progan["time"])+"\n")
                    f.close()
                        
            if str(df_general["testsCatalog"]["dlTest"]["run"])=="True":
                print("Fetching DL Test Results")

            if str(df_general["testsCatalog"]["hpcTest"]["run"])=="True":
                print("Fetching HPC Test Results")
        gc.collect()

    gc.collect()

os.system("echo PORT $PORT")
#os.system('streamlit run --server.port $PORT app.py')