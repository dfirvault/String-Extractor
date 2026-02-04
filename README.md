# String-Extractor
Extract ASCII strings for all files and recreate folder structure with the converted strings.

## Features
Folder Picker Interface: Native Windows folder selection dialog

Preserves Structure: Replicates original folder hierarchy in output

Smart Naming: Output files keep original names with .txt extension added (e.g., file.xml → file.xml.txt)

Multiple Encoding Support: Handles UTF-8, Latin-1, CP1252, ISO-8859-1 encodings

User Options: Choose to skip or overwrite existing files

Progress Reporting: Shows file sizes and processing status

Safe Operation: Original files are never modified

## Installation
### Requirements
Python 3.6 or higher

Tkinter (usually included with Python on Windows)

### Run from Source
Download the script: ascii_extractor.py

Install Python if not already installed

Run the script:
```
python ascii_extractor.py
```
## Usage

### Main Menu Options:

Option 1: Extract ASCII text from files

Option 2: View detailed instructions

Option 3: Exit program

When extracting text:

Select source folder using the folder picker

Choose output folder (default or custom)

Select whether to skip or overwrite existing files

Confirm to start processing

### Output Convention
The program adds .txt to the original filename:

Original File	Output File
document.pdf	document.pdf.txt
data.xml	data.xml.txt
script.py	script.py.txt
report.docx	report.docx.txt
What Gets Extracted
Kept: ASCII characters (codes 32-127), newlines, tabs, carriage returns

Removed: Non-ASCII characters, emojis, special symbols (©, ®, ™), control characters

### Examples
Processing a Folder
text
Source Folder/
├── documents/
│   ├── report.pdf
│   └── data.xml
└── images/
    └── notes.txt

Output Folder/
├── documents/
│   ├── report.pdf.txt
│   └── data.xml.txt
└── images/
    └── notes.txt.txt
