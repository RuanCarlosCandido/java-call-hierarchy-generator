class Node:
    def __init__(self, name):
        self.name = name
        self.children = []

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

def generate_hierarchy(class_dict, class_name):
    root = Node(class_name)
    
    for method in class_dict[class_name]:
        node = Node(f"{class_name}.{method}()")
        
        # Check if method calls another class method
        for other_class in class_dict:
            if other_class != class_name:
                for other_method in class_dict[other_class]:
                    if f"new {other_class}().{other_method}()" in class_dict[class_name][method]:
                        node.children.append(Node(f"{other_class}.{other_method}()"))
        
        root.children.append(node)
    
    return root

# test case 1
input_str_1 = """
public class ClassA {
    public String method1(){
        return "";
    }
}
"""
expected_output_1 = "ClassA.method1()"

class_dict = {"ClassA": ["method1"]}

root_1 = generate_hierarchy(class_dict, "ClassA")
output_1 = f"{root_1.children[0].name}"
assert output_1.strip() == expected_output_1.strip(), f"Expected output: {expected_output_1}, but got: {output_1}"



# test case 2
input_str1 = """package org;
public class ClassA {
    public String method1(){
        return new ClassB().method1();
    }
}"""

input_str2 = """package org.bb;
public class ClassB {
    public String method1(){
        return "";
    }
}"""

expected_output = "ClassA.method1() -> ClassB.method1()"

class_dict = {}
class_dict.update({parse_class(input_str1)[0]: {method: input_str1 for method in parse_class(input_str1)[1]}})
class_dict.update({parse_class(input_str2)[0]: {method: input_str2 for method in parse_class(input_str2)[1]}})

root = generate_hierarchy(class_dict, "ClassA")

output = f"{root.children[0].name}"
if root.children[0].children:
    output += f" -> {root.children[0].children[0].name}"

assert output.strip() == expected_output.strip()
