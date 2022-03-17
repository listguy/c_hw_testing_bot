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

- explain how to run tests
- explain on soft tests
- explain how to print results
- explain how to show diffs
- explain how to reconfig another project
