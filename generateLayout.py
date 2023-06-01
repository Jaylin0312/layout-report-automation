import json
import copy

def is_empty(value):
    if isinstance(value, dict):
        return len(value) == 0
    elif isinstance(value, str):
        return value.strip() == ""
    elif isinstance(value, tuple) or isinstance(value, list):
        return len(value) == 0
    else:
        return False

def check_empty_values(json_data, res):
    for key, value in json_data.items():
        if is_empty(value):
            if key not in res:
                res.append(key)
        elif isinstance(value, dict):
            check_empty_values(value, res)
        elif isinstance(value, list):
            for item in value:
                if isinstance(item, dict):
                    check_empty_values(item, res)
    return res


def remove_fields(json_data, elem):
    if isinstance(json_data, dict):
        modified_json_data = {}
        for key, value in json_data.items():
            if key != elem:
                # Recursively check fields in dictionaries
                modified_json_data[key] = remove_fields(value, elem)
    elif isinstance(json_data, list):
        modified_json_data = []
        for item in json_data:
            # Recursively check fields from list items
            modified_item = remove_fields(item, elem)
            # Append the modified item if it's not None
            if modified_item is not None:
                modified_json_data.append(modified_item)
    else:
        # Create a deep copy for non-dict, non-list values
        modified_json_data = copy.deepcopy(json_data)  
    
    return modified_json_data

def check_file(json_data, elem, f):
    modified_json_data = remove_fields(json_data, elem)
    json.dump(modified_json_data, f)


def main():
    res = []
    count = 1

    # Load the JSON data from a layout file
    with open('layouts/layout0.json', 'r') as f:
        json_data = json.load(f)

    # Call the function to check for empty values and store in res
    res = check_empty_values(json_data, res)
    print(res)

    for elem in res:
        with open(f"layouts/layout{count}.json", "w") as f:
            check_file(json_data, elem, f)
        f.close()
        count += 1

    