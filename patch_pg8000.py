# monkey_patch_pg8000.py
import pg8000.native
import sys

# Patch minimal pour tromper Django
class FakePsycopg2:
    def __init__(self):
        self.extensions = type('extensions', (), {})()

sys.modules['psycopg2'] = FakePsycopg2()
sys.modules['psycopg2.extensions'] = type('extensions', (), {})()