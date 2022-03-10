import os
import filecmp

path = r"C:\Users\nitza\Documents\Programming\C\c-hw\HW4\hw4q2\tests"
exe_path = r"C:\Users\nitza\Documents\Programming\C\c-hw\HW4\hw4q2\cmake-build-debug\hw4q2"
# read existing folders
# create outputs folder
# read inputs
# run program for each input and save input
# match output to expected and log results nice

# read project dir content
project_dir_content = os.listdir(path)
# path_project_dir_content = [os.path.join(path, doc) for doc in dir_content]
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

# read inputs
ins = os.listdir(path + "\ins")
outs = []
for i,input in enumerate(ins):
    outs.append(input.replace('in', 'out'))
    current = outs[-1]
    os.system(f"{exe_path} < {path}/ins/{input} > {path}/outs./{current}")
# check success rate
expected = os.listdir(path + "\expected")
for i,(exp, output) in enumerate(zip(expected, outs)):
    result = filecmp.cmp(f"{path}/expected/{exp}", f"{path}/outs/{output}")
    msg = "✅"
    if not result: msg = "❌"
    print(f"Test {i + 1}: {msg}")
