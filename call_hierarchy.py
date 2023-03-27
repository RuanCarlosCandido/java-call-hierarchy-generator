import os

class Node:
    """
    Represents a node in the call hierarchy tree.
    """
    def __init__(self, name):
        self.name = name
        self.children = []

    def __str__(self):
        return self.name

def parse_class(class_str):
    """
    Extracts the class name and method names from a string representing a Java class.
    """
    class_name = ""
    methods = []

    # Extract class name
    class_lines = class_str.split('\n')
    for line in class_lines:
        if line.startswith("public class"):
            class_name = line.split(' ')[2].strip("{ ")
    
    # Extract methods
    method_lines = class_str[class_str.find("{")+1:class_str.rfind("}")].split('\n')
    for line in method_lines:
        if "public" in line and "(" in line and ")" in line:
            method_name = line.split('(')[0].split(' ')[-1]
            methods.append(method_name)
    
    return (class_name, methods)

def generate_hierarchy(class_dict, class_name, prefix=""):
    """
    Recursively generates the call hierarchy tree for a class.
    """
    root = Node(f"{prefix}{class_name}")
    
    # Iterate over the methods in the class
    for method in class_dict[class_name]:
        node = Node(f"{prefix}{class_name}.{method}()")
        
        # Check if the method calls a method in another class
        for other_class in class_dict:
            if other_class != class_name:
                for other_method in class_dict[other_class]:
                    if f"new {other_class}().{other_method}()" in class_dict[class_name][method]:
                        # If so, recursively generate the call hierarchy tree for the other class
                        node.children.append(generate_hierarchy(class_dict, other_class, prefix=f"{prefix}  -> "))
        
        root.children.append(node)
    
    return root

def build_call_hierarchy():
    """
    Builds the call hierarchy tree for each class in a Maven project's Java files.
    """
    project_path = "/home/ruan/Music/Scripts/test_program/"  # replace with actual path to Maven project
    
    class_dict = {}
    # Iterate over the Java files in the project
    for root, dirs, files in os.walk(project_path):
        for file in files:
            if file.endswith(".java"):
                with open(os.path.join(root, file), "r") as f:
                    class_str = f.read()
                    class_name, methods = parse_class(class_str)
                    class_dict[class_name] = {method: class_str for method in methods}
    
    hierarchy = {}
    # Generate the call hierarchy tree for each class
    for class_name in class_dict:
        hierarchy[class_name] = generate_hierarchy(class_dict, class_name, prefix="")
    
    return hierarchy

def print_hierarchy(node, prefix=""):
    """
    Recursively prints the call hierarchy tree starting from a given node.
    """
    print(f"{prefix}{node}")
    for child in node.children:
        print_hierarchy(child, prefix=f"{prefix}  -> ")

if __name__ == "__main__":
    hierarchy = build_call_hierarchy()
    # Print the call hierarchy for each class in the project
    for class_name in hierarchy:
        print(f"Call Hierarchy for {class_name}:\n")
        print_hierarchy(hierarchy[class_name])
