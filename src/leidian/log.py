# -*- coding: utf-8 -*-
# author: HPCM
# time: 2024/1/12 15:34
# file: logger.py
import logging.config


logconf = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "simple": {
            "format": "[%(levelname).4s %(asctime)s] %(module)s %(lineno)d %(message)s"
        }
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "stream": "ext://sys.stdout",
            "class": "logging.StreamHandler",
            "formatter": "simple"
        }
    },
    "loggers": {
        "leidian": {
            "level": "DEBUG",
            "handlers": [
                "console",
            ],
            "propagate": True
        }
    }
}

logging.config.dictConfig(logconf)
