class ParseException(Exception):
    """
    Raised when tokens provided don't match the expected grammar
    Use this with `raise ParseException("My error message")`
    """
    pass


class ParseTree():

    def __init__(self, node_type, value):
        """
        A node in a Parse Tree data structure
        @param node_type The type of node (see element types).
        @param value The node's value. Should only be used on terminal nodes/leaves, and empty otherwise.
        """
        self.node_type = node_type
        self.value = value
        self.children = []
    

    def addChild(self,child):
        """
        Adds a ParseTree as a child of this ParseTree
        @param child The ParseTree to add
        """
        print(f"Adding child with type {child.node_type} to parent with type {self.node_type}")
        self.children.append(child)
    

    def getChildren(self):
        """
        Get a list of child nodes in the order they were added.
        @return A LinkedList of ParseTrees 
        """
        return self.children
    

    def getType(self):
        """
        Get the type of this ParseTree Node
        @return The type of node (see element types).
        """
        return self.node_type
    

    def getValue(self):
        """
        Get the value of this ParseTree Node
        @return The node's value. Should only be used on terminal nodes/leaves, and empty otherwise.
        """
        return self.value
    

    def __str__(self,depth=0):
        """
        Generate a string from this ParseTree
        @return A printable representation of this ParseTree with indentation
        """              
        indent = "  " * depth  # Indentation to show tree structure
        result = indent + self.node_type
        if self.value:
            result += " (" + str(self.value) + ")"  # Display node type and value
        for child in self.children:
            result += "\n" + child.__str__(depth + 1)  # Recursively print children
        return result

    

class Token(ParseTree):

    """
    Token for parsing. Can be used as a terminal node in a ParseTree
    """
    def __init__(self, token_type, value):
        self.token_type = token_type
        self.value = value

    def getType(self):
        return self.token_type

    def getValue(self):
        return self.value
    
