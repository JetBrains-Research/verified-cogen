import logging
import os

if not os.path.exists("log"):
    os.mkdir("log")

no_file = os.environ.get("NOFILE")
logging_file = "log/llm.log" if no_file is None or no_file == "0" else None
logging.basicConfig(
    level=os.environ.get("PYLOG_LEVEL", "INFO").upper(),
    filename=logging_file,
)
