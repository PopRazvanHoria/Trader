import os
from django.core.asgi import get_asgi_application
import logging

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'trader_bot_main.settings')

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

application = get_asgi_application()

logging.info("ASGI application is set up and running.")
