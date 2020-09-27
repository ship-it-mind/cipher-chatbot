import os

from dotenv import load_dotenv


dot_env_path = os.path.join(os.path.dirname(__file__),
                            os.path.join(os.getcwd(), '.env'))
load_dotenv(dot_env_path)

FB_PAGE_ACCESS_TOKEN = os.getenv("FB_PAGE_ACCESS_TOKEN")
FB_VERIFY_TOKEN = os.getenv("FB_VERIFY_TOKEN")
