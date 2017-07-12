import os

try:
    import local_settings
    OMDB_API_KEY = local_settings.OMDB_API_KEY
except ImportError:
    OMDB_API_KEY = os.environ.get('OMDB_API_KEY', None)
