#%%
from collect import collectResults
import datetime
from sender import Sender

#%%
print("Coletando dados...")
collect_data = collectResults(years=[datetime.datetime.now().year])
collect_data.process_years()

print("Enviando dados...")
Sender_data = Sender(bucket_name="lake-f1-raw", bucket_folder="f1/results")
Sender_data.process_folder("data/")
