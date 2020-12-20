import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SECRET_KEY = 'k7n!)*0f$wfin0%6%-x=yz_ur7qr53cg^mdt)0hj#qe+j0^s3n'
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'eoscan_db3',
        'USER': 'eoscan_admin',
        'PASSWORD': '123456789qwerty9',
        # 'HOST': 'localhost',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}
