import cloudscraper
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from datetime import datetime
import django
import os
from django.utils import timezone
from django.utils.timezone import is_aware, make_aware

# تنظیمات Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "trader_ai.settings")
django.setup()

# مدل‌های Django
from market.models import EconomicCalendar, Currency

def extract_year_from_url(url):
    try:
        parts = url.split("=")
        if len(parts) > 1 and "." in parts[1]:
            return int(parts[1].split(".")[-1])
    except Exception:
        pass
    return datetime.now().year  # اگر سال پیدا نشد، سال جاری را برگردان

def parse_calendar_table(table, base_url):
    """تبدیل جدول تقویم اقتصادی به لیستی از دیکشنری‌ها"""
    rows = []
    current_date = None
    year = extract_year_from_url(base_url)  # استخراج سال از URL

    tbody = table.find("tbody") or table

    for tr in tbody.find_all("tr"):
        tds = tr.find_all("td")
        if not tds:
            continue

        if len(tds) == 1:  # سطر تاریخ
            current_date = tds[0].get_text(strip=True) + f" {year}"  # افزودن سال
            current_date = current_date.replace("Mon", "Mon ").replace("Tue", "Tue ")\
                                         .replace("Wed", "Wed ").replace("Thu", "Thu ")\
                                         .replace("Fri", "Fri ").replace("Sat", "Sat ")\
                                         .replace("Sun", "Sun ")
            print(f"📅 تاریخ پیدا شد: {current_date}")  # چاپ تاریخ برای بررسی
            continue

        cells = [td.get_text(strip=True) for td in tds] + [""] * (10 - len(tds))
        
        full_date = f"{current_date} {cells[0]}" if current_date else ""
        print(f"🛠️ بررسی فرمت تاریخ نهایی: {full_date}")  # چاپ تاریخ قبل از پردازش
        
        try:
            event_date = None
            for date_format in ["%a %b %d %Y %I:%M%p", "%a %b %d %Y", "%b %d %Y %I:%M%p"]:
                try:
                    event_date = datetime.strptime(full_date, date_format)
                    break
                except ValueError:
                    continue

            if not event_date:
                raise ValueError(f"تاریخ قابل تبدیل نیست: {full_date}")

            if event_date.year < 1900:
                print(f"⚠️ تاریخ غیرمعتبر: {full_date}")
                event_date = None
            else:
                if not is_aware(event_date):
                    event_date = make_aware(event_date, timezone.get_current_timezone())
        
        except ValueError as e:
            print(f"⚠️ مشکل در تبدیل تاریخ: {full_date}")
            event_date = None

        row_dict = {
            "event_id": f"{cells[1]}-{event_date}" if event_date else None,
            "date": event_date,
            "time": cells[1],
            "currency": cells[2],
            "impact": cells[3],
            "event": cells[4],
            "detail": cells[5],
            "actual": cells[6],
            "forecast": cells[7],
            "previous": cells[8],
            "graph": cells[9],
            "source_url": base_url
        }
        rows.append(row_dict)
        print(f"event_date: {event_date}")
    return rows

def fetch_calendar_table_dict(url: str):
   
    scraper = cloudscraper.create_scraper(browser='chrome')
    html_content = scraper.get(url, timeout=15).text
    
    soup = BeautifulSoup(html_content, "html.parser")
    
    table = soup.find("table", class_="calendar__table")
    if table is None:
        print("❌ جدول تقویم پیدا نشد!")
        return []
   
    return parse_calendar_table(table, url)

def save_to_database(data_list):
    """ذخیره داده‌های استخراج شده در دیتابیس Django"""
    existing_events = EconomicCalendar.objects.values_list("event_id", flat=True)
    print(f"📊 تعداد رویدادهای موجود در دیتابیس: {len(existing_events)}")
    
    new_events = []
    for data in data_list:
        if data["event_id"] not in existing_events and data["date"]:
            currency, _ = Currency.objects.get_or_create(currency=data["currency"])
            new_events.append(EconomicCalendar(
                event_id=data["event_id"],
                date=data["date"],
                time=data["time"],
                impact=data["impact"],
                event=data["event"],
                actual=data["actual"],
                forecast=data["forecast"],
                previous=data["previous"],
                source_url=data["source_url"],
                currency=currency
            ))
    
    if new_events:
        EconomicCalendar.objects.bulk_create(new_events)
        print(f"✅ {len(new_events)} رویداد جدید ذخیره شد!")
    else:
        print("⏳ هیچ رویداد جدیدی یافت نشد.")

def main():
    url = "https://www.forexfactory.com/calendar?month=nov.2024"
    print(f"🌐 دریافت داده از: {url}")
    try:
        calendar_data = fetch_calendar_table_dict(url)
        if calendar_data:
            print(f"🔍 تعداد داده‌های استخراج شده: {len(calendar_data)}")
        else:
            print("⚠️ هیچ داده‌ای از سایت دریافت نشد!")
        save_to_database(calendar_data)
    except Exception as e:
        print(f"❌ خطا در پردازش: {e}")

if __name__ == "__main__":
    main()
