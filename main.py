import argparse
from math import fabs
import os
import filecmp
import subprocess
from sys import path

# path = r"C:\Users\nitza\Documents\Programming\C\c-hw\HW4\hw4q2\tests"
# exe_path = r"C:\Users\nitza\Documents\Programming\C\c-hw\HW4\hw4q2\cmake-build-debug\hw4q2"
# diffmerge_exe_path = r"C:\Program Files\SourceGear\Common\DiffMerge\sgdm.exe"
RUN_TEST = "test"
OPEN_IN_DIFF = "diff"
CONFIG = "config"
SHOW_RESULTS = "results"
# EXIT = "e"
# legal_cmds = [RUN_TEST, OPEN_IN_DIFF, CONFIG, EXIT]
CONFIG_FILE_NAME = "config.txt"

my_parser = argparse.ArgumentParser(prog='hwbot', 
                                    description='Run tests on your HW and open results diffs easily', 
                                    epilog='Enjoy 😎')


my_parser.add_argument('command',
                        metavar='command',
                        choices=['test', 'diff', 'results', 'config'], 
                        type=str, 
                        help='action to be executed')

my_parser.add_argument('test_indexes',
                        nargs='*',
                        type=int,
                        default=0,
                        help='one or more indexes of tests to show diff for')

my_parser.add_argument('-s', '--soft', 
                        action='store_true', 
                        help='run test without overwriting last test results')

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

def handle_config_file(cwd):
    if os.path.isfile(f"{cwd}\{CONFIG_FILE_NAME}"): return
    open(f"{cwd}\{CONFIG_FILE_NAME}", "x")
    setup_config(cwd)
    
def setup_config(cwd):
    project_path = get_dir_path_input("📂 Please type the full path to tests directory of your project: ")
    exe_path = get_file_path_input("🔨 Please type the full path to your project exe file: ")
    diffmerge_exe_path = get_file_path_input("▶ Please type the full path to diffmerge exe file")

    f = open(f"{cwd}\{CONFIG_FILE_NAME}", "w")
    f.write(f"{project_path}\n{exe_path}\n{diffmerge_exe_path}")
    f.close()

def read_config(path):
    project_path, exe_path, diffmerge_path = read_file_by_lines(path)
    return project_path, exe_path, diffmerge_path

def read_file_by_lines(path):
    with open(path) as file:
        lines = [line.rstrip() for line in file]
    return lines

def get_dir_path_input(msg):
    while True:
        value = input(msg)

        if os.path.isdir(value): return value
        print_error(f"Couldn't resolve given path: '{value}'")

def get_file_path_input(msg):
    while True:
        value = input(msg)

        if os.path.isfile(value): return value
        print_error(f"Couldn't resolve given path: '{value}'")

def print_error(err):
    print(f"🔴 {err}")

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

def main():
    
    ins = []
    expected = []
    outs = []
    cwd = os.getcwd()

    try:
        print("Looks like config file is missing. Let's create one quickly:")
        handle_config_file(cwd)
        print("config file created successfully")
    except OSError as err:
        print_error(f"Encountered an error while creating config file: \n{err}\nExiting...")
    
    project_path, exe_path, diffmerge_path = read_config(f"{cwd}\{CONFIG_FILE_NAME}")

    handle_outs_folder(project_path)

    args = my_parser.parse_args()

    command = args.command
    soft_test = args.soft
    test_indexes = args.test_indexes

    if(command == RUN_TEST):
        ins = read_inputs(project_path)
        expected = read_expected(project_path)
        outs = run_tests(project_path, exe_path, ins, expected)

    if(command == CONFIG):
        setup_config(cwd)
        print("config file updated successfully")
        # project_path, exe_path, diffmerge_path = read_config(f"{cwd}\{CONFIG_FILE_NAME}")
        # handle_outs_folder(project_path)

    if(command == SHOW_RESULTS):
        print("show results")

    if(command == OPEN_IN_DIFF):
        if  not test_indexes: 
            print_error("No indexes provided.")
            return
        for index in test_indexes:
            print(index)
            # try:
            #     test_name = outs[index]
            # except IndexError:
            #     print_error(f"Couldn't show diff, no test with index '{index + 1}'")
            # subprocess.Popen([diffmerge_path, f"-caption={test_name}", "-t1=Expected", "-t2=Received", f"{project_path}/expected/{test_name}", f"{project_path}/outs/{test_name}"])
    
    # while(True):
        
    #     try:
    #         action, test_to_check = get_command_from_user()
    #     except ValueError as err:
    #         print_error(err)
    #         continue
        
    #     if(action is EXIT):
    #         break

    #     if(action is RUN_TEST):
    #         ins = read_inputs(project_path)
    #         expected = read_expected(project_path)
    #         outs = run_tests(project_path, exe_path, ins, expected)
    #         continue

    #     if(action is CONFIG):
    #         setup_config(cwd)
    #         project_path, exe_path, diffmerge_path = read_config(f"{cwd}\{CONFIG_FILE_NAME}")
    #         handle_outs_folder(project_path)


    #     if(action is OPEN_IN_DIFF):
    #         try:
    #             test_name = outs[test_to_check]
    #         except IndexError:
    #             print(f"Couldn't show diff, no test with index '{test_to_check + 1}'")
    #             continue
    #         subprocess.Popen([diffmerge_path, f"-caption={test_name}", "-t1=Expected", "-t2=Received", f"{project_path}/expected/{test_name}", f"{project_path}/outs/{test_name}"])

if __name__ == "__main__":
    main()