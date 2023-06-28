#Main entry point script
#High level steps: 1) Provide starting directory as attribute in CLI using "Argparse" 
#                  2) Program recursively iterates through all files and folders using "pathlib" and stores them in list structure.
#                  3) Outputs "found" files and directories in visual tree representation in CLI.

#Calls main() from cli.py if tree_main.py is executed as __main__
import rptree_files.cli as cli
if __name__ == "__main__":
    cli.main()