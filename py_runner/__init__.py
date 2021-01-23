import subprocess
import sys


def run_or_exit(cmd):
    completed_process = subprocess.run(cmd, shell=True, stdout=sys.stdout, stderr=sys.stderr)
    if completed_process.returncode != 0:
        print_and_exit(completed_process.returncode)


def print_and_exit(return_code):
    print("Return code " + str(return_code))
    exit(return_code)
