import redis
import socket

HOST = '127.0.0.1'
PORT = 8088


def isFloatAndPositive(value):
    try:
        float(value)
        if float(value)>0:
            return True
        else:
            return False
    except ValueError:
        return False



def createAccount(redisDB, cmd):
    ''' 
        0: success
        1: account is already exisits
        3: money is not non-negative number
        4: too few arguments
        5: too more arguments
    '''
    if len(cmd)<3:
        return 4
    elif len(cmd)>3:
        return 5
    else:
        if not cmd[2].isdigit():
            return 3
        if redisDB.exists(cmd[1]):
            return 1
        else:
            money = int(cmd[2])
            account = cmd[1]
            redisDB.set(account, money)
            return 0


def saveMoney(redisDB, cmd):
    '''
        0: success
        2: account is not exisited
        3: money is not non-negative number
        4: too few arguments
        5: too more arguments
    '''
    if len(cmd)<3:
        return 4
    elif len(cmd)>3:
        return 5
    else:
        if not cmd[2].isdigit():
            return 3
        if redisDB.exists(cmd[1]):
            account = cmd[1]
            money = int(cmd[2])
            deposits = int(redisDB.get(account))
            newDeposits = deposits + money
            redisDB.set(account, newDeposits)
            return 0
        else:
            return 2

def loadMoney(redisDB, cmd):
    '''
        0: success
        2: account is not exisited
        3: money is not non-negative number
        4: too few argument
        5: too more argument
        6: deposits is not enough
    '''
    if len(cmd)<3:
        return 4
    elif len(cmd)>3:
        return 5
    else:
        if not cmd[2].isdigit():
            return 3
        if redisDB.exists(cmd[1]):
            account = cmd[1]
            money = int(cmd[2])
            deposits = int(redisDB.get(account))
            if deposits >= money:
                newDeposits = deposits - money
                redisDB.set(account, newDeposits)
                return 0
            else:
                return 6
        else:
            return 2

def remitMoney(redisDB, cmd):
    '''
        0: success
        7: source account is not existed
        8: destination account is not existed
        3: money is not non-negative number
        4: too few arguments
        5: too more augrments
        6: deposits is not enough
    '''
    if len(cmd)<4:
        return 4
    elif len(cmd)>4:
        return 5
    else:
        if cmd[3].isdigit():
            s_account = cmd[1]
            d_account = cmd[2]
            money = int(cmd[3])
            if not redisDB.exists(s_account):
                return 7
            if not redisDB.exists(d_account):
                return 8
            source = int(redisDB.get(s_account))
            dest = int(redisDB.get(d_account))
            if source >= money:
                newSource = source - money
                newDest = dest + money
                redisDB.set(s_account, newSource)
                redisDB.set(d_account, newDest)
                return 0
            else:
                return 6
        else:
            return 3

def end(redisDB, cmd):
    if len(cmd)>1:
        return 5
    else:
        return 100

cmdList = {'init':createAccount, 'save':saveMoney,
            'load':loadMoney, 'remit':remitMoney, 'end':end}

resList = {'0': " ",
        '1': " // error for registered account",
        '2': " // error for unregistered account",
        '3': " // error for not non-negative money",
        '4': " // error for too few arguments",
        '5': " // error for too more arguments",
        '6': " // error for not have enough money",
        '7': " // error for unregistered account",
        '8': " // error for unregistered account",
        }

def leave(redisDB, connection, inputCmd):
    connection.send("\n// input\n".encode('utf-8'))
    for msg in inputCmd:
        msg = msg+"\n"
        connection.send(msg.encode('utf-8'))
    connection.send("\n// output\n".encode('utf-8'))
    for key in redisDB.scan_iter():
        msg = str(key)+" : "+redisDB.get(key)+ "\n"
        connection.sendall(msg.encode('utf-8'))

def session(connection, redisDB):
    inputCmd = []
    cmdCount = 0
    successCount = 0
    while True:
        cmd = []
        request = connection.recv(1024)
        data = request.decode('utf-8')
        l_data = data.lower()
        cmd = l_data.split()
        if len(cmd) == 0:
            continue
        if cmd[0] in cmdList:
            res = cmdList[cmd[0]](redisDB,cmd)
            if res == 0:
                msg = data + " OK"
                inputCmd.append(data)
                successCount = successCount + 1
            elif res == 100:
                inputCmd.append(data)
                leave(redisDB, connection, inputCmd)
                break
            elif res == 7 or res == 2:
                msg = data+resList['7']+" '"+cmd[1]+"'"
                inputCmd.append(data+resList['7']+" '"+cmd[1]+"'")
            elif res == 8:
                msg = data+resList['8']+" '"+cmd[2]+"'"
                inputCmd(data+resList['8']+" '"+cmd[2]+"'")
            else:
                msg = data+resList[str(res)]
                inputCmd.append(data+resList[str(res)])
            cmdCount = cmdCount + 1
        else:
            msg = "No command '"+data+"' found"
        connection.send(msg.encode('utf-8'))
    msg = "\nsuccess rate : ("+str(successCount) + "/"+ str(cmdCount)+")"
    connection.send(msg.encode('utf-8'))

def Main():
    redisDB = redis.Redis(host='10.0.2.5', port=6379, decode_responses=True)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((HOST, PORT))
    sock.listen(5)
    while True:
        try:
            connection,address=sock.accept()
            session(connection,redisDB)
            connection.close()
        except:
            break
    sock.close()


if __name__ == '__main__' :
    Main()

