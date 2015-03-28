'''
Created on 28. mar. 2015

@author: GGreibesland
'''
from subprocess import Popen, PIPE, STDOUT
import datetime
import MySQLdb
import re
import sys
# mirror
#login = '{0}ftp://{1} {2}'.format(args.secure, args.site, port),
#                 'user {0}'.format(user)
mysqlLogin = 'xbmc'
mysqlPassword = 'xbmc'
mysqlDatabase = 'xbmc_video78'
mysqlHost = 'localhost'
remote = '-i %s,%s %s' % (sys.argv[0], sys.argv[1], sys.argv[2])
remotepath = '~/private/rtorrent/data/complete451'
localpath = '/mnt/raid5/.downloads/complete'


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
    return True if result > 0 else False


class lftpcommand:
    def __init(self, remoteLogin, remotePath):
        self.commandList = []

        self.cmdpre = """<< EOF
        open %s
        cd %s
        """ % (remoteLogin, remotePath)

        self.cmdpost = """
        exit
        EOF"""

    def add(self, command):
        self.commandList.add(command)
        
    def get(self):
        return self.cmdpre + '\n'.join(self.commandList) + self.cmdpost
    
    def clear(self):
        self.commandList = []

def runLftp(cmdscript):
    return Popen(['lftp', cmdscript], stdout=PIPE).communicate()[0]


def getRemoteNfoList():
    commands = lftpcommand(remote, remotepath)
    commands.add('find | grep nfo')

    mirrorFileList = runLftp(commands.get())
    print mirrorFileList
    commands.clear()
    commands.add('lcd temp')
    for line in mirrorFileList.split('\n'):
        if line != '':
            commands.add('mget -d %s' % (line))
    print commands
    runLftp(commands.get())
    return mirrorFileList.split('\n')


def getMoviesToFetch(nfos):
# Now we have a replicated directory structure with only the nfo files.
# Loop through nfo files, find imdb id
    mirrordirs = []
    for nfo in nfos:
        dir = '/'.join(nfo.split('/')[:-1])
        file = nfo[-1]
        imdb = getImdbID(nfo)
        xbmc = xbmcHasMovie(imdb)
        if imdb and not xbmc:
            mirrordirs.append(dir)
        return mirrordirs


def fetchMovies(directories):
    commands = lftpcommand(remote, remotepath)
    commands.add('lcd %s' % (localpath))
    for d in directories:
        commands.add(d)
    # Download
    runLftp(commands.get())


if __name__ == "__main__":
    nfoFiles = getRemoteNfoList()
    downMovies = getMoviesToFetch(nfoFiles)
    fetchMovies(downMovies)