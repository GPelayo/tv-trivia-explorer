from app import APP
import os
import logging
import sys
import settings

a = APP
a.logger.addHandler(logging.StreamHandler(sys.stdout))
a.logger.setLevel(logging.ERROR)

if __name__ == '__main__':
     a.debug = True
     port = int(os.environ.get("PORT", 5000))
     a.run(host=settings.FLASK_HOST_IP, port=port)
