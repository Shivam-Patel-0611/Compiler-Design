def is_operator_precedence(gram):
    is_op_pre = True
    for i,j in gram.items():
        temp = j.split("|")
        #loop to check the consecutive non_terminal or Null production
        for k in temp:
            if(k=='#'):
                is_op_pre = False
                break
            else:
                for m in range(0,len(k)-1):
                    if(k[m].isalnum()):
                        if(k[m+1].isalnum()):
                            if(k[m].isupper() and k[m+1].isupper()):
                                is_op_pre = False
                                break
                        else:
                            m=m+2                
        if(is_op_pre==False):
            break
    #print(is_op_pre)
    return is_op_pre


def leading_and_trailing(gram):
    leading = {}
    trailing = {}
    temp_storage = {}
    
    for i,j in gram.items():
        temp = j.split("|")
        for k in temp:
            #taking individual character from grammar rule using iter
            x = iter(k)
            y = next(x)
            if(len(k)>1):
                z = next(x)
            if(y.isalnum()):
                if(y.islower()):
                    leading.setdefault(i,[]).append(y)
                else:
                    if(len(k)>1):
                        leading.setdefault(i,[]).append(z)
                    if(y!=i):
                        temp_storage.setdefault(i,[]).append(y)
            else:
                leading.setdefault(i,[]).append(y)
                
    for i,j in temp_storage.items():
        for k in temp_storage[i]:
            for l in leading[k]:
                leading.setdefault(i,[]).append(l)
                
    #Running this second time because if some non_terminals are missed fue to FCFS
    #they can be added in second loop
    for i,j in temp_storage.items():
        for k in temp_storage[i]:
            for l in leading[k]:
                leading.setdefault(i,[]).append(l)
                
    print("\n1) The leading of the Operator precedence grammar is : \n")            
    for i in leading.keys():
        leading[i] = set(leading[i])
        leading[i] = list(leading[i])
        print(i," : ",leading[i])
    
    
    temp_storage = {}
    # Now this part is for the trailing part which is exactly same as leading part
    for i,j in gram.items():
        temp = j.split("|")
        for k in temp:
            k = k[::-1] # reversing the string and doing the same calculation
            #taking individual character from grammar rule using iter
            x = iter(k)
            y = next(x)
            if(len(k)>1):
                z = next(x)
            if(y.isalnum()):
                if(y.islower()):
                    trailing.setdefault(i,[]).append(y)
                else:
                    if(len(k)>1):
                        trailing.setdefault(i,[]).append(z)
                    if(y!=i):
                        temp_storage.setdefault(i,[]).append(y)
            else:
                trailing.setdefault(i,[]).append(y)
    
    for i,j in temp_storage.items():
        for k in temp_storage[i]:
            for l in trailing[k]:
                trailing.setdefault(i,[]).append(l)
                
    #Running this second time because if some non_terminals are missed fue to FCFS
    #they can be added in second loop
    for i,j in temp_storage.items():
        for k in temp_storage[i]:
            for l in trailing[k]:
                trailing.setdefault(i,[]).append(l)
                
    print("\n2) The trailing of the Operator precedence grammar is : \n")            
    for i in trailing.keys():
        trailing[i] = set(trailing[i])
        trailing[i] = list(trailing[i])
        print(i," : ",trailing[i])
    



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



'''
gram = {'S':'(L)|a',
        'L':'L,S|S'
        }


gram = {'A':'abB|dAe|a',
        'B':'aAc|de'
        }

'''



gram = {'E':'E*T|T',
        'T':'T+F|F',
        'F':'(E)|a'
        }

'''
gram = {'A':'Bbc|aA',
        'B':'dB|e'
        }



gram = {'A':'BbAd|aB|cd',
        'B':'AeBc|BbA|b'
        }

'''

check_validity = is_operator_precedence(gram)

if(check_validity):
    print("\nYes, The grammar is Operator Precedence grammar")
    leading_and_trailing(gram)
else:
    print("\nNOT an Operator Precedence Grammar")