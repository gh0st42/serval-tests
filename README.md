# serval-tests
Some small helper and benchmark scripts for serval


## Architecture

* **serval-vars** - constants used by the scripts
* **serval-base** - dynamic variables and helper functions
	* as some properties are requested from serval, servald *needs* to run.


## Monitoring

### Basic scripts
The following monitoring scripts can be used to log information regarding serval *over time*.

* **meshms-monitor** - number and size of messages
* **rhizome-monitor** - files in and sizes of files in rhizome store 
* **servald-monitor** - peer count
* **net-monitor** - count and size of ip, udp, tcp packets
	* uses **netmon.py** and therefore needs python

### Monitoring daemon
The **monitor** script is able to start/stop all scripts as a daemons and takes care of the involved PIDs:

```
usage:
  monitor start     start logging of serval, rhizome, meshms and netmon
  monitor stop      stop logging
  monitor help      show this help message
```


## Simple evaluation
* **meshms-conversation-count** - shows the number of conversations
* **rhizome-listfiles** - lists number and names of files in Rhizome store



## Data manipulation
* **meshms-hello-everybody** - sends a meshms to everybody in $SEVERAL_ALL_SIDS_FILE
* **rhizome-add-testfiles** - inserts all files at $1 or $TESTFILE_PATH 


## Core network emulator helpers
* **get-sids-core** - writes SIDs from all core nodes to $SEVERAL_ALL_SIDS_FILE
* **execute-all-core** - excecutes a command on every core node and shows the output
* **daemonize-all-core** - executes and forks a command on every core node (silently)
* **show-log** - should be run from main host, opens log of given node name in less for viewing or if -n is appended just outputs the absolute log file path (e.g. $ show-log n12 )


## Other helpers
* **generate-testfiles** - generates <count> times 5 files at [output_path] or $TESTFILE_PATH
* **mesh-scan** - initiates a serval scan for all local inet addrs
* **check-crash** - should be run from main host, checks all serval logs for FATAL log entries