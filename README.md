# Killscript
Script that makes sure to validate the configuration you set up.
Set up your own validation rules and run scripts if validation is successful or not.

`killscript.py` is the main file to be run.

```
usage: killscript.py [-h] [--config CONFIG] [--dry-run]

optional arguments:
  -h, --help            show this help message and exit
  --config CONFIG, -c CONFIG
                        Path to config file.
  --dry-run, -d         Execute as dry run. Print check results and commands
                        rather than executing commands.
```
 
Example 
```
python killscript.py -c config.json
```

## Config
The config file is a simple json file with an object containing 4 keys; `minchecks`, `checks`, `success` and `failure`.
 
### minchecks 
minchecks only takes one value which is the number of minimum checks to be successfully.

Example
```
minchecks:1
```

### checks
`checks` is an array of strings, each consisting of a handler, value and an optional extra values.
Handler and the arguments for the handler are separated by a colon (:).
Arguments for the handler are seperated by semicolon (;)

A handler can be one of the following:
 - ip - the local ip
 - hash - generate file hash from a file
 - script - execute a custom external script

#### ip
ip only takes one value being the expected ip (ipv4). * is supported as wildcard.

Example
```
ip:192.168.*
ip:192.168.0.*
ip:192.168.0.10
```

#### hash
hash takes two values and an optional extra values.

The first value is the file path.

The last value is the expected checksum of the file.

An optional 2nd value can be provided to set a hash algorithm. Defaults to sha256 if omitted. Any algorithm supported by [hashlib](https://docs.python.org/3/library/hashlib.html#hash-algorithms) is valid.

Example
```
file:./test.txt;md5;c946bdbebe795dad3ce5a17a6b3afc88
file:./test.txt;sha256;4e08b43ed4cb5250e5c503bb876e5180fd0dcfe1581ae488c374aa1e328e0b63
file:./test.txt;4e08b43ed4cb5250e5c503bb876e5180fd0dcfe1581ae488c374aa1e328e0b63
```

#### script
script only takes a single argument, the script to run.

The script **must** return exit code 0 for the check to pass.

Example
```
script:./custom-check.sh
```

### success
A string or array of strings consisting of commands to execute if enough checks pass to satisfy `minchecks`.

### failure
A string or array of strings consisting of commands to execute if too few checks pass to satisfy `minchecks`.

### Example config
```
{
    "minchecks": 2,
    "checks": [
        "ip:192.168.1.10",
        "ip:192.168.1.*",
        "ip:192.*.1.10",
        "hash:./test.txt;sha256;4e08b43ed4cb5250e5c503bb876e5180fd0dcfe1581ae488c374aa1e328e0b63",
        "hash:./test.txt;md5;4e08b43ed4cb5250e5c503bb876",
        "script:./custom-check.sh"
    ],
    "success": "./start-success.sh",
    "failure": [
        "./start-failure.sh",
        "shutdown -t now"
    ]
}
```