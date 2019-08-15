import socket
import hashlib
import argparse, sys
import os
import json
import re

parser=argparse.ArgumentParser()
parser.add_argument('--config', '-c', help='Path to config file.', type= str)
parser.add_argument('--dry-run', '-d', help='Execute as dry run. Print check results and commands rather than executing commands.', action='store_true')

args=parser.parse_args()
DRY_RUN = args.dry_run

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

def checkIp(input):
    if DRY_RUN:
        print("Running IP check")

    curr = getIp()
    exp = input.replace(".", "\.").replace("*", ".*?")
    isMatch = re.search("^{0}$".format(exp), curr) is not None

    if DRY_RUN:
        print("- Got {0}, expected {1} => {2}".format(curr, input, isMatch))

    return isMatch

def getFileHash(path, hashfn):
    allowed = hashlib.algorithms
    if hashfn in allowed:
        fun = getattr(hashlib, hashfn)()
        with open(path, "rb") as f:
            for byte_block in iter(lambda: f.read(4096),b""):
                fun.update(byte_block)

            return fun.hexdigest()
    else:
        raise NameError('Not a valid algorithm: ' + hashfn)

def checkFileHash(input):
    file, expected = input.split(";", 1)
    if ";" in expected:
        method, expected = expected.split(";", 1)
    else:
        method = "sha256"
    
    if DRY_RUN:
        print("Calculating {0} of '{1}'".format(method, file))
    
    hash = getFileHash(file, method)

    if DRY_RUN:
        print("- Got {0}, expected {1} => {2}".format(hash, expected, hash == expected))

    return hash == expected

def executeScript(script):
    if DRY_RUN:
        print("Executing external check script: {0}".format(script))

    retVal = os.system(script)

    if DRY_RUN:
        print("- Got return value {0}".format(retVal))
    return retVal == 0

def runChecks(checks, handlers):
    global DRY_RUN
    checkSuccessCount = 0
    checksRun = 0

    for check in checks:
        try:
            check = check.strip()
            if not check:
                continue

            action, args = check.split(":", 1)

            if action.lower() in handlers:
                if handlers[action.lower()](args):
                    checkSuccessCount += 1
                checksRun += 1
            elif DRY_RUN:
                print("!! UNKNOWN CHECK: {0}".format(action.lower()))
        except Exception as e:
            if DRY_RUN:
                print("EXCEPTION:")
                print(e)
            continue

    return checkSuccessCount, checksRun

handlerMap = {
    "ip": checkIp,
    "hash": checkFileHash,
    "script": executeScript
}

try:
    with open(args.config, 'r') as f:
        conf = json.load(f)
        if DRY_RUN:
            print("Config:")
            print(json.dumps(conf, indent=4, sort_keys=True))

        passed, run = runChecks(conf["checks"], handlerMap)
        success = conf["minchecks"] > 0 and passed >= conf["minchecks"]

        if DRY_RUN:
            print("======")
            print("Checks run: {0}".format(run))
            print("Checks passed: {0}".format(passed))
            print("Check required: {0}".format(conf["minchecks"]))
            print("Success: {0}".format(success))
            print("======")
        
        resultingCommands = conf["success"] if success else conf["failure"]
        PY3 = sys.version_info[0] == 3
        string_types = str if PY3 else basestring
        if isinstance(resultingCommands, string_types):
            resultingCommands = [resultingCommands]

        for cmd in resultingCommands:
            if DRY_RUN:
                print("EXEC: {0}".format(cmd))
            else:
                os.system(cmd)
except Exception as e:
    if DRY_RUN:
        print("Exception")
        print(e)