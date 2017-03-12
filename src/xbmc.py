import MySQLdb
from log import Logger

logger = Logger('debug', 'debug.txt')

def xbmcHasMovie(imdb, mysqlHost, mysqlLogin, mysqlPassword, mysqlDatabase):
    db=MySQLdb.connect(host=mysqlHost, user=mysqlLogin, passwd=mysqlPassword, db=mysqlDatabase)
    cursor = db.cursor()
    
    query = ("SELECT COUNT(c00) from movie_view WHERE c09 = '%s'") % (imdb)
    cursor.execute(query)
    
    result = cursor.fetchone()[0]
    cursor.close()
    db.close()
    logger.debug('Tried %s, got: %d' % (imdb, result))
    return True if result > 0 else False
