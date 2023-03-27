import os

class Node:
    def __init__(self, name):
        self.name = name
        self.children = []

    def __str__(self):
        return self.name

def parse_class(class_str):
    class_name = ""
    methods = []

    # extract class name
    class_lines = class_str.split('\n')
    for line in class_lines:
        if line.startswith("public class"):
            class_name = line.split(' ')[2].strip("{ ")
    
    # extract methods
    method_lines = class_str[class_str.find("{")+1:class_str.rfind("}")].split('\n')
    for line in method_lines:
        if "public" in line and "(" in line and ")" in line:
            method_name = line.split('(')[0].split(' ')[-1]
            methods.append(method_name)
    
    return (class_name, methods)

def generate_hierarchy(class_dict, class_name, prefix=""):
    root = Node(f"{prefix}{class_name}")
    
    for method in class_dict[class_name]:
        node = Node(f"{prefix}{class_name}.{method}()")
        
        # Check if method calls another class method
        for other_class in class_dict:
            if other_class != class_name:
                for other_method in class_dict[other_class]:
                    if f"new {other_class}().{other_method}()" in class_dict[class_name][method]:
                        node.children.append(generate_hierarchy(class_dict, other_class, prefix=f"{prefix}  -> "))
        
        root.children.append(node)
    
    return root

def build_call_hierarchy():
    project_path = "/home/ruan/Music/Scripts/test_program/"  # replace with actual path to Maven project
    
    class_dict = {}
    for root, dirs, files in os.walk(project_path):
        for file in files:
            if file.endswith(".java"):
                with open(os.path.join(root, file), "r") as f:
                    class_str = f.read()
                    class_name, methods = parse_class(class_str)
                    class_dict[class_name] = {method: class_str for method in methods}
    
    hierarchy = {}
    for class_name in class_dict:
        hierarchy[class_name] = generate_hierarchy(class_dict, class_name, prefix="")
    
    return hierarchy

def print_hierarchy(node, prefix=""):
    print(f"{prefix}{node}")
    for child in node.children:
        print_hierarchy(child, prefix=f"{prefix}  -> ")

if __name__ == "__main__":
    hierarchy = build_call_hierarchy()
    for class_name in hierarchy:
        print(f"Call Hierarchy for {class_name}:\n")
        print_hierarchy(hierarchy[class_name])
