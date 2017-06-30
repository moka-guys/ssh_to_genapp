'''
Created on 7 Jun 2017
This script is designed to be called by MOKA and run from a trust machine (using the python executable on the S drive).

The script takes an argument -g <GEL Participant ID>

It then ssh's into the server provided in the host.txt file using the username and password provided in the password and username files.

Using the path to the python executable found within the environment the python script is called, passing the GEL participant ID as an argument.

The stderr and stdout are printed.

@author: ajones7
'''
import getopt
import paramiko
import sys


class ssh_n_run():

    def __init__(self):
        # variables to connect to the server
        self.pw = ""
        self.user = ""
        self.host = ""
        self.password_file = "H:\\EclipseWorkspace\\run_gel_report_script\\password.txt"
        self.username_file = "H:\\EclipseWorkspace\\run_gel_report_script\\username.txt"
        self.host_file = "H:\\EclipseWorkspace\\run_gel_report_script\\host.txt"

        # Usage example
        self.usage = "S:\Genetics_Data2\Array\Software\Python\python.exe ssh_n_run.py -g <GELParticipantID>"

        # Gel participant id
        self.gelID = ""

        # Bash command - use the path to the python executable in the env to ensure that the
        self.bash = "~/miniconda2/envs/pyODBC/bin/python ~/Apps/CIP_API/gel_report.py -g "

    def get_credentials(self):
        '''Read in all the parameters to ssh into server'''
        # read username from file
        with open(self.username_file, 'r') as f:
            self.user = f.readline()
        # read password from file
        with open(self.password_file, 'r') as f:
            self.pw = f.readline()
        # read hostfrom file
        with open(self.host_file, 'r') as f:
            self.host = f.readline()

    def get_input(self, argv):
        '''Capture the gel participant ID from the command line'''
        # define expected inputs
        try:
            opts, args = getopt.getopt(argv, "g:")

        # raise errors with usage eg
        except getopt.GetoptError:
            print "ERROR - correct usage is", self.usage
            sys.exit(2)

        # loop through the arguments
        for opt, arg in opts:
            if opt in ("-g"):
                # capture the GEL proband ID
                self.gelID = str(arg)

    def get_into_server(self):
        # ssh client
        ssh = paramiko.SSHClient()
        # auto accept host key without prompting and requiring response from a user
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        # connect to server
        ssh.connect(self.host, username=self.user, password=self.pw)
        # send command
        stdin, stdout, stderr = ssh.exec_command(self.bash + str(self.gelID))
        # loop through and print stdout
        if stdout:
            for line in stdout:
                print line
        # loop through and print stderr
        if stderr:
            for line in stderr:
                print line

        # close connection
        ssh.close()

if __name__ == '__main__':
    go = ssh_n_run()
    go.get_input(sys.argv[1:])
    go.get_credentials()
    go.get_into_server()
