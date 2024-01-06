import os
from dotenv import load_dotenv

if os.path.exists('../.env'):
    load_dotenv(dotenv_path='../.env')

try:
    PINECONE_API_KEY = os.environ['PINECONE_API_KEY']
    PINECONE_ENVIRONMENT = os.environ['PINECONE_ENVIRONMENT']
except:
    raise EnvironmentError('Necessary environment variables not found')

