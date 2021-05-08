import ply.lex as lex
import ply.yacc as yacc
flag=0
s=input("enter the string : ")
count_of_a = 0
count_of_b = 0

print()
count_of_a = 0
count_of_b = 0

# List of token names.   This is always required
tokens = (
    'A',
    'B'
 )

def t_A(t):
    r'a'    
    return t

def t_B(t):
    r'b'
    return t

# Define a rule so we can track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)
 
 # A string containing ignored characters (spaces and tabs)
t_ignore  = ' \t'
 
 # Error handling rule
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)
 
 # Build the lexer
lexer = lex.lex()


def p_check(p):
    '''
    check : string 
    '''

def p_string(p):
    '''
    string : a string
            | string b
            | empty
    '''
    p[0]=p[1]
    #print(p[1])

def p_a(p):
    '''
    a : A
    '''
    p[0] = p[1]
    print("Received token : ",p[1])
    
    global count_of_a
    count_of_a+=1

def p_b(p):
    '''
    b : B
    '''
    p[0] = p[1]  
    print("Received token : ",p[1])
    
    global count_of_b
    count_of_b+=1
    

def p_empty(p):
    '''
    empty : 
    '''
    p[0]= ''
    
def p_error(p):
    print("\n\nString NOT VALIDATED \n\nThere can be two reasons reasons")
    print("\t1) Either 'a' comes after 'b'")
    print("\t2) Either there is no 'b' present ")
    global flag
    flag=1
    
        
parser=yacc.yacc()

parser.parse(s) 

if(flag==0):
    if(count_of_a>=0 and count_of_b>0):
        print("\n\nString ACCEPTED")
        print("\n\nThe count of a is : ",count_of_a)
        print("\nThe count of b is : ",count_of_b)
        print()
    else:
        print("\n\nString REJECTED")