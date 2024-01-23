#!/usr/bin/env python3

import os
import subprocess
import sys


global Colors
Colors = {
    "fg":{
        "black": "\033[30m",
        "red": "\033[31m",
        "green": "\033[32m",
        "yellow": "\033[33m",
        "blue": "\033[34m",
        "magenta": "\033[35m",
        "cyan": "\033[36m",
        "white": "\033[37m",
    },
    "bg": {
        "black": "\033[40m",
        "red": "\033[41m",
        "green": "\033[42m",
        "yellow": "\033[43m",
        "blue": "\033[44m",
        "magenta": "\033[45m",
        "cyan": "\033[46m",
        "white": "\033[47m",
    },
    "fmt": {
        "reset": "\033[0m",
        "bold": "\033[1m",
        "faint": "\033[2m",
        "italic": "\033[3m",
        "underline": "\033[4m",
        "blink": "\033[5m",
        "blink_fast": "\033[6m",
        "reverse": "\033[7m",
        "conceal": "\033[8m",
        "strikethrough": "\033[9m",
    }
}

global NO_PROMPT

class PackageManager:
    def __init__(self):
        pass

    def search(self, query):
        raise NotImplementedError("Search method must be implemented in the derived class")

    def install(self, package):
        raise NotImplementedError("Install method must be implemented in the derived class")

    def remove(self, package):
        raise NotImplementedError("Remove method must be implemented in the derived class")

class Dnf:
    def checkInstalled(package):
        try:
            output = subprocess.check_output(["dnf", "list", "installed", package], text=True)
            output = output.split("\n")
            if output[0].startswith("Error"):
                return False
            else:
                return True
        except subprocess.CalledProcessError:
            return False

    def search(self, query):
        try:
            output = subprocess.check_output(["dnf", "search", query], text=True)
            output = output.split("\n")
            
            results = {
                "Exact": {},
                "Similar": {}
            }

            exactResult = False

            # Cycle through each item in the output
            for item in range(len(output)):
                print(output[item])
                # If the item is not empty
                if output[item] != "":
                    # Check if the item is a header
                    if "=" in output[item]:
                        # Check if it's Exact or Similar matches
                        if "Exact" in output[item]:
                            # Set exactResult to True
                            exactResult = True
                            pass
                        elif "Summary" in output[item]:
                            # Set exactResult to False
                            exactResult = False
                            pass
                    else:
                        # Split the item into the name and the description
                        thisItem = output[item].split(" : ")
                        #print(thisItem)

                        # Create a dictionary for the item
                        """
                        {
                            "Name": "Name",
                            "Description": "Description"
                        }
                        """
                        thisItem = {
                            "Name": thisItem[0].split(".")[0],
                            "Architecture": thisItem[0].split(".")[1],
                            "Description": thisItem[1],
                            "isInstalled": self.checkInstalled(thisItem[0].split(".")[0])
                        }


                        # Add it to the results in the correct category
                        if exactResult:
                            results["Exact"][thisItem["Name"]] = thisItem
                        else:
                            results["Similar"][thisItem["Name"]] = thisItem
            
        except subprocess.CalledProcessError:
            results = {}

        return results

    def install(self, package):
        try:
            subprocess.check_call(["sudo", "dnf", "install", package,  if NO_PROMPT else "-y"])
        except subprocess.CalledProcessError:
            print(f"Error installing {package}")

    def remove(self, package):
        try:
            subprocess.check_call(["sudo", "dnf", "remove", package,  if NO_PROMPT else "-y"])
        except subprocess.CalledProcessError:
            print(f"Error removing {package}")

class Flatpak(PackageManager):
    def search(self, query):
        try:
            result = subprocess.check_output(["flatpak", "search", "--columns=application", query], text=True)
            return result.split("\n")
        except subprocess.CalledProcessError:
            return []

    def install(self, package):
        try:
            subprocess.check_call(["flatpak", "install", package,  if NO_PROMPT else "-y"])
        except subprocess.CalledProcessError:
            print(f"Error installing {package}")

    def remove(self, package):
        try:
            subprocess.check_call([ "flatpak", "uninstall", package, if NO_PROMPT else "-y"])
        except subprocess.CalledProcessError:
            print(f"Error removing {package}")

def prompt(message, max_value):
    while True:
        try:
            value = int(input(f"{message} [0-{max_value}]: "))
            if value < 0 or value > max_value:
                raise ValueError()
            return value
        except ValueError:
            print("Invalid input")


def search(query):
    # Search for the package in DNF
    dnf_results = Dnf.search(query)
    flatpak_results = Flatpak.search(query)

    all_results = {
        "Exact": {
            "dnf": dnf_results["Exact"],
            "flatpak": {
                flatpak_results["Exact"]
            }
        },
        "Similar": {}
    }

    # Print the results
    print(f"{Colors['fg']['cyan']}Exact matches{Colors['fmt']['reset']}")
    for packageNum in range(len(dnf_results["Exact"])):
        packageNum += 1
        package = dnf_results["Exact"][packageNum][0]
        # format packageNum to be 2 digits with a space in front
        packageNum = f"{packageNum:02d} "
        print(f"{packageNum}. {package}")

    
        

def main():
    args = sys.argv[1:]

    if len(args) == 0:
        print("USAGE: omni [function] {flag} <package>")
        sys.exit(1)

    if "--no-prompt" in args:
        args.remove("--no-prompt")
        NO_PROMPT = True
    else:
        NO_PROMPT = False

    # Check if each package manager is installed
    dnf_installed = False
    flatpak_installed = False

    try:
        subprocess.check_output(["which", "dnf"])
        dnf_installed = True
    except subprocess.CalledProcessError:
        pass

    try:
        subprocess.check_output(["which", "flatpak"])
        flatpak_installed = True
    except subprocess.CalledProcessError:
        pass

    # Check if the user wants to install a package


       



if __name__ == "__main__":
    main()
