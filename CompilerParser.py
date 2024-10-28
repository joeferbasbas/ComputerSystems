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

        classNameToken = self.mustBe("identifier", None)

        classTree = ParseTree("class", None)  
        classTree.addChild(ParseTree("identifier", classNameToken.getValue()))

        openBracket = self.mustBe("symbol", "{")
        classTree.addChild(ParseTree("symbol", openBracket.getValue()))  

        while self.current().getValue() != "}":
            if self.current().getType() == "keyword" and self.current().getValue() in ["static", "field"]:
                classTree.addChild(self.compileClassVarDec())
            elif self.current().getType() == "keyword" and self.current().getValue() in ["constructor", "function", "method"]:
                # Call compileSubroutine() and add the resulting tree to the class tree
                classTree.addChild(self.compileSubroutine())
            else:
                self.next()

        closeBraceToken = self.mustBe("symbol", "}")
        classTree.addChild(ParseTree("symbol", closeBraceToken.getValue()))  

        return classTree

    

    def compileClassVarDec(self):
        """
        Generates a parse tree for a static variable declaration or field declaration
        @return a ParseTree that represents a static variable declaration or field declaration
        """
        varDecTree = ParseTree("classVarDec", "")
    
        # Parse the keyword 'field' or 'static'
        keywordToken = self.mustBe("keyword", None)
        varDecTree.addChild(ParseTree("keyword", keywordToken.getValue()))

        # Parse the type (e.g., 'boolean', 'int', 'char', etc.)
        typeToken = self.mustBe("keyword", None)
        varDecTree.addChild(ParseTree("type", typeToken.getValue()))

        # Parse the first variable name
        varNameToken = self.mustBe("identifier", None)
        varDecTree.addChild(ParseTree("identifier", varNameToken.getValue()))

        # Handle additional variables separated by commas
        while self.current().getValue() == ",":
            self.next()  # Move past the comma
            varNameToken = self.mustBe("identifier", None)  # Expect another variable name after the comma
            varDecTree.addChild(ParseTree("identifier", varNameToken.getValue()))

        # Now we expect a semicolon at the end of the declaration
        self.mustBe("symbol", ";")  # This is the key line that ensures a semicolon at the end
        varDecTree.addChild(ParseTree("symbol", ";"))

        return varDecTree


      
    

    def compileSubroutine(self):
        """
        Generates a parse tree for a method, function, or constructor
        @return a ParseTree that represents the method, function, or constructor
        """
        subroutineTree = ParseTree("subroutine", "")

        # Parse the subroutine keyword (e.g., function, constructor, method)
        subroutineKeyword = self.mustBe("keyword", None)  # 'constructor', 'function', 'method'
        subroutineTree.addChild(ParseTree("keyword", subroutineKeyword.getValue()))

        # Parse the return type: can be a keyword ('void', 'int') or an identifier (class name, e.g., 'Test')
        if self.current().getType() == "keyword":
            returnType = self.mustBe("keyword", None)
        else:
            returnType = self.mustBe("identifier", None)  # For constructors and class types
        subroutineTree.addChild(ParseTree("returnType", returnType.getValue()))

        # Parse the subroutine name (e.g., 'new' for constructors or other function names)
        subroutineName = self.mustBe("identifier", None)
        subroutineTree.addChild(ParseTree("identifier", subroutineName.getValue()))

        # Parse the parameter list
        self.mustBe("symbol", "(")
        parameterListTree = self.compileParameterList()  # Handles the parameter list
        subroutineTree.addChild(parameterListTree)
        self.mustBe("symbol", ")")

        # Parse the subroutine body (enclosed in curly braces)
        self.mustBe("symbol", "{")
        bodyTree = self.compileSubroutineBody()  # This parses the contents inside the {}
        subroutineTree.addChild(bodyTree)
        self.mustBe("symbol", "}")

        return subroutineTree

    
    
    def compileParameterList(self):
        """
        Generates a parse tree for a subroutine's parameters
        @return a ParseTree that represents a subroutine's parameters
        """
        parameterListTree = ParseTree("parameterList", "")

        # Only attempt to parse if we expect parameters (i.e., if the current token is a keyword or identifier)
        if self.current().getType() in ["keyword", "identifier"]:
            while True:
                # Parse the parameter type (either a keyword like 'int', 'boolean', or an identifier for class types)
                if self.current().getType() == "keyword":
                    paramType = self.mustBe("keyword", None)
                else:
                    paramType = self.mustBe("identifier", None)  # For constructors and class types

                # Parse the parameter name (must be an identifier)
                paramName = self.mustBe("identifier", None)

                # Add both the type and the name as a parameter node
                parameterListTree.addChild(ParseTree("parameter", f"{paramType.getValue()} {paramName.getValue()}"))

                # Check if there is another parameter (comma)
                if self.position < len(self.tokens) and self.current().getValue() == ",":
                    self.next()  # Skip the comma and continue with the next parameter
                else:
                    break  # No more parameters, exit the loop

        return parameterListTree
        
    
    def compileSubroutineBody(self):
        """
        Generates a parse tree for a subroutine's body
        @return a ParseTree that represents a subroutine's body
        """
        subRoutineBodyListTree = ParseTree("subroutineBody", "")
    
        while self.current().getValue() != "}":  # Continue until you hit the closing brace
            # Check if the current token is a variable declaration
            if self.current().getValue() == "var":
                varDecTree = self.compileVarDec()
                if varDecTree:
                    subRoutineBodyListTree.addChild(varDecTree)
            
            # Check if the current token is a let statement
            elif self.current().getValue() == "let":
                letTree = self.compileLet()
                if letTree:
                    subRoutineBodyListTree.addChild(letTree)
            
            # Handle other possible statements in the subroutine body
            elif self.current().getValue() == "return":
                returnTree = self.compileReturn()
                if returnTree:
                    subRoutineBodyListTree.addChild(returnTree)
            
            elif self.current().getValue() == "do":
                doTree = self.compileDo()
                if doTree:
                    subRoutineBodyListTree.addChild(doTree)
            
            elif self.current().getValue() == "while":
                whileTree = self.compileWhile()
                if whileTree:
                    subRoutineBodyListTree.addChild(whileTree)
            
            elif self.current().getValue() == "if":
                ifTree = self.compileIf()
                if ifTree:
                    subRoutineBodyListTree.addChild(ifTree)
            
            else:
                self.next()  # Skip any tokens that don't start a valid statement

        return subRoutineBodyListTree


    
    
    def compileVarDec(self):
        """
        Generates a parse tree for a variable declaration
        @return a ParseTree that represents a var declaration
        """
        varDecTree = ParseTree("varDec", "")  # Changed to "varDec" for local variable declarations
    
        # Parse the keyword 'int', 'boolean', etc.
        varType = self.mustBe("keyword", None)
        varDecTree.addChild(ParseTree("type", varType.getValue()))  # Add the type to the parse tree
        
        # Parse the variable name (identifier)
        varName = self.mustBe("identifier", None)
        varDecTree.addChild(ParseTree("identifier", varName.getValue()))  # Add the variable name to the parse tree
        
        # Expect a semicolon to terminate the declaration
        self.mustBe("symbol", ";")
        varDecTree.addChild(ParseTree("symbol", ";"))  # Add the semicolon to the parse tree

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
        print(f"Parsing let statement at token: {self.current()}")
    
        self.mustBe("keyword", "let")
        varName = self.mustBe("identifier", None)
        
        if varName is None:
            raise ValueError("Expected an identifier for variable name in let statement, got None.")
        
        letTree = ParseTree("letStatement", varName.getValue())

        if self.current().getValue() == "=":
            self.next()  # Skip over the '=' symbol
            exprTree = self.compileExpression()
            if exprTree is None:
                raise ValueError("Expected an expression in let statement after '=' but got None.")
            letTree.addChild(exprTree)
            self.mustBe("symbol", ";")  # Expect a semicolon at the end of the statement

        return letTree
        


    def compileIf(self):
        """
        Generates a parse tree for an if statement
        @return a ParseTree that represents the statement
        """
        ifTree = ParseTree("ifStatement", "")
    
        # 'if' keyword
        self.mustBe("keyword", "if")
        ifTree.addChild(ParseTree("keyword", "if"))
        
        # Opening parenthesis '('
        self.mustBe("symbol", "(")
        
        # Parse the condition (expression)
        conditionTree = self.compileExpression()
        if conditionTree:
            ifTree.addChild(conditionTree)
        
        # Closing parenthesis ')'
        self.mustBe("symbol", ")")
        
        # Opening brace '{'
        self.mustBe("symbol", "{")
        
        # Parse the 'if' body (statements inside the if block)
        ifBodyTree = self.compileStatements()
        if ifBodyTree:
            ifTree.addChild(ifBodyTree)
        
        # Closing brace '}'
        self.mustBe("symbol", "}")
        
        # Optional 'else' clause
        if self.current().getValue() == "else":
            self.next()  # Skip 'else' keyword
            ifTree.addChild(ParseTree("keyword", "else"))
            
            # Opening brace for 'else' block
            self.mustBe("symbol", "{")
            
            # Parse the 'else' body (statements inside the else block)
            elseBodyTree = self.compileStatements()
            if elseBodyTree:
                ifTree.addChild(elseBodyTree)
            
            # Closing brace '}'
            self.mustBe("symbol", "}")
        
        return ifTree

    
    def compileWhile(self):
        """
        Generates a parse tree for a while statement
        @return a ParseTree that represents the statement
        """
        whileTree = ParseTree("whileStatement", "")
    
        # 'while' keyword
        self.mustBe("keyword", "while")
        whileTree.addChild(ParseTree("keyword", "while"))
        
        # Opening parenthesis '('
        self.mustBe("symbol", "(")
        
        # Parse the condition (expression)
        conditionTree = self.compileExpression()
        if conditionTree:
            whileTree.addChild(conditionTree)
        
        # Closing parenthesis ')'
        self.mustBe("symbol", ")")
        
        # Opening brace '{'
        self.mustBe("symbol", "{")
        
        # Parse the 'while' body (statements inside the while block)
        whileBodyTree = self.compileStatements()
        if whileBodyTree:
            whileTree.addChild(whileBodyTree)
        
        # Closing brace '}'
        self.mustBe("symbol", "}")
        
        return whileTree
        


    def compileDo(self):
        """
        Generates a parse tree for a do statement
        @return a ParseTree that represents the statement
        """
        doTree = ParseTree("doStatement", "")
    
        # 'do' keyword
        self.mustBe("keyword", "do")
        doTree.addChild(ParseTree("keyword", "do"))
        
        # Parse the subroutine call
        subroutineCallTree = self.compileExpressionList()  # Assuming you have a method for parsing subroutine calls
        
        if subroutineCallTree:
            doTree.addChild(subroutineCallTree)
        
        # Expect a semicolon ';' at the end of the do statement
        self.mustBe("symbol", ";")
        
        return doTree


    def compileReturn(self):
        """
        Generates a parse tree for a return statement
        @return a ParseTree that represents the statement
        """
        returnTree = ParseTree("returnStatement", "")
    
        # 'return' keyword
        self.mustBe("keyword", "return")
        returnTree.addChild(ParseTree("keyword", "return"))
        
        # Check if there's an expression to return
        if self.current().getValue() != ";":
            expressionTree = self.compileExpression()
            if expressionTree:
                returnTree.addChild(expressionTree)
        
        # Expect a semicolon ';' at the end of the return statement
        self.mustBe("symbol", ";")
        
        return returnTree


    def compileExpression(self):
        """
        Generates a parse tree for an expression
        @return a ParseTree that represents the expression
        """
        exprTree = ParseTree("expression", "")
    
        # Handle a single term (this would be extended to more complex expressions)
        termTree = self.compileTerm()
        if termTree:
            exprTree.addChild(termTree)
        
        # Optionally, handle operators and additional terms
        while self.current().getValue() in ["+", "-", "*", "/", "&", "|", "<", ">", "="]:
            operatorToken = self.current()
            self.next()  # Advance to the next token (after the operator)
            
            # Add the operator to the expression tree
            exprTree.addChild(ParseTree("operator", operatorToken.getValue()))
            
            # Parse the next term and add it to the tree
            termTree = self.compileTerm()
            if termTree:
                exprTree.addChild(termTree)
            else:
                raise ParseException(f"Expected a term after operator {operatorToken.getValue()} but got None")
        
        return exprTree


    def compileTerm(self):
        """
        Generates a parse tree for an expression term
        @return a ParseTree that represents the expression term
        """
        currentToken = self.current()

        # Handle integer constants
        if currentToken.getType() == "integerConstant":
            termTree = ParseTree("integerConstant", currentToken.getValue())
            self.next()  # Move to the next token
            return termTree

        # Handle identifiers (variables or subroutine calls)
        elif currentToken.getType() == "identifier":
            termTree = ParseTree("identifier", currentToken.getValue())
            self.next()  # Move to the next token
            return termTree

        # Handle parentheses expressions (e.g., "(a + b)")
        elif currentToken.getValue() == "(":
            self.mustBe("symbol", "(")
            exprTree = self.compileExpression()
            self.mustBe("symbol", ")")
            return exprTree

        else:
            raise ParseException(f"Unexpected term: {currentToken.getValue()}")


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


    # tokens1 = [
    #     Token("keyword", "class"),
    #     Token("identifier", "Main"),
    #     Token("symbol", "{"),
    #     Token("symbol", "}")
    # ]
    # parser1 = CompilerParser(tokens1)
    # try:
    #     result1 = parser1.compileProgram()
    #     print("Test Case 1 Passed: Valid Class Parsing")
    #     print(result1)
    # except Exception as e:
    #     print("Test Case 1 Failed: Valid Class Parsing")
    #     print(str(e))

        

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

    # tokens2 = [
    #     Token("keyword", "field"),        # 'field' keyword
    #     Token("keyword", "boolean"),      # 'boolean' type
    #     Token("identifier", "test1"),     # first variable
    #     Token("symbol", ","),             # comma
    #     Token("identifier", "test2"),     # second variable
    #     Token("symbol", ";")              # semicolon
    # ]

    # # Initialize the parser with these tokens
    # parser = CompilerParser(tokens2)

    # try:
    #     # Attempt to parse the class variable declaration
    #     result = parser.compileClassVarDec()
    #     print(result)  # This will print the resulting parse tree
    # except Exception as e:
    #     print("ParseException Occurred")
    #     print(str(e))  # Print the error for debugging

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


    # tokens4 = [
    #     Token("keyword", "function"),
    #     Token("keyword", "void"),
    #     Token("identifier", "myFunc"),
    #     Token("symbol", "("),
    #     Token("keyword", "int"),
    #     Token("identifier", "a"),
    #     Token("symbol", ")"),
    #     Token("symbol", "{"),
    #     Token("keyword", "var"),
    #     Token("keyword", "int"),
    #     Token("identifier", "a"),
    #     Token("symbol", ";"),
    #     Token("keyword", "let"),
    #     Token("identifier", "a"),
    #     Token("symbol", "="),
    #     Token("integerConstant", "1"),
    #     Token("symbol", ";"),
    #     Token("symbol", "}")
    # ]

    # parser = CompilerParser(tokens4)
    # try:
    #     result = parser.compileSubroutine()
    #     print(result)
    # except Exception as e:
    #     print(f"Error encountered during parsing: {str(e)}")
    #     # Optionally, print debugging details here



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


    # tokens = [
    # Token("keyword", "constructor"),  # 'constructor' keyword
    # Token("identifier", "Test"),      # Class type 'Test'
    # Token("identifier", "new"),       # Constructor name 'new'
    # Token("symbol", "("),             # Opening parenthesis for parameters
    # Token("symbol", ")"),             # Closing parenthesis for parameters
    # Token("symbol", "{"),             # Opening brace for constructor body
    # Token("symbol", "}"),             # Closing brace for constructor body
    # ]

    # # Initialize the parser with these tokens
    # parser = CompilerParser(tokens)

    # try:
    #     # Attempt to parse the constructor
    #     result = parser.compileSubroutine()
    #     print(result)  # This will print the resulting parse tree
    # except Exception as e:
    #     print("ParseException Occurred")
    #     print(str(e))  # Print the error for debugging

    tokens = [
    Token("keyword", "int"),          # 'int' type
    Token("identifier", "a"),         # variable name 'a'
    ]

    # Initialize the parser with these tokens
    parser = CompilerParser(tokens)

    try:
        # Attempt to parse the parameter list
        result = parser.compileParameterList()
        print(result)  # This will print the resulting parse tree
    except Exception as e:
        print("ParseException Occurred")
        print(str(e)) 