# ssh_to_genapp v1.1
This script is designed to run a command on a remote server over SSH (using paramiko).

If there's an error when executing the remote command the STDERR will be captured and printed and the script will exit.

If there's no error, the STDOUT from the remote command is printed to terminal.

Server configuration details must be stored in a file named `server_details.py` in the same directory as the script. Use the example file included as a template.

## Usage

`ssh_n_run.py -c '<command>'`
