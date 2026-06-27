#%%
from collect import collectResults
import datetime
from sender import Sender
import dotenv
import os
import time
dotenv.load_dotenv()
BUCKET_NAME = os.getenv("BUCKET_NAME")


#%%

while True:
    
    print("Iniciando processo")
    
    print("Coletando dados")
    collect_data = collectResults(years=[datetime.datetime.now().year])
    collect_data.process_years()

    print("Enviando dados...")
    Sender_data = Sender(bucket_name= BUCKET_NAME,bucket_folder="f1-results-raw/results")
    Sender_data.process_folder("data/")

    print("Iteração finalizada")
    time.sleep(60*60*6)