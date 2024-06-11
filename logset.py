import logging
import os

LOG_FORMAT = "%(asctime)s - %(levelname)s %(filename)s - %(message)s"
logging.basicConfig(filename=os.path.dirname(os.getcwd()) + r'\\output\Log.log', format=LOG_FORMAT, level=logging.DEBUG)
