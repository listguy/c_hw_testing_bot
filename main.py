import os
import filecmp
import subprocess
from sys import path

path = r"C:\Users\nitza\Documents\Programming\C\c-hw\HW4\hw4q2\tests"
exe_path = r"C:\Users\nitza\Documents\Programming\C\c-hw\HW4\hw4q2\cmake-build-debug\hw4q2"
diffmerge_exe_path = r"C:\Program Files\SourceGear\Common\DiffMerge\sgdm.exe"
RUN_TEST = "r"
OPEN_IN_DIFF = "d"
EXIT = "e"
legal_cmds = [RUN_TEST, OPEN_IN_DIFF, EXIT]

def handle_outs_folder(path):
    # read project dir content
    project_dir_content = os.listdir(path)
    # filter out all folders
    folders = [folder for folder in project_dir_content if os.path.isdir(f"{path}\{folder}")]

    # create outputs folder if one doesn't exist already
    if not "outs" in folders:
        try:
            os.mkdir(path + "\outs")
            print("'outs' folder successfully created.")
        except FileExistsError as err:
            print(f"error in creating outs folder, exiting")
            print(f"ERROR: \n{err}")
    else:
        print("'outs' folder already exists, skipped creation")

def read_inputs(path):
    # read inputs
    ins = os.listdir(path + "\ins")
    return ins

def read_expected(path):
    # read expected
    expected = os.listdir(path + "\expected")
    return expected

def run_tests(path, exe, ins, expected):
    outs = []
    for input in ins:
        outs.append(input.replace('in', 'out'))
        current = outs[-1]
        os.system(f"{exe} < {path}/ins/{input} > {path}/outs./{current}")
    # check success rate
    for i,(exp, output) in enumerate(zip(expected, outs)):
        result = filecmp.cmp(f"{path}/expected/{exp}", f"{path}/outs/{output}")
        msg = "✅"
        if not result: msg = "❌"
        print(f"Test {i + 1}: {msg}")
    return outs

def get_command_from_user():
    r_input = input("🤔 ").replace(" ","")
    command = r_input[0]
    file_number = r_input[1:]
    if command not in legal_cmds:
        raise ValueError(f"'{command}' command is not recognized")
    if command != OPEN_IN_DIFF:
        return command, ""        
    if not file_number.isdigit():
        raise ValueError(f"File number should be an integer. Received '{file_number}'")
    return command, int(file_number) - 1
    
    
# read existing folders
# create outputs folder
# read inputs
# run program for each input and save input
# match output to expected and log results nice

handle_outs_folder(path)
ins = []
expected = []
outs = []

print("Hello and welcome to C-HW bot. Use the command line to operate this tool.")
while(True):
    
    try:
        action, test_to_check = get_command_from_user()
    except ValueError as err:
        print(f"🔴 {err}")
        continue
    
    if(action is EXIT):
        break

    if(action is RUN_TEST):
        ins = read_inputs(path)
        expected = read_expected(path)
        outs = run_tests(path, exe_path, ins, expected)
        continue

    if(action is OPEN_IN_DIFF):
        try:
            test_name = outs[test_to_check]
        except IndexError:
            print(f"Couldn't show diff, no test with index '{test_to_check + 1}'")
            continue
        subprocess.Popen([diffmerge_exe_path, f"-caption={test_name}", "-t1=Expected", "-t2=Received", f"{path}/expected/{test_name}", f"{path}/outs/{test_name}"])