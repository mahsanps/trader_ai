from django.core.management import call_command
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'trader_ai.settings')  # جایگزین کن با اسم پروژه‌ات
django.setup()

with open('db.json', 'w', encoding='utf-8') as f:
    call_command('dumpdata', 
                 exclude=['auth.permission', 'contenttypes'], 
                 indent=2, 
                 stdout=f)
