# H.W Bot 🤖

A simple script to automatically run tests on your H.W and open results diffs easily

## Setup

- Make sure you have a `tests` directory
- Inside, have `ins` directory for input and `expected` directory for the expected outputs

Illustration:

```
    📁tests
    ├─ 📁expected
    │  ├─ 📄expected_output.txt
    ├─ 📁ins
    │  ├─ 📄input.txt

```

**Note**, all files should be _text_ files

## Getting Started

- Download repo code to your machine
- Open it in your favorite terminal
- run: `python main.py config`.

```
    # You will see these 3 prompts:
    📂 Please type the full path to tests directory of your project: //test directory
    🔨 Please type the full path to your project exe file: //your exe file to test
    ▶  Please type the full path to diffmerge exe file: //diffmerge exe file (will be used to show diffs)
```

- You are good to go!

## Usage

### Test

Use command `test` to run all tests on the configured project. Results will be printed at the end.

**Soft Tests:** Tests' results are saved automatically, overwriting the last results. To run tests without overwriting add the `-s` flag.

Example:

```
python main.py test
```

Example with `-s` flag:

```
python main.py test -s
```

### See Results

Use command `results` to print last tests' results.

Example:

```
python main.py results
```

### Show diffs

Use command `diff` to open diffs in [DiffMerge](https://sourcegear.com/diffmerge/) for certain tests.

Provide tests' output file names, separated by comma, for every test you want to diff. You can use `results` for help.

Example (for 3 tests):

```
python main.py diff out1.txt out2.txt out3.txt
```

### Reconfiguration

Use command `config` to run the configuration prompt again.

Useful if you've changed the project path or you want to test another project

Example

```
python main.py config
```

### Help

Use the `-h` flag to print help message in console

Example

```
python main.py -h
```
