import argparse
import os
import filecmp
import json
import subprocess
from sys import path

RUN_TEST = "test"
OPEN_IN_DIFF = "diff"
CONFIG = "config"
SHOW_RESULTS = "results"
CONFIG_FILE_NAME = "config.txt"
RESULTS_FILE_NAME = "results.txt"

# region Parser
my_parser = argparse.ArgumentParser(prog='hwbot', 
                                    description='Run tests on your HW and open results diffs easily', 
                                    epilog='Enjoy 😎')

my_parser.add_argument('command',
                        metavar='command',
                        choices=['test', 'diff', 'results', 'config'], 
                        type=str, 
                        help='action to be executed')

my_parser.add_argument('tests',
                        nargs='*',
                        type=str,
                        default="",
                        help='one or more file names of tests to show diff for')

my_parser.add_argument('-s', '--soft', 
                        action='store_true', 
                        help='run test without overwriting last test results')

# endregion

# region helpers
def handle_outs_folder(path):
    # read project dir content
    project_dir_content = os.listdir(path)
    # filter out all folders
    folders = [folder for folder in project_dir_content if os.path.isdir(f"{path}\{folder}")]

    # create outputs folder if one doesn't exist already
    if not "outs" in folders:
        try:
            os.mkdir(path + "\outs")
        except FileExistsError as err:
            print_error(f"error in creating outs folder:\n{err}\nExiting...")

def handle_config_file(path):
    if os.path.isfile(path): return
    open(path, "x")
    setup_config(path)
    
def setup_config(path):
    # project_path = get_dir_path_input("📂 Please type the full path to tests directory of your project: ")
    # exe_path = get_file_path_input("🔨 Please type the full path to your project exe file: ")
    # diffmerge_exe_path = get_file_path_input("▶ Please type the full path to diffmerge exe file")

    config_data = {
        "project_path": get_dir_path_input("📂 Please type the full path to tests directory of your project: "),
        "exe_path": get_file_path_input("🔨 Please type the full path to your project exe file: "),
        "diffmerge_exe_path": get_file_path_input("▶ Please type the full path to diffmerge exe file")
    }
    write_to_json_file(path, config_data)

def create_results_file(path):
    if os.path.isfile(path): return
    open(path, "x")

def read_json_file(path):
    f = open(path)
    try:
        content = json.load(f)
        f.close
        return content
    except json.JSONDecodeError:
        pass
    return None
    
def write_to_json_file(path, content):
    f = open(path, "w")
    json.dump(content, f)
    f.close()

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
    results = {}
    for input in ins:
        current = input.replace('in', 'out')
        results[current] = False
        os.system(f"{exe} < {path}/ins/{input} > {path}/outs./{current}")
    # check success rate
    for i,(exp, output) in enumerate(zip(expected, results.keys())):
        result = filecmp.cmp(f"{path}/expected/{exp}", f"{path}/outs/{output}")
        results[output] = result
    return results

def print_results(results):
    for i,(test, result) in enumerate(results.items()):
        msg = "✅" if result else "❌"
        print(f"{test}: {msg}")
# endregion

def main():
    cwd = os.getcwd()
    config_path = f"{cwd}\{CONFIG_FILE_NAME}"
    results_path = f"{cwd}\{RESULTS_FILE_NAME}"

    # create config file
    try:
        print("Looks like config file is missing. Let's create one quickly:")
        handle_config_file(config_path)
        print("config file created successfully")
    except OSError as err:
        print_error(f"Encountered an error while creating config file: \n{err}\nExiting...")

    # create results file
    try:
        create_results_file(results_path)
    except OSError as err:
        print_error(f"Encountered an error while creating results file: \n{err}\nExiting...")
    
    config_data = read_json_file(config_path)
    if not config_data:
        print_error("Corrupted config data. Reconfiging:")
        setup_config(config_path)
        print("config file updated successfully")
        config_data = read_json_file(config_path)
        

    handle_outs_folder(config_data["project_path"])

    args = my_parser.parse_args()

    command = args.command
    soft_test = args.soft
    files_to_diff = args.tests

    if(command == RUN_TEST):
        ins = read_inputs(config_data.get("project_path"))
        expected = read_expected(config_data.get("project_path"))
        results = run_tests(config_data.get("project_path"), config_data.get("exe_path"), ins, expected)
        print_results(results)
        if(soft_test): return
        write_to_json_file(results_path, results)

    if(command == CONFIG):
        setup_config(config_path)
        print("config file updated successfully")

    if(command == SHOW_RESULTS):
        results = read_json_file(results_path)
        if not results: 
            print_error("No results to show")
            return
        print_results(results)

    if(command == OPEN_IN_DIFF):
        if  not files_to_diff: 
            print_error("No indexes provided.")
            return
        diff_exe = config_data.get("diffmerge_exe_path")
        if not diff_exe: print_error("diffmerge exe path missing. try re-configing. Exiting...")
        project_path = config_data.get("project_path")
        if not project_path: print_error("project path missing. try re-configing. Exiting...")
        for file in files_to_diff:
            subprocess.Popen([diff_exe, f"-caption={file}", "-t1=Expected", "-t2=Received", f"{project_path}/expected/{file}", f"{project_path}/outs/{file}"])
    
if __name__ == "__main__":
    main()