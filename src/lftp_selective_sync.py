'''
Created on 28. mar. 2015

@author: GGreibesland
'''
from subprocess import Popen, PIPE, STDOUT
import datetime
import MySQLdb
import re
import sys
import shutil
import io
import time
import os


mysqlLogin = 'xbmc'
mysqlPassword = 'xbmc'
mysqlDatabase = 'xbmc_video78'
mysqlHost = 'localhost'
<<<<<<< HEAD
remote = '-i %s,%s %s' % (sys.argv[0], sys.argv[1], sys.argv[2])
remotepath = '~/private/rtorrent/data/complete451'
localpath = '/mnt/raid5/.downloads/complete'
requireMinimumImdbRating = True
minimumImdbRating = 7.0

def getImdbRating(imdb):
    br = Browser()
    link = br.open("http://www.imdb.com/title/" + imdb)
    soup = BeautifulSoup(link.read())
    #try :
    i = 0
    rating = soup.find('span',attrs={'itemprop' : 'ratingValue'}).text
    return float(rating)
=======
remoteUser = ''
remotePass = ''
remoteHost = ''
remotepath = ''
localpath = ''
lftp_parallell = 4
debug = True
logfile = 'debug.log'


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


###############################################################################

if not remoteUser or not remoteHost or not remotePass:
    remote = '-u %s,%s %s' % (sys.argv[0], sys.argv[1], sys.argv[2])
else:
    remote = '-u %s,%s %s' % (remoteUser, remotePass, remoteHost)

>>>>>>> 02942474179bdd06da8e4dca7ed8ce675711764b

def getImdbID(nfo):
    p = re.compile('tt\d{7}')  # Pattern for finding imdb id
    with open(nfo,'r') as f:
        nfoFile = ''.join(f.readlines())
    found = p.search(nfoFile)
    return found.group() if found else None


def xbmcHasMovie(imdb):
    db=MySQLdb.connect(host=mysqlHost, user=mysqlLogin, passwd=mysqlPassword, db=mysqlDatabase)
    cursor = db.cursor()
    
    query = ("SELECT COUNT(c00) from movieview WHERE c09 = '%s'") % (imdb)
    cursor.execute(query)
    
    result = cursor.fetchone()[0]
    cursor.close()
    db.close()
    logtofile('Tried %s, got: %d' % (imdb, result))
    return True if result > 0 else False


class lftpcommand:
    def __init__(self, remoteLogin, remotePath):
        self.commandList = []
        self.lftp_logfile = os.getcwd() + '/output.log'
        self.lftpsettings = 'set xfer:eta-period 5;set xfer:log true\,set xfer:log-file %s;set xfer:rate-period 20;' % (self.lftp_logfile)
        self.cmdpre = 'open %s;cd %s;' % (remoteLogin, remotePath)
        self.cmdpre += self.lftpsettings
        self.cmdpost = ''

    def add(self, command):
        self.commandList.append(command)
        
    def get(self):
        return self.cmdpre + ';'.join(self.commandList) + self.cmdpost
    
    def clear(self):
        self.commandList = []

    def getLogFile(self):
        return self.lftp_logfile


def runLftp(lftpcmd, watch=False):
    lrun = ['lftp', '-c', lftpcmd.get()]
    process = Popen(lrun, stdout=PIPE)
    if watch:
        logf = lftpcmd.getLogFile()
        while process.poll() is None:
            print file(logf, "r").readlines()[-1]
            time.sleep(2)
    return Popen(lrun, stdout=PIPE).communicate()[0]


def getRemoteNfoList(remote=remote,remotepath=remotepath):
    cleanTemp()
    commands = lftpcommand(remote, remotepath)
    commands.add('find | grep nfo')

    mirrorFileList = runLftp(commands)
    #print mirrorFileList
    commands.clear()
    commands.add('lcd temp')
    for line in mirrorFileList.split('\n'):
        if line != '':
            commands.add('mget -d %s' % (line))
    #print commands
    runLftp(commands)
    return mirrorFileList.split('\n')


def getMoviesToFetch(nfos):
# Now we have a replicated directory structure with only the nfo files.
# Loop through nfo files, find imdb id
    mirrordirs = []
    for nfo in nfos:
<<<<<<< HEAD
        dir = '/'.join(nfo.split('/')[:-1])
        file = nfo[-1]
        imdb = getImdbID(nfo)
        xbmc = xbmcHasMovie(imdb)
        if imdb and not xbmc:
            if requireMinimumImdbrating and getImdbRating(imdb) >= minimumImdbRating:
                mirrordirs.append(dir)
        return mirrordirs
=======
        if nfo != '':
            dir = '/'.join(nfo.split('/')[:-1])
            file = nfo[-1]
            imdb = getImdbID(nfo.replace('./', './temp/'))
            logtofile('NFO File: ' + nfo + ', imdb id: ' + imdb)
            xbmc = xbmcHasMovie(imdb)
            if imdb and not xbmc:
                mirrordirs.append(dir)
    return mirrordirs
>>>>>>> 02942474179bdd06da8e4dca7ed8ce675711764b


def fetchMovies(directories):
    commands = lftpcommand(remote, remotepath)
    commands.add('lcd %s' % (localpath))
    commands.add('pwd')
    for d in directories:
        commands.add('mirror -c -P%i %s' % (lftp_parallell, d))
    # Download
    logtofile('Running with commands: ' + commands.get())
    runLftp(commands)


<<<<<<< HEAD
if __name__ == "__main__":
    print sys.argv
=======
def cleanTemp():
    tempdir = os.getcwd() + '/temp'
    if os.path.exists(tempdir):
        shutil.rmtree(tempdir)
    if not os.path.exists(tempdir):
        os.makedirs(tempdir)


def run_selective_sync():
>>>>>>> 02942474179bdd06da8e4dca7ed8ce675711764b
    nfoFiles = getRemoteNfoList()
    logtofile('NFO Files: ')
    logtofile(nfoFiles)
    downMovies = getMoviesToFetch(nfoFiles)
<<<<<<< HEAD
    fetchMovies(downMovies)
=======
    logtofile('Folders to download:')
    logtofile(downMovies)
    fetchMovies(downMovies)


if __name__ == "__main__":
    run_selective_sync()

>>>>>>> 02942474179bdd06da8e4dca7ed8ce675711764b
