'''
Created on 7 Jun 2017
This script is designed to be called by MOKA and run from a trust machine (using the python executable on the S drive).
The script recieves a command to execute on the server
It then ssh's into the server using the details in the server_details.py script
A tuple containing stdout and stderr is returned.
@author: ajones7
'''
import getopt
import paramiko
import sys
import server_details as server_details

class ssh_n_run():
    def __init__(self):
        # Usage example
        self.usage = "S:\Genetics_Data2\Array\Software\Python\python.exe ssh_n_run.py -c <command>"
        # set the command to run on the server
        self.command = ""


    def get_command(self, argv):
        """Capture the gel participant ID from the command line"""
        # define expected inputs
        try:
            opts, args = getopt.getopt(argv, "c:")

        # raise errors with usage eg
        except getopt.GetoptError:
            print "ERROR - correct usage is", self.usage
            sys.exit(2)

        # loop through the arguments
        for opt, arg in opts:
            if opt in ("-c"):
                # capture the command to be executed
                self.command = str(arg)

    def execute_command(self):
        """
        This function SSH's into the server and executes the command, printing the response
        The paramiko ssh package is used to connect to the server using the user details specified in the server_details.py script
        The standard out and standard error is captured and printed
        """    
        # ssh client
        ssh = paramiko.SSHClient()
        # auto accept host key without prompting and requiring response from a user
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        # connect to server using details imported from from server_details.py
        ssh.connect(server_details.hostname, username = server_details.username, password = server_details.password)
        # send command
        stdin, stdout, stderr = ssh.exec_command(self.command)
        # Capture stderr and stdout
        stderr = stderr.read()
        stdout = stdout.read()
        # close connection
        ssh.close()
        # If there's standard error, raise exception and exit
        if stderr:
            raise Exception(stderr)
        # Print the stdout
        print stdout
        

if __name__ == '__main__':
    go = ssh_n_run()
    go.get_command(sys.argv[1:])
    go.execute_command()
