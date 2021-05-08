from itertools import groupby

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
    
    for i in non_terminals: # this loop is used to traverse the whole list one-time for simple analysis
        for z,j in gram.items(): # this loop is used to traverse the right hand side of the grammar
            temp = j.split('|')
            for k in temp: # this loop is used to traverse the splitted right hand side og the grammar
                l = 0
                while(l!=len(k)):
                    if(k[l]==i):
                        l+=1
                        if(l>=len(k)):
                            if(i!=z):
                                remaining.setdefault(i,[]).append(z)
                            else:
                                follow.setdefault(i,[]).append('$')
                        elif(k[l].isalnum()):
                            if(k[l].islower()):
                                follow.setdefault(i,[]).append(k[l])
                            else:
                                flag=0
                                x = k[l]
                                x1 = x
                                while(flag==0):
                                    x = x1
                                    for p in first_key[x]:
                                        if(p=='#'):
                                            l+=1
                                            if(l>=len(k)):
                                                if(i!=z):
                                                    remaining.setdefault(i,[]).append(z)
                                                else:
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
                if(len(remaining[j])==0):
                    for l in follow[j]:
                        follow.setdefault(i,[]).append(l)
                    remaining[i][remaining[i].index(j)] = 'del'
            
            remaining[i] = list(filter(lambda val : val!='del',remaining[i]))
            
            if(len(remaining[i])==0):
                queue[queue.index(i)] = 'del'
            
        queue = list(filter(lambda val : val!='del',queue))
    
    return follow            

def parsing_table(gram,first_key,follow_key):
    terminals = []
    table= {}
    for i in first_key.keys():
        for j in first_key[i]:
            if(j=='#'):
                terminals.append('$')
            else:
                terminals.append(j)
        for j in follow_key[i]:
            terminals.append(j)
    terminals = set(terminals)
    
    #print(terminals)
    for i,j in gram.items():
        for k in j.split('|'):
            #print(i," => ",k)
            if(k=='#'):
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
    
    parse_table = []
    for i in range(len(gram.keys())):
        row = []
        for j in range(len(terminals)):
            row.append("-")
        parse_table.append(row)
    for i in table.keys():
        for j in table[i]:
            parse_table[production_index[j[0]]][terminal_index[i]] = "{} => {}".format(j[0],j[1])
    
    print("\n\nThe Parse Table will be : ")
    print("",end="\n\t\t")
    count = 0
    for i in terminals:
        print(i,end="\t\t|\t\t")
    print("____________________________________________________________________________________________________\n")
    
    
    for i in gram.keys():
        print(i,end='')
        for j in parse_table[production_index[i]]:
            if(j=='-'):
                print("\t\t{}\t\t|".format(j),end="")
            else:
                print("\t\t{}\t|".format(j),end="")
        print("\n")
    return table

def check_validity(s,table,start_symbol):
    stack = s.split(" ")
    stack.append('$')
    #print(stack)
    #print(start_symbol)
    
    stack_grammar = ['$']
    stack_grammar.append(start_symbol)
    
    flag=0
    accepted = False
    print("\nString \t\t\t\t\t\t\t\tGrammar rules \t\t\t\t\t\t Production used\n")
    while(flag==0):
        print(stack,end="\t  ==>  \t")
        print(stack_grammar,end="")
        if(stack[0]==stack_grammar[len(stack_grammar)-1]):
            #print("Characters matched")
            if(stack[0]=='$'):
                accepted = True
                flag=1
            else:
                stack.pop(0)
                stack_grammar.pop(len(stack_grammar)-1)
                print()
        elif(stack_grammar[len(stack_grammar)-1]=='#'):
            stack_grammar.pop(len(stack_grammar)-1)
            print()
        else:
            found=False
            try:
                for x in table[stack[0]]:
                    if(found==False):
                        if(x[0]==stack_grammar[len(stack_grammar)-1]):
                            found = True
                            print("\t\t\t => by using( ",x[0]," => ",x[1]," )")
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
        #print(stack)
        #print(stack_grammar)
    if(accepted==True):
        print('\n\nThe string "{}" is valid'.format(s))
    else:
        print("\n\nInvalid string")
                            
                    
          
gram = {'E':'TR',
        'R':'+TR|#',
        'T':'FY',
        'Y':'*FY|#',
        'F':'(E)|id'
        }

s = 'id + id * id'

#s = 'id + id * id + id'

#s = 'id + id * ( id + id ) * id'

#s = '( ( id * id ) + id ) * id'

# below is the example of invalid string
s = 'id + id * ( id / id'

print("\nIn this code we have taken epsilon='#'")

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

table = parsing_table(gram, first_key, follow_key)
print("\n\nThe parsing table will be : ")
# write code to draw paesing table
for i in table.keys():
    table[i].sort()
    table[i] = list(num for num,_ in groupby(table[i]))
    print(i," => ",table[i])

check_validity(s,table,next(iter(gram)))
        