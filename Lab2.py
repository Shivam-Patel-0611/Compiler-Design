# -*- coding: utf-8 -*-
"""
Created on Mon Feb 22 17:30:22 2021

@author: Shivam Patel
@Rollno: 18BCP104
@Branch: CE'18'
"""

from itertools import groupby
from tabulate import tabulate

def add_follow_to_non_varibale(whose,from_whom,follow):
    follow[from_whom] = list(set(follow[from_whom]))
    for l in follow[from_whom]:
        follow.setdefault(whose,[]).append(l)
    return follow


def remove_non_determinism(gram):   
    new_production_start = 'Z'
    new_grammar = {}
    remaining = {}
    for i in gram.keys():
        temp = gram[i].split('|')
        for j in temp:
            remaining.setdefault(i,[]).append(j)

    #grammar_com = {}
    
    g = 0
    while(g!=len(remaining.keys())):
        i = list(remaining.keys())[g]
        j = remaining[i]
        new_grammar[i] = []
        g+=1
        
        temp = j
        false = [False]*len(j)
        dict_of_visited = dict(zip(j,false))
        common = {}
        for k in j:
            if(dict_of_visited[k]==False):
                dict_of_visited[k]==True
                dict_of_common = dict(zip(j,false))
                #if_any_common_present = False
                common = {}
                
                for l in j:
                    if(dict_of_visited[k]==False and l!=k):
                        m = 0
                        com_string = ''
                        while(m<min(len(k),len(l))):
                            if(k[m]==l[m]):
                                com_string += k[m]
                                #if_any_common_present = True
                                m+=1
                                dict_of_common[l] = True
                                dict_of_visited[l] = True
                            else:
                                break
                        lst = []
                        lst.append(j.index(k))
                        lst.append(j.index(l))
                        
                        if(com_string!=''):
                            for x,y in dict_of_common.items():
                                if(y==True):
                                    lst.append(j.index(x))
                            common[com_string] = list(set(lst))
                
                if(len(common.keys())==0):
                    new_grammar.setdefault(i,[]).append(k)
                else:
                    test_set = common.keys()
                    result = min(test_set,key=len)
                    
                    new_grammar.setdefault(i,[]).append(result+new_production_start)
                    for q in common[result]:
                        remaining_string = j[q].partition(result)[2]
                        if(len(remaining_string)==0):
                            new_grammar.setdefault(new_production_start,[]).append('#')
                        else:
                            new_grammar.setdefault(new_production_start,[]).append(remaining_string)
                    
                    remaining[new_production_start] = new_grammar[new_production_start]
                    new_production_start = chr(ord(new_production_start)-1)
                
    return new_grammar

def first(gram):
    first_key = {}
    queue = []
    
    remaining = {}
    for i in gram.keys():
        temp = gram[i].split('|')
        for j in temp:
            remaining.setdefault(i,[]).append(j)
    
    for i in remaining.keys():
        first_key[i] = []
        for j in remaining[i]:
            if(j=='id'):
                first_key.setdefault(i,[]).append(j)
                remaining[i][remaining[i].index(j)] = 'del'
            elif(j[0].isalnum()):
                if(j[0].islower()):
                    first_key.setdefault(i,[]).append(j[0])    
                    remaining[i][remaining[i].index(j)] = 'del'
                else:
                    if(i not in queue):    
                        queue.append(i)
            else:
                first_key.setdefault(i,[]).append(j[0])
                remaining[i][remaining[i].index(j)] = 'del'
            
        remaining[i] = list(filter(lambda val : val!='del',remaining[i]))
    
    while len(queue)!=0:
        for i in queue:
            for j in remaining[i]:
                flag=0
                x=0
                x1=0
                while(flag==0):
                    x1=x
                    if(j[x].islower()):
                        first_key.setdefault(i,[]).append(j[x])
                        remaining[i][remaining[i].index(j)] = 'del'
                        flag=1
                    else:
                        if(len(first_key[j[x]])!=0 and len(remaining[j[x]])==0):
                            for k in first_key[j[x]]:
                                if(k=='#'):
                                    x+=1
                                else:
                                    first_key.setdefault(i,[]).append(k)
                        else:
                            flag=1
                            
                        if(x==x1 and flag==1):
                            flag=1
                        elif(x==x1 and flag==0):
                            remaining[i][remaining[i].index(j)] = 'del'
                            flag=1
                        elif('#' not in first_key[j[x1]] and len(first_key[j[x1]])>0):
                            remaining[i][remaining[i].index(j)] = 'del'
                            flag=1
                        elif(x==len(j)):
                            first_key.setdefault(i,[]).append("#")
                            remaining[i][remaining[i].index(j)] = 'del'
                            flag=1
            
            remaining[i] = list(filter(lambda val : val!='del',remaining[i]))
            if(len(remaining[i])==0):
                queue[queue.index(i)] = 'del'
            
        queue = list(filter(lambda val : val!='del',queue))   
    return first_key

