class ParseException(Exception):
    """
    Raised when tokens provided don't match the expected grammar
    Use this with `raise ParseException("My error message")`
    """
    pass


class ParseTree():
    def __init__(self, node_type, value):
        if node_type is None:
            raise ValueError("ParseTree node_type cannot be None.")
        self.node_type = node_type
        self.value = value
        self.children = []

    def addChild(self, child):
        if child is None:
            raise ValueError(f"Cannot add None as a child to node of type {self.node_type}")
        if not hasattr(child, 'node_type'):
            raise TypeError(f"Child node does not have a 'node_type' attribute: {child}")
        
        print(f"Adding child with type {child.node_type} to parent with type {self.node_type}")
        self.children.append(child)

    def __str__(self):
        # Example for debugging the tree structure
        output = f"Node: {self.node_type}, Value: {self.value}\n"
        for child in self.children:
            output += f"    {str(child)}"
        return output

    

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

    def __str__(self):
        return f"Token(type={self.token_type}, value={self.value})"
    
