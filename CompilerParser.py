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
        self.mustBe("keyword", "class")

        # Parse class name (identifier)
        classNameToken = self.mustBe("identifier", None)

        # Create the class parse tree node
        classTree = ParseTree("class", None)  # No value for the class node itself

        # Add class name as a child node
        classTree.addChild(ParseTree("identifier", classNameToken.getValue()))

        # Parse opening '{'
        openBracket = self.mustBe("symbol", "{")
        classTree.addChild(ParseTree("symbol", openBracket.getValue()))  # Add '{' to the parse tree

        # Parse the class body (handle classVarDec)
        while self.current().getValue() != "}":
            if self.current().getType() == "keyword" and self.current().getValue() in ["static", "field"]:
                classTree.addChild(self.compileClassVarDec())
            else:
                self.next()

        # Parse closing '}'
        closeBraceToken = self.mustBe("symbol", "}")
        classTree.addChild(ParseTree("symbol", closeBraceToken.getValue()))  # Add '}' to the parse tree

        return classTree

    

    def compileClassVarDec(self):
        """
        Generates a parse tree for a static variable declaration or field declaration
        @return a ParseTree that represents a static variable declaration or field declaration
        """
        varDecTree = ParseTree("classVarDec", "")
        keywordToken = self.mustBe("keyword", None)  # either 'static' or 'field'
        varDecTree.addChild(ParseTree("keyword", keywordToken.getValue()))

        # Parse type (e.g., 'int')
        typeToken = self.mustBe("keyword", None)  # 'int', 'boolean', etc.
        varDecTree.addChild(ParseTree("keyword", typeToken.getValue()))

        # Parse variable name
        varNameToken = self.mustBe("identifier", None)
        varDecTree.addChild(ParseTree("identifier", varNameToken.getValue()))

        # Parse semicolon
        self.mustBe("symbol", ";")
        varDecTree.addChild(ParseTree("symbol", ";"))

        return varDecTree


      
    

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
        statements = ParseTree("statements", "")
        while self.current().getValue() not in ["}", "else"]:  # Adjust as needed for your language
            if self.current().getValue() == "let":
                statements.addChild(self.compileLet())
            elif self.current().getValue() == "if":
                statements.addChild(self.compileIf())
            elif self.current().getValue() == "while":
                statements.addChild(self.compileWhile())
            elif self.current().getValue() == "do":
                statements.addChild(self.compileDo())
            else:
                self.next()  # Skip tokens that don't start a statement
        return statements
    
    
    def compileLet(self):
        """
        Generates a parse tree for a let statement
        @return a ParseTree that represents the statement
        """
        self.mustBe("keyword", "let")
        varName = self.mustBe("identifier", None)
        letTree = ParseTree("letStatement", varName.getValue())

        if self.current().getValue() == "=":
            self.next()  # Skip over the '=' symbol
            letTree.addChild(self.compileExpression())  # Parse the expression that represents the new value
            self.mustBe("symbol", ";")  # Expect a semicolon at the end of the statement

        return letTree


    def compileIf(self):
        """
        Generates a parse tree for an if statement
        @return a ParseTree that represents the statement
        """
        self.mustBe("keyword", "if")
        self.mustBe("symbol", "(")
        condition = self.compileExpression()  # Assuming compileExpression() is implemented
        self.mustBe("symbol", ")")

        self.mustBe("symbol", "{")
        ifBody = self.compileStatements()
        self.mustBe("symbol", "}")

        ifTree = ParseTree("ifStatement", condition)
        ifTree.addChild(ifBody)

        if self.current().getValue() == "else":
            self.next()
            self.mustBe("symbol", "{")
            elseBody = self.compileStatements()
            self.mustBe("symbol", "}")
            ifTree.addChild(elseBody)

        return ifTree

    
    def compileWhile(self):
        """
        Generates a parse tree for a while statement
        @return a ParseTree that represents the statement
        """
        self.mustBe("keyword", "while")
        self.mustBe("symbol", "(")
        condition = self.compileExpression()
        self.mustBe("symbol", ")")

        self.mustBe("symbol", "{")
        whileBody = self.compileStatements()
        self.mustBe("symbol", "}")

        whileTree = ParseTree("whileStatement", condition)
        whileTree.addChild(whileBody)
        return whileTree


    def compileDo(self):
        """
        Generates a parse tree for a do statement
        @return a ParseTree that represents the statement
        """
        self.mustBe("keyword", "do")
        methodName = self.mustBe("identifier", None)  # Assuming simple case; adjust for method calls
        self.mustBe("symbol", "(")
        # Assuming compileExpressionList() handles the list of expressions for arguments
        argumentList = self.compileExpressionList()  
        self.mustBe("symbol", ")")
        self.mustBe("symbol", ";")

        doTree = ParseTree("doStatement", methodName.getValue())
        doTree.addChild(argumentList)
        return doTree


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


    tokens1 = [
        Token("keyword", "class"),
        Token("identifier", "Main"),
        Token("symbol", "{"),
        Token("symbol", "}")
    ]
    parser1 = CompilerParser(tokens1)
    try:
        result1 = parser1.compileProgram()
        print("Test Case 1 Passed: Valid Class Parsing")
        print(result1)
    except Exception as e:
        print("Test Case 1 Failed: Valid Class Parsing")
        print(str(e))

        

    # tokens2 = [
    #     Token("keyword", "static"),
    #     Token("keyword", "int"),
    #     Token("identifier", "a"),
    #     Token("symbol", ";")
    # ]
    # parser2 = CompilerParser(tokens2)
    # try:
    #     result2 = parser2.compileProgram()
    #     print("Test Case 2 Failed: Should have thrown an error")
    # except ParseException as e:
    #     print("Test Case 2 Passed: Error correctly thrown\n")
    #     print(str(e))



    print('\n')

    # tokens3 = [
    #     Token("keyword", "class"),
    #     Token("identifier", "Main"),
    #     Token("symbol", "{"),
    #     Token("keyword", "static"),
    #     Token("keyword", "int"),
    #     Token("identifier", "a"),
    #     Token("symbol", ";"),
    #     Token("symbol", "}")
    # ]
    # parser2 = CompilerParser(tokens3)
    # try:
    #     result2 = parser2.compileProgram()
    #     print(result2)
    # except Exception as e:
    #     print("Test Case 3 Failed:", str(e))



    # test_cases = [
    #     {
    #         'description': 'Valid function with parameters',
    #         'tokens': [
    #             Token("keyword", "function"), Token("identifier", "int"), Token("identifier", "sum"),
    #             Token("symbol", "("), Token("identifier", "int"), Token("identifier", "a"),
    #             Token("symbol", ","), Token("identifier", "int"), Token("identifier", "b"),
    #             Token("symbol", ")"), Token("symbol", "{"), Token("symbol", "}")
    #         ]
    #     },
    #     {
    #         'description': 'Valid method with no parameters',
    #         'tokens': [
    #             Token("keyword", "method"), Token("identifier", "void"), Token("identifier", "display"),
    #             Token("symbol", "("), Token("symbol", ")"), Token("symbol", "{"), Token("symbol", "}")
    #         ]
    #     },
    #     {
    #         'description': 'Constructor with parameters',
    #         'tokens': [
    #             Token("keyword", "constructor"), Token("identifier", "Main"), Token("identifier", "Main"),
    #             Token("symbol", "("), Token("identifier", "int"), Token("identifier", "size"),
    #             Token("symbol", ")"), Token("symbol", "{"), Token("symbol", "}")
    #         ]
    #     },
    #     {
    #         'description': 'Invalid subroutine (missing closing brace)',
    #         'tokens': [
    #             Token("keyword", "function"), Token("identifier", "int"), Token("identifier", "broken"),
    #             Token("symbol", "("), Token("identifier", "int"), Token("identifier", "param"),
    #             Token("symbol", ")"), Token("symbol", "{")
    #         ]  # Missing closing '}' to simulate an error case.
    #     }
    # ]

    # for case in test_cases:
    #     parser = CompilerParser(case['tokens'])
    #     try:
    #         result = parser.compileSubroutine()
    #         print(f"{case['description']}: PASSED")
    #         print("Resulting Parse Tree:")
    #         print(result)
    #     except ParseException as e:
    #         print(f"{case['description']}: FAILED")
    #         print(f"Error: {e}")


    # tests = [
    #     {
    #         "description": "Subroutine body with one variable declaration",
    #         "tokens": [
    #             Token("symbol", "{"),
    #             Token("keyword", "var"),
    #             Token("identifier", "int"),
    #             Token("identifier", "x"),
    #             Token("symbol", ";"),
    #             Token("symbol", "}")
    #         ]
    #     },
    #     {
    #         "description": "Variable declaration missing semicolon",
    #         "tokens": [
    #             Token("keyword", "var"),
    #             Token("identifier", "int"),
    #             Token("identifier", "y")
    #         ]
    #     }
    # ]

    # for test in tests:
    #     parser = CompilerParser(test['tokens'])
    #     try:
    #         if test['description'].startswith("Subroutine"):
    #             result = parser.compileSubroutineBody()
    #         else:
    #             result = parser.compileVarDec()
    #         print(f"Test '{test['description']}' passed. Result: {result}")
    #     except Exception as e:
    #         print(f"Test '{test['description']}' failed with an error: {str(e)}")