def follow(gram,first_key):    
    non_terminals = []
    queue = []
    follow = {}
    remaining = {}
    for i in first_key.keys():
        non_terminals.append(i)
        remaining[i] = []
        follow[i] = []
    
    follow.setdefault(non_terminals[0],[]).append('$')
    '''
    print()
    print(gram)
    print()
    print(non_terminals)
    print()
    print(remaining)
    print()
    print(follow)
    '''
    
    for i in non_terminals: # this loop is used to traverse the whole list one-time for simple analysis
        #print("\n\nItem changed to : ",i)
        #print("\n\n")
        for z,j in gram.items(): # this loop is used to traverse the right hand side of the grammar
            temp = j.split('|')
            for k in temp: # this loop is used to traverse the splitted right hand side og the grammar
                #print("=>",k)
                l = 0
                while(l<len(k)):
                    #print("==>",k[l])
                    if(k[l]==i):
                        #print("Char matched")
                        l+=1
                        if(l>=len(k)):
                            if(i!=z):
                                #print("===>length greater and DIFF element on left side")
                                remaining.setdefault(i,[]).append(z)
                            else:
                                #print("===>lebgth greater and SAME elemnt on left side")
                                follow.setdefault(i,[]).append('$')
                        elif(k[l].isalnum()):
                            if(k[l].islower()):
                                #print("following char is in lower case")
                                follow.setdefault(i,[]).append(k[l])
                                l+=1
                            else:
                                #print("following char is in Upper case")
                                flag=0 # used for exiting loop for calculating the follows
                                x = k[l]
                                x1 = x
                                #print(x)
                                while(flag==0):
                                    x = x1
                                    for p in first_key[x]:
                                        if(p=='#'):
                                            #print("Hash encountered")
                                            l+=1
                                            if(l>=len(k)):
                                                if(i!=z):
                                                    #print("===>length greater and DIFF element on left side")
                                                    remaining.setdefault(i,[]).append(z)
                                                else:
                                                    #print("===>length greater and SAME element on left side")
                                                    follow.setdefault(i,[]).append('$')
                                                flag=1    
                                            elif(k[l].isalnum()):
                                                if(k[l].islower()):
                                                    follow.setdefault(i,[]).append(k[l])
                                                    flag=1
                                                else:
                                                    x1 = k[l]
                                            else:
                                                follow.setdefault(i,[]).append(k[l])
                                                flag=1
                                        else:
                                            follow.setdefault(i,[]).append(p)
                                    if('#' not in first_key[x]):
                                        flag=1
                        else:
                            follow.setdefault(i,[]).append(k[l])
                    else:
                        l+=1;
    
    for i in remaining.keys():
        if(len(remaining[i])!=0):
            queue.append(i)
            
    while(len(queue)!=0):
        for i in queue:
            temp = remaining[i]
            for j in temp:                
                cycle_exist = True
                seen = []
                initial = j
                while (initial not in seen) and (initial is not None):
                    seen.append(initial)
                    if(len(remaining[initial])==0):
                        cycle_exist = False
                        break
                    initial = remaining[initial][0]
                    
                if(cycle_exist==True and len(seen)>1):
                    #print("Yes its true")
                    remaining[i][remaining[i].index(j)] = 'del'
                    remaining[i] = list(filter(lambda val : val!='del',remaining[i]))
                else:
                    add_follow_to_non_varibale(i, j, follow)
                    remaining[i][remaining[i].index(j)] = 'del'
                
            remaining[i] = list(filter(lambda val : val!='del',remaining[i]))
            
            if(len(remaining[i])==0):
                queue[queue.index(i)] = 'del'
            
        queue = list(filter(lambda val : val!='del',queue))
    
    return follow            

