import os
from dotenv import load_dotenv

BASEDIR = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(BASEDIR, ".env"))

class Config(object):
    T1 = "test_string"
    SECRET_KEY= os.environ.get("SECRET_KEY")
    OS_NAME = os.name
    RECAPTCHA_PUBLIC_KEY=os.environ.get("PUBLIC_KEY")
    RECAPTCHA_PRIVATE_KEY=os.environ.get("PRIVATE_KEY")