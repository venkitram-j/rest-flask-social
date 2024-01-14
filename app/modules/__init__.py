"""
Module initialization
"""
from importlib import import_module


ENABLED_MODULES = [
    "users",
]


def init_app(app):
    
    for module in ENABLED_MODULES:
        import_module(f".{module}", package=__name__).init_app(app)