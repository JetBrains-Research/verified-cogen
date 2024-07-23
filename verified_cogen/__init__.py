import logging
import os
from verified_cogen.tools import get_cache_dir
import pathlib


def init_logging():
    log_dir = pathlib.Path(get_cache_dir()) / "log"
    log_dir.mkdir(parents=True, exist_ok=True)

    no_file = os.environ.get("NOFILE")
    logging_file = (log_dir / "llm.log") if no_file is None or no_file == "0" else None

    logging.basicConfig(
        level=os.environ.get("PYLOG_LEVEL", "INFO").upper(),
        filename=logging_file,
    )


init_logging()