def parsing_table(gram,first_key,follow_key):
    is_LL1 = True
    terminals = []
    table= {}
    # adding all known terminals covered in first and follow and then removing the duplicates
    for i in first_key.keys():
        for j in first_key[i]:
            if(j=='#'):
                terminals.append('$')
            else:
                terminals.append(j)
        for j in follow_key[i]:
            terminals.append(j)
    terminals = set(terminals)
    terminals = list(terminals)
    terminals.insert(0,'Symbols')
    
    for i,j in gram.items(): # accessing the right hand side of the grammar and splitting it
        table.setdefault('Symbols',[]).append(i)    
        for k in j.split('|'):
            if(k=='#'): # if production is null than add that production to the follow of the left side
                for l in follow_key[i]:
                    table.setdefault(l,[]).append([i,k])
            elif(k=='id'):
                table.setdefault(k,[]).append([i,k])
            else:
                z=0
                z1=z
                while(not k[z].isalpha()):
                    table.setdefault(k[z],[]).append([i,k])
                    z+=1
                    break
                
                if(z==0):
                    flag=0
                    while(flag==0):
                        #print("hello")
                        z = z1
                        if(z>=len(k)):
                            flag=1
                        elif(k[z].islower()):
                            table.setdefault(k[z],[]).append([i,k])
                            flag=1
                        elif(k[z].isupper()):
                            #print("upper")
                            for l in first_key[k[z]]:
                                if(l=='#'):
                                    #print("hash encountered")
                                    z1+=1
                                else:
                                    table.setdefault(l,[]).append([i,k])
                            if('#' not in first_key[k[z]]):
                                flag=1
                        else:
                            table.setdefault(k[z],[]).append([i,k])
                            flag=1
                    
                    if(z==len(k)):
                        for l in follow_key[i]:
                            table.setdefault(l,[]).append([i,k])
    for i in table.keys():
        table[i].sort()
        table[i] = list(num for num,_ in groupby(table[i]))
    # Code to print parsing table
    
    terminal_index = {}
    production_index = {}
    
    count = 0
    for i in terminals:
        terminal_index[i] = count
        count+=1
    
    count = 0
    for i in gram.keys():
        production_index[i] = count
        count+=1
    #print(table)
    #print()
    
    parse_table = []
    for i in range(len(gram.keys())):
        row = []
        for j in range(len(terminals)):
            row.append("-")
        parse_table.append(row)
    for i in table.keys():
        if(i!='Symbols'):
            for j in table[i]:
                #parse_table[production_index[j[0]]][terminal_index[i]] = "{} => {}".format(j[0],j[1])
                if(parse_table[production_index[j[0]]][terminal_index[i]]!='-'):
                    is_LL1 = False
                    parse_table[production_index[j[0]]][terminal_index[i]] += "\n{} => {}".format(j[0],j[1])
                else:
                    parse_table[production_index[j[0]]][terminal_index[i]] = "{} => {}".format(j[0],j[1])
    for j in table['Symbols']:
        parse_table[production_index[j]][0] = j
    
    table_representation = tabulate(parse_table,headers = terminals, tablefmt='orgtbl')
    print("\n\n",table_representation)
    
    return table,is_LL1

def check_validity(s,table,start_symbol):
    stack = []
    for i in s:
        stack.append(i)
    stack.append('$')
    #print(stack)
    #print(start_symbol)
    
    stack_grammar = ['$']
    stack_grammar.append(start_symbol)
    
    flag=0
    accepted = False
    content = []
    #print("\nString \t\t\t\t\t\t\t\tGrammar rules \t\t\t\t\t\t Production used\n")
    while(flag==0):
        l = []
        #print(stack,end="\t  ==>  \t")
        #print(stack_grammar,end="")
        stack.reverse()
        l.append(''.join(stack))
        l.append(''.join(stack_grammar))
        stack.reverse()
        if(stack[0]==stack_grammar[len(stack_grammar)-1]):
            #print("Characters matched")
            if(stack[0]=='$'):
                accepted = True
                flag=1
            else:
                stack.pop(0)
                stack_grammar.pop(len(stack_grammar)-1)
                #print()
        elif(stack_grammar[len(stack_grammar)-1]=='#'):
            stack_grammar.pop(len(stack_grammar)-1)
            #print()
        else:
            found=False
            try:
                for x in table[stack[0]]:
                    if(found==False):
                        if(x[0]==stack_grammar[len(stack_grammar)-1]):
                            found = True
                            #print("\t\t\t => by using( ",x[0]," => ",x[1]," )")
                            l.append(x[0]+" => "+x[1])
                            stack_grammar.pop(len(stack_grammar)-1)
                            if(x[1]=='id'):
                                stack_grammar.append(x[1])
                            else:
                                for i in range(0,len(x[1])):
                                    stack_grammar.append(x[1][len(x[1])-i-1])
            except KeyError:
                accepted = False
                flag=1
            if(found==False):
                flag=1
        content.append(l)
        #print(stack)
        #print(stack_grammar)
        
    # to print the validity steps in tabular format
    Heading = ['String','Grammar Rules','Production used']
    table_representation = tabulate(content,headers = Heading, tablefmt='orgtbl')
    print("\n\n",table_representation)
    
    if(accepted==True):
        print('\n\nThe string "{}" is valid'.format(s))
    else:
        print("\n\nInvalid string")


