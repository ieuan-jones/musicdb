import musicdb.db
import csvreader

conn = connect_db()
initialise_db(conn)

with open('moosic.csv', 'r') as f:
    pass

close_db(conn)
