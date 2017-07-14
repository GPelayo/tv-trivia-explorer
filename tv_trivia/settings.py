import os
from selenium import webdriver

try:
    import local_settings
    OMDB_API_KEY = local_settings.OMDB_API_KEY
    FLASK_HOST_IP = local_settings.FLASK_HOST_IP
    SELENIUM_WEBDRIVER_TYPE = local_settings.SELENIUM_WEBDRIVER_TYPE
except ImportError:
    OMDB_API_KEY = os.environ.get('OMDB_API_KEY', None)
    FLASK_HOST_IP = '0.0.0.0'
    SELENIUM_WEBDRIVER_TYPE = webdriver.PhantomJS
