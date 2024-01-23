import subprocess
import json
import regex

# match strings of spaces bigger than 2 spaces
# (?<=\S)\s{2,}(?=\S)


def search(query):
    try:
        output = subprocess.check_output(["flatpak", "search", query], text=True)
        output = output.split("\n")[1:]  # Remove the first item (the header)

        results = {}

        for item in range(len(output)):
            # If the item is not empty
            if output[item] != "":
                # Split the item into the name and the description
                thisItem = output[item].split("\t")
                results[thisItem[0]] = {
                    "Description": thisItem[1],
                    "Application ID": thisItem[2],
                    "Version": thisItem[3],
                    "Branch": thisItem[4],
                    "Remotes": thisItem[5],
                }

    except subprocess.CalledProcessError:
        results = {}

    print(results)
    return results


with open("flatpak.json", "w") as f:
    json.dump(search("firefox"), f, indent=4)
