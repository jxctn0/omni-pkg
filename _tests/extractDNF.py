import subprocess
import json

def search(query):
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
                    print(thisItem)

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
                        "Description": thisItem[1]
                    }


                    # Add it to the results in the correct category
                    if exactResult:
                        results["Exact"][thisItem["Name"]] = thisItem
                    else:
                        results["Similar"][thisItem["Name"]] = thisItem

        print(results)
        return results
        
    except subprocess.CalledProcessError:
        results = {}

    return results

with open("packages.json", "w") as file:
    json.dump(search("libre"), file, indent=4)