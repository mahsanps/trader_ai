import os
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from market.models import FxOptionExpiry


class Command(BaseCommand):
    help = "Download and store ForexLive FX option expiry image for a given date"

    def add_arguments(self, parser):
        parser.add_argument('--date', type=str, help='Date in YYYY-MM-DD format')

    def handle(self, *args, **options):
        date_str = options['date']
        dt = datetime.strptime(date_str, '%Y-%m-%d')
        formatted_date = dt.strftime("%Y%m%d")

        # Try both formats: with zero and without zero
        day_formats = []
        try:
            day_formats.append(dt.strftime('%-d-%B').lower())  # Linux/mac
        except:
            day_formats.append(dt.strftime('%#d-%B').lower())  # Windows fallback
        day_formats.append(dt.strftime('%d-%B').lower())  # Always try full two-digit too

        # Try to fetch the correct page
        response = None
        for day_fmt in day_formats:
            url = f"https://www.forexlive.com/Orders/fx-option-expiries-for-{day_fmt}-10am-new-york-cut-{formatted_date}/"
            print(f"🌐 Trying: {url}")
            r = requests.get(url)
            if r.status_code == 200:
                response = r
                break

        if not response:
            self.stdout.write("❌ Page not found.")
            return

        soup = BeautifulSoup(response.text, "html.parser")
        figure = soup.find("figure", class_="content-data__image")
        if not figure:
            self.stdout.write("❌ Figure with image not found.")
            return

        img = figure.find("img")
        if not img:
            self.stdout.write("❌ Image tag not found inside figure.")
            return

        image_url = img.get("data-src") or img.get("src")
        if not image_url:
            self.stdout.write("❌ Image URL not found.")
            return

        print(f"📷 Image found: {image_url}")
        image_response = requests.get(image_url)
        if image_response.status_code != 200:
            self.stdout.write("❌ Failed to download image.")
            return

        # Save image to model
        image_name = f"{formatted_date}.jpg"
        fx_image, created = FxOptionExpiry.objects.get_or_create(date=dt.date())
        fx_image.image.save(image_name, ContentFile(image_response.content), save=True)

        self.stdout.write(self.style.SUCCESS(f"✅ Image saved for {dt.date()}"))
