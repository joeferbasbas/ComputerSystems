from ParseTree import *

class CompilerParser :

    def __init__(self,tokens):
        """
        Constructor for the CompilerParser
        @param tokens A list of tokens to be parsed
        """
        self.tokens = tokens
        self.position = 0
        
    

    def compileProgram(self):
        """
        Generates a parse tree for a single program
        @return a ParseTree that represents the program
        """
        return self.compileClass()
    
    
    def compileClass(self):
        """
        Generates a parse tree for a single class
        @return a ParseTree that represents a class
        """
        print("Checking for 'class' keyword...")
        self.mustBe("keyword", "class")
        
        print("Getting class name...")
        classNameToken = self.mustBe("identifier", None)
        
        # Create class node with the class name
        classTree = ParseTree("class", classNameToken.getValue())

        print("Checking for opening '{'...")
        openBraceToken = self.mustBe("symbol", "{")
        classTree.addChild(ParseTree("symbol", openBraceToken.getValue()))

        print("Parsing class body...")
        # Assume compileClassVarDec() is implemented to handle variable declarations
        while self.current().getValue() != "}":
            if self.current().getValue() == "static":  # or other conditions based on variable declarations
                classTree.addChild(self.compileClassVarDec())
            else:
                self.next()  # This is a simplification, adjust based on actual content handling

        print("Checking for closing '}'...")
        closeBraceToken = self.mustBe("symbol", "}")
        classTree.addChild(ParseTree("symbol", closeBraceToken.getValue()))

        print("Class parsing completed.")
        return classTree




    

    def compileClassVarDec(self):
        """
        Generates a parse tree for a static variable declaration or field declaration
        @return a ParseTree that represents a static variable declaration or field declaration
        """
        declarationType = self.current().getValue()  # Get 'static' or 'field'
        declarationTree = ParseTree("declaration", declarationType)
        self.next()  # Move past 'static' or 'field'
        
        typeToken = self.mustBe("identifier", None)  # Expect the type
        declarationTree.addChild(ParseTree("type", typeToken.getValue()))
        
        varNameToken = self.mustBe("identifier", None)  # Expect the variable name
        declarationTree.addChild(ParseTree("varName", varNameToken.getValue()))
        
        self.mustBe("symbol", ";")  # Expect the semicolon
        return declarationTree


      
    

    def compileSubroutine(self):
        """
        Generates a parse tree for a method, function, or constructor
        @return a ParseTree that represents the method, function, or constructor
        """
        subroutineTypeToken = self.current()
        self.next()  # Move past the type keyword

        if subroutineTypeToken.getValue() == "constructor":
            # Constructor name, usually the same as the class name
            constructorNameToken = self.mustBe("identifier", None)
            self.mustBe("symbol", "(")  # Now expect the '('
        else:
            returnTypeToken = self.mustBe("identifier", None)
            subroutineNameToken = self.mustBe("identifier", None)
            self.mustBe("symbol", "(")

        # Process parameters
        parameters = self.compileParameterList()
        self.mustBe("symbol", ")")

        # Subroutine body assumed to be enclosed with '{' and '}'
        self.mustBe("symbol", "{")
        # Process the body here (not implemented)
        self.mustBe("symbol", "}")

        return ParseTree("subroutine", {
            "type": subroutineTypeToken.getValue(),
            "name": constructorNameToken.getValue() if subroutineTypeToken.getValue() == "constructor" else subroutineNameToken.getValue(),
            "parameters": parameters,
            # Body would be added here
        })
    
    
    def compileParameterList(self):
        """
        Generates a parse tree for a subroutine's parameters
        @return a ParseTree that represents a subroutine's parameters
        """
        paramListTree = ParseTree("parameterList", "")
    
        # Check if the next token is ')' which means the parameter list is empty
        if self.current().getValue() == ")":
            return paramListTree  # Return empty parameter list

        while True:
            # Expect type identifier
            typeToken = self.mustBe("identifier", None)
            # Expect parameter name identifier
            paramNameToken = self.mustBe("identifier", None)
            
            paramListTree.addChild(ParseTree("parameter", typeToken.getValue() + " " + paramNameToken.getValue()))
            
            # If the next token is ',', there are more parameters
            if self.current().getValue() == ",":
                self.next()  # Move past the comma to the next parameter
            else:
                break  # Exit the loop if there's no comma

        return paramListTree 
    
    
    def compileSubroutineBody(self):
        """
        Generates a parse tree for a subroutine's body
        @return a ParseTree that represents a subroutine's body
        """
        print("Parsing subroutine body...")
        bodyTree = ParseTree("subroutineBody", "")

        self.mustBe("symbol", "{")  # Assuming subroutine body starts with '{'
        
        while self.current().getValue() != "}":
            if self.current().getValue() == "var":
                bodyTree.addChild(self.compileVarDec())
            elif self.current().getValue() == "if":
                bodyTree.addChild(self.compileIf())
            elif self.current().getValue() == "while":
                bodyTree.addChild(self.compileWhile())
            # Add more statement types as necessary
            else:
                # Simple handling for unrecognized or end statements (e.g., break, return)
                self.next()  # Skip or simple parse of other types of statements
                
        self.mustBe("symbol", "}")  # End of subroutine body

        return bodyTree
    
    
    def compileVarDec(self):
        """
        Generates a parse tree for a variable declaration
        @return a ParseTree that represents a var declaration
        """
        print("Parsing variable declaration...")
        varDecTree = ParseTree("variableDeclaration", "")
        
        # Assume the 'var' keyword has already been identified if this method is called
        self.mustBe("keyword", "var")
        
        typeToken = self.mustBe("identifier", None)  # Type of the variable(s)
        varDecTree.addChild(ParseTree("type", typeToken.getValue()))
        
        # Handle one or more variable names separated by commas
        while True:
            varNameToken = self.mustBe("identifier", None)
            varDecTree.addChild(ParseTree("varName", varNameToken.getValue()))
            
            # Check if there is a comma, indicating more variables
            if self.current().getValue() == ",":
                self.next()
            elif self.current().getValue() == ";":
                self.next()
                break  # End of variable declaration
            else:
                raise ParseException("Expected ',' or ';', but found " + self.current().getValue())

        return varDecTree 
    

    def compileStatements(self):
        """
        Generates a parse tree for a series of statements
        @return a ParseTree that represents the series of statements
        """
        return None 
    
    
    def compileLet(self):
        """
        Generates a parse tree for a let statement
        @return a ParseTree that represents the statement
        """
        return None 


    def compileIf(self):
        """
        Generates a parse tree for an if statement
        @return a ParseTree that represents the statement
        """
        return None 

    
    def compileWhile(self):
        """
        Generates a parse tree for a while statement
        @return a ParseTree that represents the statement
        """
        return None 


    def compileDo(self):
        """
        Generates a parse tree for a do statement
        @return a ParseTree that represents the statement
        """
        return None 


    def compileReturn(self):
        """
        Generates a parse tree for a return statement
        @return a ParseTree that represents the statement
        """
        return None 


    def compileExpression(self):
        """
        Generates a parse tree for an expression
        @return a ParseTree that represents the expression
        """
        return None 


    def compileTerm(self):
        """
        Generates a parse tree for an expression term
        @return a ParseTree that represents the expression term
        """
        return None 


    def compileExpressionList(self):
        """
        Generates a parse tree for an expression list
        @return a ParseTree that represents the expression list
        """
        return None 


    def next(self):
        """
        Advance to the next token
        """

        self.position += 1
        return


    def current(self):
        """
        Return the current token
        @return the token
        """
        if self.position < len(self.tokens):
            return self.tokens[self.position]
        else:
            raise ParseException("No more token to parse at current retrieval")


    def have(self,expectedType,expectedValue):
        """
        Check if the current token matches the expected type and value.
        @return True if a match, False otherwise
        """ 
        currToken = self.current()
        if currToken.getType() == expectedType:
            if expectedValue is None or currToken.getValue() == expectedValue:
                return True
            
        return False


    def mustBe(self,expectedType,expectedValue):
        """
        Check if the current token matches the expected type and value.
        If so, advance to the next token, returning the current token, otherwise throw/raise a ParseException.
        @return token that was current prior to advancing.
        """
        currToken = self.current()  # Get the current token
        if not self.have(expectedType, expectedValue):
            raise ParseException(f"Expected {expectedType} '{expectedValue}', but found {currToken.getType()} '{currToken.getValue()}'")
        self.next()  # Only advance if the check passes
        return currToken

