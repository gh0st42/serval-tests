# serval-tests
Some small helper and benchmark scripts for serval

## Usage

* listfiles - prints the number of files in rhizome store and their names
* mesh-add-all-files - adds all files ending in ".file" to rhizome store, edit script to change file location. Used for benchmarking purposes.
* mesh-scan.sh - Triggers manual scan of local addresses, used to get serval running in core-network emulation.
* check-crash - should be run from main host, checks all serval logs for FATAL log entries
* show-log - should be run from main host, opens log of given node name in less for viewing (e.g. $ show-log n12)

