from backClass import * 

#
#PREAMBLE
#

#define the seconds in a year:month:day
dayS   = 24*60*60
monthS = 30.42*dayS
yearS  = 12*monthS
#
waitDays = 5
wait  = waitDays*dayS

#
bu = backUtil(
    mountPoint = "/media/nick/backDrive/",
    backPoint  = "/home/nick/backups/",
    logPoint   = "/home/nick/backups/logs/",
    subnet     = "192.168.11",
    clientList = "client.list"
)

#
#MAIN
#

#
bu.writeOut()
while True:
    #
    for ip in bu.ipAct:
        #get hostname of ip if its in the system
        host = bu.getHostname(ip)
        Host = host.capitalize()
        #backup hostnames that appear in the client file
        if host in bu.hostUsers.keys():
            #
            user = bu.hostUsers[host] #NOTE: figure out how to handle hosts with multiple users
            User = user.capitalize()
            #
            time = cal.timegm( tm.gmtime() )
            ls = bu.lsBackup(host)

            #start with [], until we find some
            diffsDay   = []
            diffsMonth = []
            diffsYear  = []
            #first backup
            if ls==[]: bu.backProc(host, ip, time)
            else:
                #get the most recent backup time
                diffsDay   = [time-getNum(l) for l in ls if (time-getNum(l))<monthS ]
                diffsMonth = [time-getNum(l) for l in ls if (time-getNum(l))>=monthS and (time-getNum(l))<yearS ]
                diffsYear  = [time-getNum(l) for l in ls if (time-getNum(l))>=yearS ]

                #NOTE: everything below seems like it could be indented because diffsDay==[] only needs to trigger when ls==[] does not.
                if diffsDay==[]: bu.backProc(host, ip, time)
                elif min(diffsDay)>=wait: bu.backProc(host, ip, time)
                    #NOTE: maybe I'll activate this again later
                    #if name=='Chordata': saveSelf(ip, hostUsers[name], logPoint)
                    #if name=='Swc-malus-ml': saveSelf(ip, hostUsers[name], logPoint)
                    #if name=='Annas-mbp': saveSelf(ip, hostUsers[name], logPoint)
                #MANAGE YEAR
                if len(diffsYear)>=2:
                    #keep youngest 
                    minYear = min(diffsYear)
                    del diffsYear[diffsYear.index(minYear)]
                    #remove others
                    for diff in diffsYear:
                        rmTime = time-diff
                        os.system( f"rm {bu.logPoint}/{rmTime}{User}{Host}Backup.log" )
                        os.system( f"rm -r {bu.mountPoint}/{rmTime}{User}{Host}Backup.*[zg][iz]*" )
                    #
                #MANAGE MONTH
                if len(diffsMonth)>=3:
                    #keep oldest
                    maxMonth = max(diffsMonth)
                    del diffsMonth[diffsMonth.index(maxMonth)]
                    #keep youngest
                    minMonth = min(diffsMonth)
                    del diffsMonth[diffsMonth.index(minMonth)]
                    #remove others
                    for diff in diffsMonth:
                        rmTime = time-diff
                        os.system( f"rm {bu.logPoint}/{rmTime}{User}{Host}Backup.log" )
                        os.system( f"rm -r {bu.mountPoint}/{rmTime}{User}{Host}Backup.*[zg][iz]*" )
                    #
                #MANAGE DAY
                if len(diffsDay)>=3:
                    #keep oldest
                    maxDay = max(diffsDay)
                    del diffsDay[diffsDay.index(maxDay)]
                    #keep youngest
                    minDay = min(diffsDay)
                    del diffsDay[diffsDay.index(minDay)]
                    #remove others
                    for diff in diffsDay:
                        rmTime = time-diff
                        os.system( f"rm {bu.logPoint}/{rmTime}{User}{Host}Backup.log" )
                        os.system( f"rm -r {bu.mountPoint}/{rmTime}{User}{Host}Backup.*[zg][iz]*" )
                    #
                #
                #NOTE:indent would end here
            #
        #
    #
    bu.writeOut()
    time = cal.timegm( tm.gmtime() )
#

