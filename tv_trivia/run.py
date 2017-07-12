from app import APP
import os
import logging
import sys

a = APP
a.logger.addHandler(logging.StreamHandler(sys.stdout))
a.logger.setLevel(logging.ERROR)

if __name__ == '__main__':
     a.debug = True
     port = int(os.environ.get("PORT", 5000))
     a.run(host='0.0.0.0', port=port)
