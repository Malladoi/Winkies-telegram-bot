from urllib import parse
import psycopg2
import os

parse.uses_netloc.append("postgres")
heroku_db_url = parse.urlparse(os.environ['DATABASE_URL'])

conn = psycopg2.connect(
    database=heroku_db_url.path[1:],
    user=heroku_db_url.username,
    password=heroku_db_url.password,
    host=heroku_db_url.hostname,
    port=heroku_db_url.port
)

cur = conn.cursor()

# cur.execute("""
#     CREATE TABLE vendors (
#         vendor_id SERIAL PRIMARY KEY,
#         vendor_name VARCHAR(255) NOT NULL
#     )
#     """)

cur.execute("""insert into vendors(vendor_id, vendor_name) values(1, 'Apple')""")
# test = cur.fetchall()[1]
cur.close()
# commit the changes
conn.commit()
conn.close()