print("\nIn this code we have taken epsilon='#'")


# Predefined Grammar rules
'''
gram = {'S':'ACB|CbB|Ba',
        'A':'da|BC',
        'B':'g|#',
        'C':'h|#'
        }
s = 'ga'
'''

'''
gram = {'E':'TR',
        'R':'+TR|#',
        'T':'FY',
        'Y':'*FY|#',
        'F':'(E)|id'
        }
'''

'''
gram = {'S':'ASb|C',
        'A':'a',
        'C':'cC|#'
        }
s = 'acb'

'''

'''
gram = {'S':'ABCDE',
        'A':'a|#',
        'B':'b|#',
        'C':'c',
        'D':'d|#',
        'E':'e|#'
        }
s = 'abde'
'''

'''
gram = {'S':'aBDh',
        'B':'cC',
        'C':'bC|#',
        'D':'EF',
        'E':'g|#',
        'F':'f|#'
        }
s = 'acgh'
'''

'''
gram = {'S' : 'AaAb|BbBa',	
        'A' : '#',
        'B' : '#'
        }
s = 'ab'
'''


# Predefined left factored Grammar rules


gram = {'S':'iEtS|iEtSeS|a',
        'E':'b'
        }


'''
gram = {'S':'bSSaaS|bSSaSb|bSb|a'
        }
'''

'''
gram = {'S':'aSSbS|aSaSb|abb|b'
        }
'''

# Code to take input from terminal:
'''
print("\n\nRules:")
print("i) Production should be in space separated format and only one production for single terminals in one line")
print("For eg:")
print("If original production is like S -> aBc|Bbc then enter")
print("Total productions : 2")      
print("S : aBc")
print("S : Bbc")

gram = {}

n = int(input("Enter total number of productions : "))
for i in range(n):
    s = input("Rule {} => ".format(i+1))
    l = s.split(" ")
    gram.setdefault(l[0],[]).append(l[2])

for i in gram.keys():
    gram[i] = "|".join(gram[i])

s = input("Please enter the string to be validated : ")
print(gram)
'''



gram = remove_non_determinism(gram)

print("\nSo after removing left Factoring, the new_grammar will be : ")
for i in gram.keys():
    gram[i] = '|'.join(gram[i])
    print(i," => ",gram[i])
    #print(gram[i])

#print(gram)

first_key = first(gram)
print("\nThe first(s) of various symbols is : ")
for i in first_key.keys():
    first_key[i] = set(first_key[i])
    print("{ ",i," : ",list(first_key[i]),"}")



follow_key = follow(gram,first_key)
print("\nThe follow of various symbols is : ")
for i in follow_key.keys():
    follow_key[i] = set(follow_key[i])
    print("{ ",i," : ",list(follow_key[i]),"}")

table,is_LL1 = parsing_table(gram, first_key, follow_key)
print("\n\nThe parsing table will be : ")
# write code to draw paesing table
for i in table.keys():
    table[i].sort()
    table[i] = list(num for num,_ in groupby(table[i]))
    print(i," => ",table[i])

if(is_LL1):
    print("\nYes LL1 is possible")
    check_validity(s,table,next(iter(gram)))
else:
    print("\nNot Possible to construct parser as there are multiple entries in table")

               