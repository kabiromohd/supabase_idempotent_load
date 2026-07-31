import pandas as pd
import os
import psycopg2
from dotenv import load_dotenv
from urllib.parse import quote_plus
from sqlalchemy import create_engine

load_dotenv(override=True)

# Using SQLAlchemy to create a database engine using supabase pooler host
# This resolve the issue of ipv6 on the free tier of supabase

password = quote_plus(os.getenv("PASSWORD"))

db_url = (
    f"{os.getenv('SUPABASE_DRIVER')}://"
    f"{os.getenv('USER')}:"
    f"{password}@"
    f"{os.getenv('HOST')}:{os.getenv('PORT')}/{os.getenv('DATABASE')}"
)

engine = create_engine(db_url)

df = pd.read_sql(f"SELECT * FROM public.orders", engine)

print(df)