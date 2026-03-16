from dotenv import load_dotenv
import os

load_dotenv()

MOODLE_URL = os.getenv("MOODLE_URL")
MOODLE_TOKEN = os.getenv("MOODLE_TOKEN")
MOODLE_FORMAT = os.getenv("MOODLE_FORMAT", "json")
OLD_SCHOOL_YEAR = os.getenv("OLD_SCHOOL_YEAR")
NEW_SCHOOL_YEAR = os.getenv("NEW_SCHOOL_YEAR")

if not MOODLE_URL or not MOODLE_TOKEN:
    raise ValueError("MOODLE_URL and MOODLE_TOKEN must be set in the .env file")