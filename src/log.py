import datetime
import io
import time

def logtofile(msg):
    if debug:
        timestamp = time.time()
        humanreadable = datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
        try:
            f = open(logfile,'a')
            f.write(str(humanreadable) + ' ' + str(msg) + '\n')
            f.close()
        except IOError:
            print 'IO error occured. Unable to write to log.'
