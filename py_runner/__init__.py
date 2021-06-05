import os
import subprocess
import sys
import tempfile


def run_or_exit(cmd):
    print(f'Running "{cmd}"')
    completed_process = subprocess.run(cmd, shell=True, stdout=sys.stdout, stderr=sys.stderr)
    if completed_process.returncode != 0:
        print_and_exit(completed_process.returncode)


def py_run_or_exit(cmd):
    py_path = sys.executable
    run_or_exit(f'{py_path} {cmd}')


def run_or_exit_get_output_via_tmp_file(cmd, strip=True):
    temp_file = tempfile.mktemp(suffix='.run_or_exit.tmp')

    try:
        run_or_exit(f'{cmd} > {temp_file}')
        with open(temp_file, 'r') as f:
            output = f.read()
            if strip:
                output = output.strip('\r\n \t')
            return output
    finally:
        try:
            os.remove(temp_file)
        except OSError:
            pass


def py_run_or_exit_get_output_via_tmp_file(cmd, strip=True):
    py_path = sys.executable
    return run_or_exit_get_output_via_tmp_file(f'{py_path} {cmd}', strip)


def print_and_exit(return_code):
    print("Return code " + str(return_code))
    exit(return_code)


# Shorthand for changing the cwd temporarily. Usage:
# with CWDChanger(new_dir):
#   print('Inside new dir')
# print('Back to outside dir')
class CWDChanger(object):
    def __init__(self, new_cwd):
        self.new_cwd = new_cwd

    def __enter__(self):
        self.prev_cwd = os.getcwd()
        os.chdir(self.new_cwd)

    def __exit__(self, exc_type, exc_val, exc_tb):
        os.chdir(self.prev_cwd)