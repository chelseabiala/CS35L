import os
import sys
import zlib
# Keep the function signature,
# but replace its body with your implementation.
#
# Note that this is the driver function.
# Please write a well-structured implemention by creating other functions outside of this one,
# each of which has a designated purpose.
#
# As a good programming practice,
# please do not use any script-level variables that are modifiable.
# This is because those variables live on forever once the script is imported,
# and the changes to them will persist across different invocations of the imported functions.

# Top-order function, calls all helpers
def topo_order_commits():
    directory = discover()
    branches = get_list(directory)
    commit_nodes, roots = build_graph(directory, branches)
    sorted_commits = order_commits(commit_nodes, roots)
    print_commits(commit_nodes, sorted_commits, branches)

# Given helper class
class CommitNode:
    def __init__(self, commit_hash):
        """                                                                                    
        :type commit_hash: str                                                                 
        """
        self.commit_hash = commit_hash
        self.parents = set()
        self.children = set()

# Discover the .git directory
def discover():
    path = os.path.abspath(os.getcwd())
    # Loop upward through current path
    while True:
        # If path is at root, it's not in the directory
        if os.path.dirname(path) == path:
            sys.stderr.write("Not inside a Git repository")
            sys.exit(1)
        for i in os.listdir(path):
            if i == ".git":
                return os.path.realpath(os.path.join(path, i))
        path = os.path.abspath(os.path.join(path, os.pardir))

# Get the list of local branch names
def get_list(path):
    # Using git directory path found earlier
    path += "/refs/heads"
    branches = {}
    # Loop through directories to find brnches
    for path, dirs, files in os.walk(path):
        for f in files:
            commit = open(os.path.join(path,f),"r").read().replace("\n", "")
            # Remove /heads/ to be added to dictionary of branches
            name = os.path.join(path,f)[len(path)+1:]
            if commit not in branches:
                branches[commit] = []
                branches[commit].append(name)
    return branches

# Build the commit graph
def build_graph(path, branches):
    roots = set()
    objects = path + "/objects/"
    commit_nodes = {}
    # Loop through branch dictionary
    for commit in branches:
        # Add branches to commit nodes as CommitNode objects
        if commit not in commit_nodes:
            commit_nodes[commit] = CommitNode(commit)
            stack = [commit_nodes[commit]]
            # Loop through appended commits
            while stack:
                curr = stack.pop()
                parents = []
                #  Decode node to find parents
                data = zlib.decompress(open(os.path.join(objects, curr.commit_hash[0:2], curr.commit_hash[2:]), 'rb').read())
                text = str(data, 'utf-8', 'strict')
                text = text.split("\n")
                # Add parents to parents set in CommitNode
                for t in text:
                    if "parent" in t:
                        parents += (t.split()[1:])
                curr.parents = set(sorted(parents))
                # If the node has no parents, it's a root
                if len(curr.parents) == 0:
                    roots.add(curr.commit_hash)
                else:
                    for p in curr.parents:
                        if p not in commit_nodes:
                            commit_nodes[p] = CommitNode(p)
                            parent = commit_nodes[p]
                            stack.append(parent)
                        curr_parent = commit_nodes[p]
                        # Add node to the parents' children list
                        curr_parent.children.add(curr.commit_hash)
            roots = sorted(roots)
    return commit_nodes, roots

# Generate a topological ordering of the commits in the graph
def order_commits(commit_nodes, roots):
    visited = set()
    sorted_commits = []
    stack = list(roots)
    # Loop through roots
    while stack:
        # Don't pop until the end
        node = stack[-1]
        visited.add(node)
        added = False
        # Order the children nd add to sorted list
        for child in sorted(commit_nodes[node].children):
            if child not in visited:
                stack.append(child)
                added = True
                break
        if not added:
            sorted_commits.append(stack.pop())
    return sorted_commits

# Print the commit hashes in the order generated by the previous step, from the least to the greatest
def print_commits(commit_nodes, sorted_commits, branches):
    is_sticky = False
    # Loop through sorted commits
    for i in range(len(sorted_commits)):
        # Get hash to print
        hash_print = sorted_commits[i]
        if is_sticky:
            is_sticky = False
            sticky_hash_print = " ".join(commit_nodes[hash_print].children)
            print(f"={sticky_hash_print}")
        # If there is a branch, sort and append
        if hash_print in branches:
            sorted_branches = sorted(branches[hash_print])
        else:
            sorted_branches = []
        if branches:
            print(hash_print+(" "+" ".join(sorted_branches)))
        else:
            print(hash_print+("   "))
        # Prepare to process next commit
        if len(sorted_commits) > (i+1):
            if sorted_commits[i+1] not in commit_nodes[hash_print].parents:
                is_sticky = True
                sticky_hash_print = " ".join(commit_nodes[hash_print].parents)
                print(f"{sticky_hash_print}=\n")
            
if __name__ == '__main__':
    topo_order_commits()

# Changed permissions to run strace, looked for  commands called containng exec(), were none
