author = 'KSugonyakin'

import psycopg2
import os


def checkConnection(conn: psycopg2._ext.connection):
        return conn.status
    # cur = conn.cursor()

# cur.execute("""
#     CREATE TABLE vendors (
#         vendor_id SERIAL PRIMARY KEY,
#         vendor_name VARCHAR(255) NOT NULL
#     )
#     """)

#cur.execute("""insert into vendors(vendor_id, vendor_name) values(1, 'Apple')""")
# test = cur.fetchall()[1]
#cur.close()
# commit the changes
#conn.commit()
#conn.close()