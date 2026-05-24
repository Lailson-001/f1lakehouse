#%%
import pandas as pd
pd.set_option('display.max_columns',None)

from pathlib import Path
import fastf1
import time
import argparse
from pathlib import Path
#%%
class collectResults:
    
    def __init__(self,years=[2021,2022,2023], modes= ["R","S"]):
        self.years = years
        self.modes = modes
        
    def get_data(self,year,gp,mode) ->pd.DataFrame:
        try:
            session = fastf1.get_session(year,gp,mode)
        except ValueError as err:
            return pd.DataFrame()
        
        session._load_drivers_results()
        
        df= session.results
        df["Mode"] = session.name
        df["year"] = session.date.year
        df["Date"] = session.date
        df["RoundNumber"] = session.event["RoundNumber"]
        df["OfficialEventName"] = session.event["OfficialEventName"]
        df["Country"] = session.event ["Country"]
        df["Location"] = session.event["Location"]
        return df
    
    def get_file_path(
        self,
        year: int,
        gp: int,
        mode: str
        ) -> Path:
        root_dir = Path(__file__).resolve().parent.parent
        data_dir = root_dir / "data"

        data_dir.mkdir(parents=True, exist_ok=True)
        return data_dir / f"{year}_{gp:02}_{mode}.parquet"


    def save_data(
        self,
        df: pd.DataFrame,
        year: int,
        gp: int,
        mode: str
    ) -> None:

        file_path = self.get_file_path(year, gp, mode)

        df.to_parquet(file_path, index=False)   
      
       
        
    def process(self,year,gp,mode):
        df= self.get_data(year,gp,mode)
        
        if df.empty:
            return False
        
        self.save_data(df,year,gp,mode)
        time.sleep(2)
        return True
    
    def process_year_modes(self,year):
        for i in range (1,50):
            for mode in self.modes:
                if not self.process(year,i,mode) and mode =="R":
                    return
                
    def process_years(self):
        for year in self.years:
            print(f"coletando dados do ano{year}")
            self.process_year_modes(year)
            time.sleep(10)
            
#%%
parser = argparse.ArgumentParser()
parser.add_argument("--start",type=int,default=0)
parser.add_argument("--stop", type=int,default=0)
parser.add_argument("--years", "-y", nargs="+", type=int)
parser.add_argument("--modes","-m", nargs="+")
args = parser.parse_args()

if args.years:
    collect = collectResults(args.years,args.modes)
   
elif args.start and args.stop:
    years = [i for i in range(args.start,args.stop+1)]    
    collect = collectResults(years,args.modes)

else:
    parser.error("Você precisa informar --years ou --start/--stop")
    
collect.process_years()

