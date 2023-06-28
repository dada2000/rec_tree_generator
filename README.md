# RECURSIVE TREE GENERATOR -> GRAPHICAL OUTPUT IN CLI:

## USING: pathlib, argparse, relative module imports, indirect recursive implementation
### GENERAL:
**High level steps:**
1. Provide starting directory(relative or absolute) and optional attributes (directory only, output_file) in CLI using "Argparse".
2. Program iterates (indirect recursion) through all files and folders using "pathlib" and stores them as <str> in list structure.
3. Resulting tree (files, folders) can either be printed in CLI(default) or into specified file path.

### BACKGROUND DETAILS:
**Main application functionalities:**
* Iterates provided rel. or abs. root directory and constructs list recursively of all files/directories inside root_dir.
* Displays visual tree representation from constructed element list with indents and file counts preview.
* **High level Class**: DirectoryTree class (.generate()) --> Generates and displays tree diagram --> Either into specified file or CLI.
* **Low level Class**: _TreeGenerator(.build_tree()) --> Iterates entire tree structure recursively --> Creates list (self._tree) with file/directory entries
* Tree diagram(list) consists of 2 main components: HEAD(root directory[name and "|" sep_char]) and BODY(directory content[level_prefix, connector, name])
* **Entry script** for the directory tree builder is *tree_main.py* which then calls all other subscripts (cli.py, rptree.py, ...) through relative imports.

### RESULTS:
* *IN GENERAL*: Tree generation uses **indirect Recursion**: alternates for-loop iteration(for files and directories) with recursively calling tree_body() method to iterate through for each directory's contents.
* Efficient use of Python's pathlib library and its handy features to check file/folder properties as well as iterating(*non-recursively*) through a directory's contents. Implementation of argparse library which provides a complete ecosystem to capture&evaluate positional and optional attributes (e.g. -d, --output_file, --version, ...) and adjust the direction of the Python script and its output based on the provided argparse attribute values. 

