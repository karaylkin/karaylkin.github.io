import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from polls.models import Poll

print("Existing Polls:")
for poll in Poll.objects.all():
    print(f"ID: {poll.id}, Question: {poll.question}")