if __name__ == "__main__":


    """ 
    Tokens for:
        class MyClass {
        
        }
    """
    tokens = []
    tokens.append(Token("keyword","class"))
    tokens.append(Token("identifier","MyClass"))
    tokens.append(Token("symbol","{"))
    tokens.append(Token("symbol","}"))

    parser = CompilerParser(tokens)

    


    try:
        result = parser.compileProgram()
        print(result)
    except ParseException as e:
        print(f"Error Parsing: {e}")


    test_cases = []
    test_cases.append(Token("keyword", "static"))
    test_cases.append(Token("identifier", "int"))
    test_cases.append(Token("identifier", "myVar"))
    test_cases.append(Token("symbol", ";"))
    

    varDecParser = CompilerParser(test_cases)
    try:
        var_declaration = varDecParser.compileClassVarDec()
        print("Parsed Variable Declaration:")
        print(var_declaration)
    except ParseException as e:
        print(f'Error parsing: {e}')



    test_cases = [
        {
            'description': 'Valid function with parameters',
            'tokens': [
                Token("keyword", "function"), Token("identifier", "int"), Token("identifier", "sum"),
                Token("symbol", "("), Token("identifier", "int"), Token("identifier", "a"),
                Token("symbol", ","), Token("identifier", "int"), Token("identifier", "b"),
                Token("symbol", ")"), Token("symbol", "{"), Token("symbol", "}")
            ]
        },
        {
            'description': 'Valid method with no parameters',
            'tokens': [
                Token("keyword", "method"), Token("identifier", "void"), Token("identifier", "display"),
                Token("symbol", "("), Token("symbol", ")"), Token("symbol", "{"), Token("symbol", "}")
            ]
        },
        {
            'description': 'Constructor with parameters',
            'tokens': [
                Token("keyword", "constructor"), Token("identifier", "Main"), Token("identifier", "Main"),
                Token("symbol", "("), Token("identifier", "int"), Token("identifier", "size"),
                Token("symbol", ")"), Token("symbol", "{"), Token("symbol", "}")
            ]
        },
        {
            'description': 'Invalid subroutine (missing closing brace)',
            'tokens': [
                Token("keyword", "function"), Token("identifier", "int"), Token("identifier", "broken"),
                Token("symbol", "("), Token("identifier", "int"), Token("identifier", "param"),
                Token("symbol", ")"), Token("symbol", "{")
            ]  # Missing closing '}' to simulate an error case.
        }
    ]

    for case in test_cases:
        parser = CompilerParser(case['tokens'])
        try:
            result = parser.compileSubroutine()
            print(f"{case['description']}: PASSED")
            print("Resulting Parse Tree:")
            print(result)
        except ParseException as e:
            print(f"{case['description']}: FAILED")
            print(f"Error: {e}")


    tests = [
        {
            "description": "Subroutine body with one variable declaration",
            "tokens": [
                Token("symbol", "{"),
                Token("keyword", "var"),
                Token("identifier", "int"),
                Token("identifier", "x"),
                Token("symbol", ";"),
                Token("symbol", "}")
            ]
        },
        {
            "description": "Variable declaration missing semicolon",
            "tokens": [
                Token("keyword", "var"),
                Token("identifier", "int"),
                Token("identifier", "y")
            ]
        }
    ]

    for test in tests:
        parser = CompilerParser(test['tokens'])
        try:
            if test['description'].startswith("Subroutine"):
                result = parser.compileSubroutineBody()
            else:
                result = parser.compileVarDec()
            print(f"Test '{test['description']}' passed. Result: {result}")
        except Exception as e:
            print(f"Test '{test['description']}' failed with an error: {str(e)}")