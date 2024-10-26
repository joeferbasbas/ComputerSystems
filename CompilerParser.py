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
        
        print(f"Class name obtained: {classNameToken.getValue()}")
        classTree = ParseTree("class", "") 
        classTree.addChild(ParseTree("identifier", classNameToken.getValue()))
        
        print("Checking for opening '{'...")
        self.mustBe("symbol", "{")
        
        # Here you might add code to handle class body
        print("Checking for closing '}'...")
        self.mustBe("symbol", "}")

        print("Class parsing completed.")
        return classTree

    

    def compileClassVarDec(self):
        """
        Generates a parse tree for a static variable declaration or field declaration
        @return a ParseTree that represents a static variable declaration or field declaration
        """
        if not (self.have("keyword", "static") or self.have("keyword", "field")):
            raise ParseException(f"Expected 'static' or 'field', found {self.current().getType()} {self.current().getValue()}")


        declarationType = self.current().getValue()
        declarationTree = ParseTree(declarationType, "")
        self.next()

        typeToken = self.mustBe("identifier", None)
        declarationTree.addChild(ParseTree('type', typeToken.getValue()))

        while True:
            varNameToken = self.mustBe("identifier", None)
            declarationTree.addChild(ParseTree("varName", varNameToken.getValue()))
            
            self.next()
            if self.current().getValue() == ';':
                self.next()
                break
            elif self.current().getValue() == ',':
                self.next()
            else:
                raise ParseException("expected , or ; but found " + self.current().getValue())
        return declarationTree


      
    

    def compileSubroutine(self):
        """
        Generates a parse tree for a method, function, or constructor
        @return a ParseTree that represents the method, function, or constructor
        """
        return None 
    
    
    def compileParameterList(self):
        """
        Generates a parse tree for a subroutine's parameters
        @return a ParseTree that represents a subroutine's parameters
        """
        return None 
    
    
    def compileSubroutineBody(self):
        """
        Generates a parse tree for a subroutine's body
        @return a ParseTree that represents a subroutine's body
        """
        return None 
    
    
    def compileVarDec(self):
        """
        Generates a parse tree for a variable declaration
        @return a ParseTree that represents a var declaration
        """
        return None 
    

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
            raise ParseException("No more token to parse")


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
        if not self.have(expectedType, expectedValue):
            currToken = self.current()
            raise ParseException(f"Expected {expectedType} '{expectedValue}', but found {currToken.getType()} '{currToken.getValue()}'")
        self.next()
        return self.current()

if __name__ == "__main__":


    """ 
    Tokens for:
        class MyClass {
        
        }
    """
    # tokens = []
    # tokens.append(Token("keyword","class"))
    # tokens.append(Token("identifier","MyClass"))
    # tokens.append(Token("symbol","{"))
    # tokens.append(Token("symbol","}"))

    # parser = CompilerParser(tokens)

    


    # try:
    #     result = parser.compileProgram()
    #     print(result)
    # except ParseException as e:
    #     print(f"Error Parsing: {e}")


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

