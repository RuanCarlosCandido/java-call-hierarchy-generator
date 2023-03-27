Java Call Hierarchy Generator
This is a Python script for generating call hierarchies for Java classes in a project. Given a project path, the script parses each Java file in the project and generates a call hierarchy for all the methods in each class. The call hierarchy is represented as a tree structure, where each node represents a method call and the children of a node represent the methods called by that method. The script uses a depth-first search to traverse the call hierarchy and outputs the hierarchy to the console.

Installation
Clone the repository: git clone https://github.com/RuanCarlosCandido/java-call-hierarchy-generator.git
Change into the repository directory: cd java-call-hierarchy-generator
Install the required dependencies: pip install -r requirements.txt

Usage
Change the project_path variable in main.py to the path of your Java project.

Run the script: python main.py
The script will output the call hierarchy for each class in the project to the console.

Tests
The script includes test cases to ensure correct functionality. To run the tests, run pytest in the repository directory.
