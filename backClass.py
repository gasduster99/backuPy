import os
import glob
import humanize
import subprocess
import time as tm
import calendar as cal

#
class backUtil():
    #
    def __init__(self, 
            mountPoint="/media/nick/backDrive/",
            backPoint="/home/nick/backups/",
            logPoint="/home/nick/backups/logs/",
            subnet="192.168.11", 
            clientList="client.list"
            ):
        #give declared values to self
        self.mountPoint = mountPoint
        self.backPoint  = backPoint
        self.logPoint   = logPoint
        self.subnet     = subnet
        
        #NOTE: make sure that this dictionary/file are structured to accept multiple users per host
        self.hostUsers = dict( userHost.strip().replace(' ', '').split(';') for userHost in open(clientList) )
        self.ipAct = ["%s.%d"%(subnet, i) for i in range(256)]
    #
    
    #
    def lsBackup(self, name):
        #
        User = self.hostUsers[name].capitalize()
        Name = name.capitalize()
        #
        return( glob.glob(f"{self.mountPoint}*{User}{Name}Backup.*[gz][zi]*") )
        
    #

    #
    def writeOut(self):
        #
        minS = 60
        hrS = 60*minS
        dayS = 24*hrS
        #
        time = cal.timegm( tm.gmtime() )
        #
        os.system('clear')
        for name in self.hostUsers:
                #
                print(f"{name}:")
                ls = self.lsBackup(name)
                for l in sorted(ls):
                        dif = time - getNum(l)
                        days = dif // dayS
                        #
                        diff = dif-(days*dayS)
                        hrs = diff // hrS
                        #
                        difff = diff-(hrs*hrS)
                        mins = difff // minS
                        #
                        diffff = difff-(mins*minS)
                        s = diffff #// S
                        #
                        lInfo = os.stat(l)
                        lSize = humanize.naturalsize(lInfo.st_size, gnu=True)
                        # 
                        print(l)
                        print( f"\tD:H:M.S: {days}:{hrs}:{mins}.{s}" ) 
                        print( f"\tSize: {lSize}" )
                        print('')
                #
        print('')
        #
    #

    #
    def getHostname(self, ip):
        #
        hostnames = self.hostUsers.keys()
        for name in hostnames:
            #
            user = self.hostUsers[name]
            pipe = subprocess.Popen( ["expect", "sshHostname.exp", f"{user}@{ip}"],  #%(hostUsers[name], ip)],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            #import pdb; pdb.set_trace()
            hostStr = pipe.communicate()[0].decode().split('\r\n')[1]
            outStr  = hostStr.strip().split('.')[0].capitalize()
            #
            if name==outStr: break
        #
        if not any([outStr==h for h in hostnames]): outStr=''
        #
        return( outStr )
    #

    #def exclude

    #
    def backProc(self, host, ip, time): #host, user, time, ip, mp, lp, bp):
        '''
        use ssh to:
            -notify that the backup is beginning
            -remove unneccecary stuff before backup
            -rsync to sync the client home directory to the server client share
        then archive the synced server client share to a external drive at "mountPoint"
        finally use ssh to notify that the backup is complete
        '''

        #
        Host = host.capitalize()
        user = self.hostUsers[host] #NOTE: add a loop over users to handle hosts with multiple users
        User = user.capitalize()

        #
        print( f"{user}{Host} Backup in Progress" )
        print( "\tStart Sync..." )

        #import pdb; pdb.set_trace()
        homeDir = subprocess.check_output( f"ssh {user}@{ip} pwd", shell=True).strip()
        os.system( f"ssh {user}@{ip} bash -l {homeDir}/Documents/programs/backupSys/start.sh & >> {self.logPoint}/{time}{User}{Host}Backup.log 2>&1" )
        os.system('rsync -avz '
            '--exclude ".cache" '
            '--exclude ".config/teamveiwer*" '
            '--exclude ".wine" '
            '--exclude "extra" '
            '--exclude "Dropbox" '
            '--exclude "Creative Cloud Files" '
            '--exclude ".mozilla" '
            '--exclude "*/.git/*" '
            '--exclude "VirtualBox VMs" '
            '--exclude "Library" '
            '--exclude ".Trash" '
            '--exclude "Parallels" '
            '--delete-delay '
            '--delete-excluded '
            f"{user}@{ip}:{homeDir}/ {self.backPoint}/{user}{Host}/ >> {self.logPoint}/{time}{User}{Host}Backup.log 2>&1"
        )
        print("\tStop Sync...")
        os.system( f"ssh {user}@{ip} bash -l {homeDir}/Documents/programs/backupSys/stop.sh & >> {self.logPoint}/{time}{User}{Host}Backup.log 2>&1" )
        #
        print("\tArchive...")
        self.archive(host, time)
    #

    #
    def archive(self, host, time):
        #
        Host = host.capitalize()
        user = self.hostUsers[host] #NOTE: add a loop over users to handle hosts with multiple users
        User = user.capitalize()

        #NOTE: A host of options for various platforms that I have tried. Figure it out on you platform. 
        #Add something that works for you and send a pull request if you want. Maybe one day I will get 
        #together enough solutions here to maybe make the program automagically figure its shit out here.
        
        #os.system('zip -r %s%d%s%sBackup %s%s%s >> %s%d%s%sBackup.log 2>&1' % (mp, time, user.capitalize(), host.capitalize(), bp, user.lower(), host.capitalize(), lp, time, user.capitalize(), host.capitalize()))
        os.system('tar -I pigz -cf {self.mountPoint}/{time}{User}{Host}Backup.tar.gz {self.backPoint}{user}{Host} >> {self.logPoint}/{time}{User}{Host}Backup.log 2>&1')
        #os.system('tar --use-compress-program="pigz -k -p 1" -cf %s%d%s%sBackup.tar.gz %s%s%s >> %s%d%s%sBackup.log 2>&1' % (mp, time, user.capitalize(), host.capitalize(), bp, user.lower(), host.capitalize(), lp, time, user.capitalize(), host.capitalize()))
        #https://unix.stackexchange.com/questions/57719/how-do-i-resume-a-tar-command-which-was-killed
    #
#

#
def getNum(lsEntry):
    #
    numLetter = lsEntry.rpartition('/')[2]
    filInt = filter(lambda x: x.isdigit(), numLetter)
    strInt = "".join(filInt)
    return( int(strInt) )
#

##
##TIME PREAMBLE
##
#
##
#waitDays = 5
##define the seconds in a year:month:day
#dayS   = 24*60*60
#monthS = 30.42*dayS
#yearS  = 12*monthS
##
#time  = cal.timegm( tm.gmtime() )
#wait  = waitDays*dayS
#
##
##MAIN
##
#
##
#bu = backUtil()
#bu.writeOut()

##
#while True:
#    #
#    for ip in bu.ipAct:
#        #get hostname of ip if its in the system
#        host = bu.getHostname(ip)
#        Host = host.capitalize() 
#        #backup hostnames that appear in the client file
#        if host in bu.hostUsers.keys():
#            #
#            user = bu.hostUsers[host] #NOTE: figure out how to handle hosts with multiple users
#            User = user.capitalize()
#            #
#            time = cal.timegm( tm.gmtime() )
#            ls = bu.lsBackup(host)
#
#            #start with [], until we find some
#            diffsDay   = []
#            diffsMonth = []
#            diffsYear  = []
#            #first backup
#            if ls==[]: bu.backProc(host, ip, time)
#            else: 
#                #get the most recent backup time
#                diffsDay   = [time-getNum(l) for l in ls if (time-getNum(l))<monthS ]
#                diffsMonth = [time-getNum(l) for l in ls if (time-getNum(l))>=monthS and (time-getNum(l))<yearS ]
#                diffsYear  = [time-getNum(l) for l in ls if (time-getNum(l))>=yearS ]
#
#                #NOTE: everything below seems like it could be indented because diffsDay==[] only needs to trigger when ls==[] does not.
#                if diffsDay==[]: bu.backProc(host, ip, time)
#                elif min(diffsDay)>=wait: bu.backProc(host, ip, time)
#                    #NOTE: maybe I'll activate this again later
#                    #if name=='Chordata': saveSelf(ip, hostUsers[name], logPoint)
#                    #if name=='Swc-malus-ml': saveSelf(ip, hostUsers[name], logPoint)
#                    #if name=='Annas-mbp': saveSelf(ip, hostUsers[name], logPoint)
#                #MANAGE YEAR
#                if len(diffsYear)>=2:
#                    #keep youngest 
#                    minYear = min(diffsYear) 
#                    del diffsYear[diffsYear.index(minYear)]
#                    #remove others
#                    for diff in diffsYear:
#                        rmTime = time-diff
#                        os.system( f"rm {bu.logPoint}/{rmTime}{User}{Host}Backup.log" )
#                        os.system( f"rm -r {bu.mountPoint}/{rmTime}{User}{Host}Backup.*[zg][iz]*" )
#                    #
#                #MANAGE MONTH
#                if len(diffsMonth)>=3:
#                    #keep oldest
#                    maxMonth = max(diffsMonth)
#                    del diffsMonth[diffsMonth.index(maxMonth)]
#                    #keep youngest
#                    minMonth = min(diffsMonth) 
#                    del diffsMonth[diffsMonth.index(minMonth)]
#                    #remove others
#                    for diff in diffsMonth:
#                        rmTime = time-diff
#                        os.system( f"rm {bu.logPoint}/{rmTime}{User}{Host}Backup.log" )
#                        os.system( f"rm -r {bu.mountPoint}/{rmTime}{User}{Host}Backup.*[zg][iz]*" )
#                    #
#                #MANAGE DAY
#                if len(diffsDay)>=3:
#                    #keep oldest
#                    maxDay = max(diffsDay)
#                    del diffsDay[diffsDay.index(maxDay)]
#                    #keep youngest
#                    minDay = min(diffsDay)
#                    del diffsDay[diffsDay.index(minDay)]
#                    #remove others
#                    for diff in diffsDay:
#                        rmTime = time-diff
#                        os.system( f"rm {bu.logPoint}/{rmTime}{User}{Host}Backup.log" )
#                        os.system( f"rm -r {bu.mountPoint}/{rmTime}{User}{Host}Backup.*[zg][iz]*" )
#                    #
#                #
#                #NOTE:indent would end here
#            #
#        #
#    #
#    bu.writeOut()
#    time = cal.timegm( tm.gmtime() )
##



