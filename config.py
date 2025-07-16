import os
from dotenv import load_dotenv

class Config(object):
    T1 = "test_string"
    SECRET_KEY= os.environ.get("SECRET_KEY")
    BASEDIR = os.path.abspath(os.path.dirname(__file__))
    OS_NAME = os.name
    RECAPTCHA_PUBLIC_KEY=os.environ.get("PUBLIC_KEY")
    RECAPTCHA_PRIVATE_KEY=os.environ.get("PRIVATE_KEY")