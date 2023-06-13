# -*- coding: utf-8 -*-
# author: HPCM
# time: 2023/5/29 11:40
# file: __init__.py.py
import importlib.metadata

__version__ = importlib.metadata.version(__package__ or __name__)
