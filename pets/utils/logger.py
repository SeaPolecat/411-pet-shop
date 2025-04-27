import logging
import sys
from flask import current_app, has_request_context

def configure_logger(logger):
    logger.setLevel(logging.DEBUG)

    handler = logging.StreamHandler(sys.stderr)
    handler.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)

    # Avoid adding duplicate handlers
    if not logger.handlers:
        logger.addHandler(handler)

    # Attach Flask app logger handlers if in a request context
    if has_request_context():
        app_logger = current_app.logger
        for h in app_logger.handlers:
            logger.addHandler(h)
