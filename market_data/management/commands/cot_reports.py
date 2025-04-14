import os
import zipfile
import requests
import pandas as pd
from datetime import datetime
from django.core.management.base import BaseCommand
from market.models import COTReport, Symbol


class Command(BaseCommand):
    help = 'Download and import CFTC COT reports'

    def handle(self, *args, **options):
        url = "https://www.cftc.gov/files/dea/history/fut_fin_txt_2020.zip"
        local_zip = "fut_fin_txt_2024.zip"
        extract_path = "cot_data"

        print("📥 Downloading CFTC ZIP file...")
        response = requests.get(url)
        with open(local_zip, "wb") as f:
            f.write(response.content)
        
        with zipfile.ZipFile(local_zip, 'r') as zip_ref:
            zip_ref.extractall(extract_path)
            extracted_files = zip_ref.namelist()
        
        os.remove(local_zip)

        for file in extracted_files:
            if not file.lower().endswith('.txt'):
                continue

            file_path = os.path.join(extract_path, file)
            

            try:
                df = pd.read_csv(file_path, skiprows=0, engine='python')
                print(f"✅ Loaded {len(df)} rows")

                
            except Exception as e:
                print(f"❌ Failed to load {file}: {e}")
                continue

            saved = 0
            for idx, row in df.iterrows():
                try:
                    date_str = str(row.get("As_of_Date_In_Form_YYMMDD", "")).strip()
                    if not date_str.isdigit() or len(date_str) != 6:
                        continue
                    report_date = datetime.strptime(date_str, "%y%m%d").date()
                except Exception:
                    continue

                try:
                    market_name = str(row.get('Market_and_Exchange_Names', '')).strip()
                    if not market_name:
                        continue

                    symbol, _ = Symbol.objects.get_or_create(symbol=market_name)

                    COTReport.objects.create(
                        symbol=symbol,
                        report_date=report_date,
                        open_interest=int(float(row.get('Open_Interest_All') or 0)),
                        commercial_long=int(float(row.get('Dealer_Positions_Long_All') or 0)),
                        commercial_short=int(float(row.get('Dealer_Positions_Short_All') or 0)),
                        non_commercial_long=int(float(row.get('Asset_Mgr_Positions_Long_All') or 0)),
                        non_commercial_short=int(float(row.get('Asset_Mgr_Positions_Short_All') or 0)),
                    )
                    saved += 1

                except Exception as e:
                    print(f"❌ Error saving row {idx}: {e}")
                    continue

            print(f"✅ Saved {saved} rows from {file}")

        print("\n🎉 All done!")
