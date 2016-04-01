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
* **pidstat-monitor** - tracks pidstat info of servald
* **meshms-insertion-monitor** - follows serval.log and creates csv dump for meshms insertions
* ... (more to come)

### Monitoring daemon
The **monitor** script is able to start/stop all scripts as a daemons and takes care of the involved PIDs:

```
usage:
  monitor system    start logging of system related services (netmon, pidstat, ...)
  monitor serval    start logging of serval related services (rhizome, meshms, ...)
  monitor stop      stop logging
  monitor help      show this help message
```


## Simple evaluation
* **meshms-conversation-count** - shows the number of conversations
* **rhizome-listfiles** - lists number and names of files in Rhizome store



## Data manipulation
* **meshms-hello-everybody** - sends a meshms to everybody in $SEVERAL\_ALL\_SIDS\_FILE
* **rhizome-add-testfiles** - inserts all files at $1 or $TESTFILE\_PATH
* **SimpleMeshUser.py** - send MeshMS messages periodically
* **SimpleRhizomeAdder.py** - insert periodically files to rhizome store
* **DirectRhizomeAdder.py** - send files periodically



## Other helpers
* **generate-testfiles** - generates <count> times 5 files at [output\_path] or $TESTFILE\_PATH
* **mesh-scan** - initiates a serval scan for all local inet addrs
