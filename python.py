# STEP1: Import all the packages
import pandas as pd  # import pandas for general file types
import json  # imoprt json for json files
import bs4  # import bs4 for html files
import requests  # import requests for web requests
import sqlalchemy  # import sqlalchemy for sql queries
from PIL import Image  # import pillow for image files
import pydub  # import pydub for audio files
from pydub.playback import play
import playsound  # import playsound for audio files
import geopandas as gpd  # import geopandas for geospatial files
from google.cloud import bigquery  # import bigquery for bigquery files
import matplotlib
import xlrd  # import xlrd for excel files, tab names
import PyPDF2  # import PyPDF2 for pdf files

# Section 1:
# 1. from Kaggle, downloaded two datasets and combined into one xls file
# 2. put the file in the data subfolder
# 3. defined the xls spreadsheet with the variable xls
xls = xlrd.open_workbook(
    '/Users/carolinesanicola/Documents/GitHub/hha-data-ingestion/data/dataset.xls', on_demand=True)
# 4. to see what tabs are in the spreadsheet, create the below command
xls.sheet_names()
# 5. from this, find out there are two tabs: 'BigThree' and 'pokemon'
# 6. define each tab with a variable using the below commands
tab1 = pd.read_excel(
    '/Users/carolinesanicola/Documents/GitHub/hha-data-ingestion/data/dataset.xls', sheet_name='BigThree')
tab2 = pd.read_excel(
    '/Users/carolinesanicola/Documents/GitHub/hha-data-ingestion/data/dataset.xls', sheet_name='pokemon')

# Section 2:
# 1. looked for an open source json API via CMS
# 2. using the already imported 'requests' and 'json' packages,
# set 'apiDataset' variable to the online request of the open source json API link
# 3. make sure the variable is set to the json file associated with the dataset

apiDataset = requests.get(
    'https://data.cms.gov/data-api/v1/dataset/0e312aa0-3508-414c-a874-35e42122f123/data')
apiDataset = apiDataset.json()


# Section 3:
# 1. set up Google Cloud project service account
# 2. add authentication key into folder (and do a gitignore to protect key)
# 3. go to google public database and find two public access database
# 4. create 'client' variable to connect to authentication key
client = bigquery.Client.from_service_account_json(
    '/Users/carolinesanicola/Documents/GitHub/hha-data-ingestion/caroline-507-c98b1afca13c.json')
# 5. create 'query_job' variable to use key to access public database and limit the table to the first 100 rows
query_job = client.query(
    "SELECT * FROM `bigquery-public-data.google_analytics_sample.ga_sessions_*` LIMIT 100")
# 6. make this into a command
results = query_job.result()
# 7. use the 'results' command and name this as variable 'bigquery1'
bigquery1 = pd.DataFrame(results.to_dataframe())

# 8. repeat for second query database
client = bigquery.Client.from_service_account_json(
    '/Users/carolinesanicola/Documents/GitHub/hha-data-ingestion/caroline-507-c98b1afca13c.json')
query_job = client.query(
    "SELECT * FROM `bigquery-public-data.hacker_news.comments` LIMIT 100")
results = query_job.result()
bigquery2 = pd.DataFrame(results.to_dataframe())
