import os
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from market.models import FxOptionExpiry


class Command(BaseCommand):
    help = "Download and store all ForexLive FX option expiry images from 2022 to today"

    def handle(self, *args, **options):
        start_date = datetime(2022, 1, 1)
        end_date = datetime.today()

        current_date = start_date
        while current_date <= end_date:
            formatted_date = current_date.strftime("%Y%m%d")

            # Skip if already exists
            if FxOptionExpiry.objects.filter(date=current_date.date()).exists():
                print(f"✅ Already exists: {current_date.date()}")
                current_date += timedelta(days=1)
                continue

            # Handle different formats for the day part
            day_formats = []
            try:
                day_formats.append(current_date.strftime('%-d-%B').lower())  # Linux/mac
            except:
                day_formats.append(current_date.strftime('%#d-%B').lower())  # Windows
            day_formats.append(current_date.strftime('%d-%B').lower())  # Always try with 2-digit day

            image_found = False
            for day_fmt in day_formats:
                url = f"https://www.forexlive.com/Orders/fx-option-expiries-for-{day_fmt}-10am-new-york-cut-{formatted_date}/"
                print(f"🌐 Trying: {url}")
                r = requests.get(url)
                if r.status_code != 200:
                    continue

                soup = BeautifulSoup(r.text, "html.parser")
                figure = soup.find("figure", class_="content-data__image")
                if not figure:
                    continue

                img = figure.find("img")
                if not img:
                    continue

                image_url = img.get("data-src") or img.get("src")
                if not image_url:
                    continue

                print(f"📷 Image found: {image_url}")
                image_response = requests.get(image_url)
                if image_response.status_code != 200:
                    print("❌ Failed to download image.")
                    break

                image_name = f"{formatted_date}.jpg"
                fx_image, _ = FxOptionExpiry.objects.get_or_create(date=current_date.date())
                fx_image.image.save(image_name, ContentFile(image_response.content), save=True)
                print(f"✅ Image saved for {current_date.date()}")
                image_found = True
                break

            if not image_found:
                print(f"❌ No image for {current_date.date()}")

            current_date += timedelta(days=1)

        print("🎉 Done fetching all FX option expiry images.")
