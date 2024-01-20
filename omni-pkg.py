"""
A package manager wrapper for local and containerised package managers.
Developed by jxctno (jxctno@jxctno.com)
Heavily based on Rhino Linux's 'rhino-pkg' (github.com/rhino-linux/rhino-pkg)
"""

import shutil
import subprocess
import json
import os


global PACKAGE_MANAGERS 
PACKAGE_MANAGERS = {
    "apt": {
        "command": "apt",
        "install": "install",
        "remove": "remove",
        "update": "update",
        "upgrade": "upgrade",
        "search": "search",
        "list": "list",
        "show": "show",
        "clean": "clean"
    },
    "dnf": {
        "command": "dnf",
        "install": "install",
        "remove": "remove",
        "update": "update",
        "upgrade": "upgrade",
        "search": "search",
        "list": "list",
        "show": "info",
        "clean": "clean"
    },
    "pacman": {
        "command": "pacman",
        "install": "-S",
        "remove": "-R",
        "update": "-Sy",
        "upgrade": "-Su",
        "search": "-Ss",
        "list": "-Q",
        "show": "-Qi",
        "clean": "-Sc"
    },
    "emerge": {
        "command": "emerge",
        "install": -1,
        "remove": "--unmerge",
        "update": "--sync",
        "upgrade": "--update --deep",
        "search": "--search",
        "list": "--list",
        "show": "--info",
        "clean": "--depclean"
    },
    "pkgtool": {
        "command": "pkgtool",
        "install": "installpkg",
        "remove": "removepkg",
        "update": -1,
        "upgrade": -1,
        "search": -1,
        "list": "ls",
        "show": -1,
        "clean": -1
    },
    "zypper": {
        "command": "zypper",
        "install": "install",
        "remove": "remove",
        "update": "update",
        "upgrade": "dup",
        "search": "search",
        "list": "search --installed-only",
        "show": "info",
        "clean": "clean"
    },
    "dpkg": {
        "command": "dpkg",
        "install": "-i",
        "remove": "-r",
        "update": "--configure -a",
        "upgrade": "-l",
        "search": "-l",
        "list": "-l",
        "show": "-l",
        "clean": "apt-get clean && apt-get autoclean"
    },
    "yum": {
        "command": "yum",
        "install": "install",
        "remove": "remove",
        "update": "update",
        "upgrade": "update",
        "search": "search",
        "list": "list installed",
        "show": "info",
        "clean": "clean all"
    },
    "apk": {
        "command": "apk",
        "install": "add",
        "remove": "del",
        "update": "update",
        "upgrade": "upgrade",
        "search": "search",
        "list": "info",
        "show": "info",
        "clean": "cache clean"
    },
    "flatpak": {
        "command": "flatpak",
        "install": "install",
        "remove": "uninstall",
        "update": "update",
        "upgrade": "upgrade",
        "search": "search",
        "list": "list",
        "show": "info",
        "clean": "repair"
    },
    "snap": {
        "command": "snap",
        "install": "install",
        "remove": "remove",
        "update": "refresh",
        "upgrade": "refresh",
        "search": "find",
        "list": "list",
        "show": "info",
        "clean": "forget"
    }
}


# System class for managing package managers.
class System:
    def __init__(self, verbose=False):
        # Dictionary to store available package managers and their paths.
        self.PackageManagers = {}
        # Flag for verbose output
        self.verbose = verbose
        # Initializing available package managers.
        self.initialize_package_managers()

    # Function to check if a package manager command is available.
    def check_package_manager(self, command):
        return shutil.which(command)

    # Function to initialize available package managers.
    def initialize_package_managers(self):
        for pm, commands in PACKAGE_MANAGERS.items():
            path = self.check_package_manager(commands["command"])
            if path:
                self.PackageManagers[pm] = {"commands": commands, "path": path}

    # Function to search for a package across all installed package managers.
    def search_package(self, search_query):
        results = {}
        for pm_name, pm_info in self.PackageManagers.items():
            pm_commands = pm_info["commands"]
            search_cmd = [pm_info["path"], pm_commands["search"], search_query]
            # Assuming the output format for the search results is a list of dictionaries
            search_result = self.run_shell_command(search_cmd)
            if search_result:
                results[pm_name] = search_result
                if self.verbose:
                    print(f"Search result for {pm_name}: {search_result}")
        return results

    # Function to run a shell command and return the output as a list of dictionaries.
    def run_shell_command(self, command):
        # result = subprocess.run(command, capture_output=True, text=True)
        # if result.returncode == 0:
        #     # Assuming the output format for the search results is a list of dictionaries
        #     return json.loads(result.stdout)
        # else:
        #     return None
        if self.verbose:
            print(f"Running command: {command}")

        # turn command into string
        command = " ".join(command)
        os.system(command)

# Example usage:
VERBOSE = True  # Set to True for verbose output
system_info = System(verbose=VERBOSE)
search_query = "example-package"
search_results = system_info.search_package(search_query)

# Printing the search results
print("Search Results:")
print(f"Search Query: {search_query}")
print("Results:")
for pm_name, pm_results in search_results.items():
    print(f"- {pm_name}: {pm_results}")