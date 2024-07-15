################################### CONSTANTS #############################3
DIGITS = '0123456789'
NOERROR = 'NOERROR'

################################## ERRORS ############################
class Error:
    def __init__(self, posStart, posEnd, errorName, details) -> None:
        self.posStart = posStart
        self.posEnd = posEnd
        self.errorName = errorName
        self.details = details

    def asString(self):
        result = f'{self.errorName}:  {self.details}'
        result += f'File {self.posStart.fn}, line {self.posStart.line + 1}'
        return result
    
class IllegalCharError (Error):
    def __init__(self, posStart, posEnd, details) -> None:
        super().__init__(posStart, posEnd, 'Illegal Character', details)

################################ POSITION #############################
class Position:
    def __init__(self, index, line, column, fn, ftxt) -> None:
        self.index = index
        self.line = line
        self.column = column
        self.fn = fn
        self.ftxt = ftxt

    def advance(self, currentChar):
        self.index += 1
        self.column += 1

        if currentChar == '\n':
            self.line += 1
            self.column = 0

    def copy(self):
        return Position(self.index, self.line, self.column, self.fn, self.ftxt)

################################### TOKENS ##############################
TT_INT = 'INT'
TT_FLOAT = 'FLOAT'
TT_PLUS = 'PLUS'
TT_MINUS = 'MINUS'
TT_MUL = 'MUL'
TT_DIV = 'DIV'
TT_LPAREN = 'LPAREN'
TT_RPAREN = 'RPAREN'

class Token:
    def __init__(self, type_, value=None) -> None:
        self.type = type_
        self.value = value

    def __repr__(self) -> str:
        if self.value:
            return f'{self.type}:{self.value}'
        return f'{self.type}'
    
####################################### LEXER ##############################
class Lexer:
    def __init__(self, fn, text) -> None:
        self.fn = fn
        self.text = text
        self.pos = Position(-1, 0, -1, fn, text)
        self.currentChar = None

    def advance(self):
        self.pos.advance(self.currentChar)
        self.currentChar = self.text[self.pos.index] if self.pos.index < len(self.text) else None

    def makeTokens(self):
        tokens = []
        self.advance()
        while self.currentChar != None:
            if self.currentChar in ' \t':
                self.advance()
            elif self.currentChar in '+':
                tokens.append(Token(TT_PLUS))
                self.advance()
            elif self.currentChar in '-':
                tokens.append(Token(TT_MINUS))
                self.advance()
            elif self.currentChar in '*':
                tokens.append(Token(TT_MUL))
                self.advance()
            elif self.currentChar in '/':
                tokens.append(Token(TT_DIV))
                self.advance()
            elif self.currentChar in '(':
                tokens.append(Token(TT_LPAREN))
                self.advance()
            elif self.currentChar in ')':
                tokens.append(Token(TT_RPAREN))
                self.advance()
            elif self.currentChar in DIGITS:
                tokens.append(self.makeNumbers())
            else:
                posStart = self.pos.copy()
                char = self.currentChar
                self.advance()
                return [], IllegalCharError(posStart, self.pos, "'" + char + "' ")

        return tokens, NOERROR
    
    def makeNumbers(self):
        numStr = ''
        dotCount = 0

        while self.currentChar != None and self.currentChar in DIGITS + '.':
            if self.currentChar == '.':
                if dotCount == 1: 
                    break
                dotCount += 1
                numStr += '.'
            else:
                numStr += self.currentChar

            self.advance()

        if dotCount == 0:
            return Token(TT_INT, int(numStr))
        else:
            return Token(TT_FLOAT, float(numStr))
        
############################### RUN #######################
def run(fn, text):
    lexer = Lexer(fn, text)
    tokens, error = lexer.makeTokens()
    return tokens, error