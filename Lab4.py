import ply.lex as lex
# List of token names.   This is always required
operator = []
operand = []
validity = 1
stack = []
count_opert_in_brack = 0
count_operd_in_brack = 0

tokens = (
    'INT',
    'FLOAT',
    'NAME',
    'PLUS',
    'MINUS',
    'TIMES',
    'DIVIDE',
    'LPAREN',
    'RPAREN',
 )
 
 # Regular expression rules for simple tokens    
def t_PLUS(t):
    r'\+'
    global count_opert_in_brack
    operator.append(t.value)
    count_opert_in_brack+=1
    return t

def t_MINUS(t):
    r'\-'
    global count_opert_in_brack
    operator.append(t.value)
    count_opert_in_brack+=1
    return t

def t_TIMES(t):
    r'\*'
    global count_opert_in_brack
    operator.append(t.value)
    count_opert_in_brack+=1
    return t

def t_DIVIDE(t):
    r'\/'
    global count_opert_in_brack
    operator.append(t.value)
    count_opert_in_brack+=1
    return t

def t_LPAREN(t):
    r'\('
    stack.append(t.value)
    return t

# we will check if operands within opening and closing bracket should be greater than 1 and also difference betwn operand and operator must be 1
def t_RPAREN(t):
    r'\)'
    global count_operd_in_brack,count_opert_in_brack,validity
    if(stack.pop()!='('):
        validity=0
    elif(count_operd_in_brack>0 and len(count_operd_in_brack)-len(count_operd_in_brack)!=1):
        validity=0
    else:
        count_opert_in_brack = 0
        count_operd_in_brack = 0
    return t
    
# A regular expression rule with some action code

def t_FLOAT(t):
    r'\d*\.\d+'
    t.type = 'FLOAT'
    t.value = float(t.value)
    operand.append(t.value)
    return t

def t_INT(t):
    r'[0-9]+'
    t.type = 'INT'
    operand.append(t.value)
    return t
    
def t_NAME(t):
    r'[a-zA-z]\w*'
    t.type = 'NAME'
    operand.append(t.value)
    return t
 
# Define a rule so we can track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)
 
 # A string containing ignored characters (spaces and tabs)
t_ignore  = ' \t'
 
 # Error handling rule
def t_error(t):
    print("\nIllegal character '%s'" % t.value[0])
    t.lexer.skip(1)
 
 # Build the lexer
lexer = lex.lex()
 
#print(type(lexer)) 
#print(lexer)
#To use the lexer, you first need to feed it some input text using its input() method. After that, repeated calls to token() produce tokens. The following code shows how this works:
 
 # Test it out
#data = '''(a+b-4cc'''
data = input("Please enter the expression : ")
 
 # Give the lexer some input
lexer.input(data)
tokens = [] 
 # Tokenize
while True:
    tok = lexer.token()
    if not tok: 
        break      # No more input
    tokens.append(tok)
    if(validity==0):
        break
    #print(tok)

if(len(stack)!=0):
    validity = 0

if(len(operand)<=len(operator)):
    validity = 0

if(validity==1):
    print("Given Expression is valid")
    print("Operator : ",operator)
    print("Operand : ",operand)    
else:
    print("Invalid expression")