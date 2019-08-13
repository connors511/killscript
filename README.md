# killswitch

`killscript.py` is the main file to be run.

The script takes 3 argument (must be written in order):
 1. argument being the check-config
 2. argument being the success script to be run
 3. argument being the failutre script to be run
 
Example 
```
python killscript.py "checkConfig.txt" "echo Success" "echo Failure"
```

## Check-config
Check config is the run configuration for the script.

The way it works is that the file is read line by line (if a line is empty it is ignored).

Each line contains an action, value and an optional extra value. Action, value and the extra value are all separated with a colon (:).

An action can be one of the following:
 - minchecks - the minimum checks that needs to be validated true
 - ip - the local ip
 - file - generate file hash from a file
 
### minchecks 
minchecks only takes one value which is the number of minimum checks to be successfully.

If multiple minchecks actions are inputted only the last one will take effect.

Example
```
minchecks:1
```

### ip
ip only takes one value being the expected ip.

Example
```
ip:192.168.0.10
```

### file
file takes one value and one extra value.

The value being the file path.

The extra value being the expected file hash.

Example
```
file:./test.txt:4e08b43ed4cb5250e5c503bb876e5180fd0dcfe1581ae488c374aa1e328e0b63
```
