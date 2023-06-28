#Gets imported and called from rptree_project/tree_main.py(!)
#Provides main application functionalities: 1.) Iterates provided rel. or abs. root directory and constructs list recursively of all files/directories inside root_dir.
#                                           2.) Displays visual tree representation from constructed element list.
# High level Class: DirectoryTree class (.generate() )  #--> "Generates and displays tree diagram" based on root_dir input parameter
# Low level Class: _TreeGenerator(.build_tree() ) #--> "Iterates tree structure recursively and creates list with file/directory entries inside root_dir"
# Tree diagram consists of 2 main components: HEAD(rel. root directory[name and "|" sep_char]), BODY(directory content[level_prefix, connector, name])
#                                           Tree connectors are either PIPE, TEE or ELBOW(last element in current folder)
# In general: Tree generation uses indirect Recursion: alternates for-loop iteration(for files and directories) with recursively calling tree_body() method for each directory.
import os, pathlib, sys

#Define connector and prefix constants for visual tree output in CLI [4x spaces wide]
PIPE = "|" #len=1
#Connectors
ELBOW = "└──" #len=3
TEE = "├──"   #len=3

#Prefixes for files/folders inside directories
PIPE_PREFIX = "│   " #len=4
SPACE_PREFIX = "    " #len=4

#HIGH level DirectoryTree class
class DirectoryTree:
    def __init__(self, root_dir, dir_only=False, output_file=sys.stdout):
        self._output_file = output_file #Either sys.stdout(CLI) OR destination file location
        self._generator = _TreeGenerator(root_dir, dir_only) #instance attribute assigned -> _TreeGenerator (non-public class) instance object
    
    def generate(self):
        tree = self._generator.build_tree() #Creates list of files/directories including prefixes + connectors
        #print(f"===> INSIDE generate() -> self._output_file = {self._output_file}")
        if self._output_file != sys.stdout:
            tree.insert(0,"```")
            tree.append("```")
            self._output_file = open(self._output_file, mode="w", encoding="UTF-8") #Overwrites self._output_file so that it can be opened in "write mode" inside the "with" statement in the next line
        with self._output_file as stream:
            for entry in tree: #Prints directory tree list line by line in CLI  #TEST pathlib write_text option as alternative!
                print(entry, file=stream) #Uses file-option of print() that writes either into standard stream (sys.stdout[CLI!]) OR specified file path location (opened before)

#LOW level _TreeGenerator non-public class -> only to be used inside rptree.py [Not called directly!]
class _TreeGenerator:
    def __init__(self, root_dir, dir_only=False):
        self._root_dir = pathlib.Path(root_dir)  #Recursive start point (rel. or abs. path works!) for tree generation
        self._dir_only = dir_only #Boolean -> TRUE => Directories only output  |  FALSE => Files/Directories output (standard)
        self._tree = [] #list stores strings for each line/entry of tree diagram [incl. prefixes, connectors and name(file/directory)]
    
    def build_tree(self): #Combo method to call ._tree_head() and ._tree_body() methods and return completed self._tree list with all file/directory entries
        head_str, head_count = self.head_dir() #Returns head string formatting and entries count for root_dir
        self._tree_head(head_str, head_count)
        self._tree_body(self._root_dir)
        self._tree.append(f"\n{'  TREE GENERATION COMPLETED!  '.center(80,'*')}\n>>> SPECIFIED DIRECTORY: {pathlib.Path(head_str)}\n>>> LOCATION: {pathlib.Path(head_str).resolve()}\n")
        return self._tree
    
    def head_dir(self): #Returns (head_string, head entries count) tuple for optimized root dir formatting
        if str(self._root_dir.name) == "": #In case of default dir (".")
            cur_cwd = pathlib.Path.cwd()
            return (f"{cur_cwd.name}{os.sep}", f"[{len(list(cur_cwd.iterdir()))} entries]")
        elif self._root_dir.name=="..":
            return (f"{self._root_dir.resolve().name}{os.sep}", f"[{len(list(self._root_dir.iterdir()))} entries]")
        else:    
            return (f"{self._root_dir.name}{os.sep}", f"[{len(list(self._root_dir.iterdir()))} entries]")

    def _tree_head(self, head_str, head_count): #Gets called only 1x to generate first self._tree list entry
        self._tree.append(f"\n+++ SPECIFIED ROOT DIR +++\n{head_str} {head_count}\n{PIPE}")

    def _tree_body(self, directory, prefix=""): #Generates the remainder of the tree diagram
        entries = self._prepare_entries(directory) #Returns either directories only or files/directories for current root_directory contents
        entries_count = len(entries)
        #Loops through iterdir() files/directories:
        for idx, entry in enumerate(entries): #idx starts at 0 (!)
            connector = ELBOW if idx == entries_count - 1 else TEE #If current entry is last element of entries --> ELBOW connector (└──)
            if entry.is_dir(): #Conditional decides which submethod(dir or file) will be called with current entry.
                self._add_directory(entry, idx, entries_count, prefix, connector)
            else:
                self._add_file(entry, prefix, connector)
    
    def _prepare_entries(self, directory): #Returns either directories only or files/directories for current root_directory contents
        entries = directory.iterdir() #Creates an iterator which contains all files and directories NON-recursively located inside current directory(root_dir)
        if self._dir_only:
            entries = [entry for entry in entries if entry.is_dir()] #Filters entries for only directories posix path objects.
            return entries
        else:
            entries = sorted(entries, key=lambda entry : entry.is_file()) #Sorts and converts iterator into sorted list with directories first followd by files.
            return entries
    
    def _add_directory(self, directory, idx, entries_count, prefix, connector):
        self._tree.append(f"{prefix}{connector} {directory.name}{os.sep} [{len(list(directory.iterdir()))} entries]") #Creates list object(str) for current directory
        #Checks relative position (idx vs. total entries_count) of CURRENT DIRECTORY --> determines according prefix for its sub-elements (files/dirs)
        #Adds PREFIX spacer [EITHER empty 4x whitespace OR "|" + 3x whitespaces] to the RIGHT of current prefix [starts with empty prefix at level 0]
        # └──> So that the connectors of its subelements start "under" the first letter (pos5) of the current directory.
        # Prefix is concatenated in each function call under current directory.
        if idx != entries_count-1: #If current directory is not last element of its directory level
            prefix += PIPE_PREFIX
        else: #If current directory IS last element of its directory level
            prefix += SPACE_PREFIX
        self._tree_body(directory=directory, prefix=prefix)#Indirect recursive call for current directory --> all files/directories inside current directory are then iterated...
        #Adds final spacer prefix under the "printed" directory to separate it from the following items (with removed whitespaces on the right) 
        self._tree.append(prefix.rstrip())
    
    def _add_file(self, file, prefix, connector):
        self._tree.append(f"{prefix}{connector} {file.name}")

#MAIN PROGRAM:

