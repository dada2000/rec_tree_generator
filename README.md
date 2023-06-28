# RECURSIVE TREE GENERATOR -> GRAPHICAL OUTPUT IN CLI:

## USING: pathlib, argparse, indirect recursive implementation
### GENERAL:
**High level steps:**
1. Provide starting directory in CLI as positional argument (rel. or abs.) and optional arguments (uses argparse library).
2. Program iterates (indirect recursion) through all files and folders (uses pathlib library) and stores them in a list.
3. Resulting tree (files, folders) can either be printed in CLI(default) or into specified file path (validates file location upfront).

### BACKGROUND DETAILS:
**Main application functionalities:**
* Iterates provided rel. or abs. root directory and constructs list containing all files/directories under specified root_dir.
* Displays visual tree representation from constructed element list with indents and file counts preview.
* **High level Class**: DirectoryTree class (.generate()) --> Generates and displays tree diagram --> Either in CLI or into specified file location.
* **Low level Class**: _TreeGenerator(.build_tree()) --> Iterates entire tree structure recursively --> Creates list (self._tree) with all file/directory entries
* Tree diagram(list) consists of 2 main components: HEAD(root directory[name and "|" sep_char]) and BODY(directory content[level_prefix, connector, name])
* **Entry script** for the directory tree builder is *tree_main.py* which then calls all other subscripts (cli.py, rptree.py, ...) through relative imports.

### RESULTS:
* *IN GENERAL*: Tree generation uses **indirect recursion**: alternates for-loop iteration(for files and directories) with recursively calling tree_body() method for each subsquent directory.
* Efficient use of Python's pathlib and argparse libraries and its handy features to check file/folder properties as well as iterating(*non-recursively*) through a directory's content. Argparse library provides a complete ecosystem to capture&evaluate positional and optional arguments (e.g. -d, --output_file, --version, ...) which dynamically determine the execution flow of the Python script and its outputs.

