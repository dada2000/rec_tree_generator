#Provides the command-line interface for the application using argparse to "capture" the positional and optional arguments provided.
import argparse, pathlib, sys

#Relative imports: DO NOT work when cli.py is executed directly!!! Works fine when cli.py is imported itself and executed from another main file.
from . import __version__ #Relative import of version number from __init__.py
from .rptree import DirectoryTree

#FUNCTION DEFINITIONS:
def main():
    args = parse_cmd_line_arguments() #Outsources argparse argument capture&evaluation process in extra function (below)
    root_dir = pathlib.Path(args.root_dir)
    print(type(__version__))
    print(f"\n{36*'#'}\n## Welcome to Tree Generator v{__version__:>3} ##\n{36*'#'}") #Header preceeding main program and tree representation.
    print(f"Directories only?: {args.dir_only}")
    print(f"Output file: {'sys.stdout' if args.output_file == sys.stdout else args.output_file}")
    if not root_dir.is_dir(): #Checks if root_dir path is formatted correctly and also exists in actual file system. --> Otherwise exits system...
        print(f"Could not find your specified directory: {root_dir!r}! Exiting tree generator...")
        sys.exit()
    dir_only = args.dir_only #Boolean optional argument -> EITHER directories only OR files/directories are represented in current directory tree contents
    output_file = args.output_file #Stores output_file location -> type = str()
    if output_file != sys.stdout: #Validates correct input when --output_file optional argument is specified. --> Auto-corrects output_file to sys.stdout --> Program continues...
        if output_file == None:
            print(f"You did not specify an output file after setting optional parameter [-o]: {output_file}! -> Tree displayed in sys.stdout(CLI) instead...")
            output_file = sys.stdout
        elif not pathlib.Path(output_file).is_file():
            print(f"Could not find your specified output file: {output_file}! -> Tree output in sys.stdout instead...")
            output_file = sys.stdout
    tree = DirectoryTree(root_dir, dir_only, output_file) #Creates class object instance with provided path as root_dir.
    tree.generate() ##Generates complete tree (list) and creates print() output in CLI.

def parse_cmd_line_arguments(): #Processes argparse argument capture process and returns stored arguments in namespace(args)
    parser = argparse.ArgumentParser(prog="tree", description="Recursive directory tree generator", epilog="Closing tree generator ...")
    parser.version = f"RP Tree generator version: v{__version__}"
    parser.add_argument("-v", "--version", action="version")
    parser.add_argument("root_dir", metavar="ROOT_DIR", nargs="?", default=".", help="Provides start directory (ROOT_DIR) to generate subsequent files/directories tree")
    parser.add_argument("-d","--dir_only",action="store_true", help="Option to generate a directory only tree WITHOUT files")
    parser.add_argument("-o","--output_file", metavar="OUTPUT_FILE", nargs="?", default=sys.stdout, help="Save generated tree to an (existing) file location")
    return parser.parse_args()