import socket
import hashlib
import sys
import os

def getIp():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    result = ""

    try:
        s.connect(("10.255.255.255", 1))
        result = s.getsockname()[0]
    except:
        result = "127.0.0.1"
    finally:
        s.close()

    return result

def getFileHash(path):
    sha256_hash = hashlib.sha256()
    with open(path, "rb") as f:
        for byte_block in iter(lambda: f.read(4096),b""):
            sha256_hash.update(byte_block)

        return sha256_hash.hexdigest()

def check(path):
    minChecks = 0
    checkSuccessCount = 0

    with open(path, "r") as f:
        for line in f:
            try:
                line = line.strip()
                if not line:
                    continue

                split = line.split(":")
                action = split[0].lower()
                if (action == "minchecks"):
                    try:
                        minChecks = int(split[1])
                    except:
                        minChecks = 0

                elif (action == "ip"):
                    currentIp = getIp().lower()
                    expectedIp = split[1].lower()
                    if (currentIp == expectedIp):
                        checkSuccessCount += 1

                elif (action == "disk"):
                    currentFileHash = getFileHash(split[1]).lower()
                    expectedFileHash = split[2].lower()
                    if (currentFileHash == expectedFileHash):
                        checkSuccessCount += 1
            except:
                continue

    return minChecks > 0 and checkSuccessCount >= minChecks

checkPath = sys.argv[1]

checkStatus = False
try:
    checkStatus = check(checkPath)
except:
    checkStatus = False


if checkStatus:
    mountCommand = sys.argv[2]
    os.system(mountCommand)
else:
    failureCommand = sys.argv[3]
    os.system(failureCommand)
