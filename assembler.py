# this is a code that convert assembly code into machine code using python language 
# inputs in this program could be given from file or in terminal
# push pop sub add or xor jmp ind dec and inc are instructions that are supported in here
phase2Array =[]
def check_error(): # an function to check if commands are correct from some syntax mistake and if not exit the program
    for i in range(length_instruction):
        for j in range(len (instruction2[i])):
            if instruction2[i][0] == "add" or instruction2[i][0] == "sub" or instruction2[i][0] == "and" or instruction2[i][0] == "or" or instruction2[i][0] == "xor" : # check if it's correct instruction 
                if len(instruction2[i])==3 and ((len(instruction2[i][2]) == len(instruction2[i][1])) or len(instruction2[i][2]) == len(instruction2[i][1]) + 2 or len(instruction2[i][2]) + 2 == len(instruction2[i][1])) and (instruction2[i][1][-1] == instruction2[i][2][-1]):
                        return # check if it has coreect size of two reg and also have 2 registers 
            elif instruction2[i][0] == "push" or  instruction2[i][0] == "pop" or  instruction2[i][0] == "inc" or  instruction2[i][0] == "dec":
                if len(instruction2[i]) == 2:
                    return # check if has 1 reg after these instructions
            elif instruction2[i][0] == "jmp" or instruction2[i][0][-1]== ":":
                if instruction2[i][0] == "jmp" :
                    if len(instruction2[i]) == 2:
                        return # check if has 1 reg after these instructions
            else:
                print("something is wrong!")
                exit() # if not exit from program 


input_type = input("Enter 'T' for terminal input or 'F' for file input: ").lower() # ask the user that how it want to insert the codes
instruction2 = [] 
if input_type == 't': # if from terminal take take input from user
    print("Enter the assembly command: ")
    while True:
        try:
            instruction1 = input() 
            instruction2.append(instruction1) 
        except EOFError:
            break  # insert code until EOF
    
elif input_type == 'f': # if from file 
    file_path = input("Enter the file path: ") 
    # get the path of file from user
    try :
        with open(file_path, 'r') as file:
            for line in file:  # oopoen the file and read the file line to line until the end
                instruction1 = line.replace("\n" , "")
                instruction2.append(instruction1)
    except FileNotFoundError:
        print("File not found.") # if the path is invalid print the error
        exit
else:
    print("Invalid input type. Please enter 'T' or 'F'.") # if user enter anything beside t and f print this error
    exit()


instruction2= "\n".join(instruction2).lower() # lower case all the instructions and registers
instruction2 = instruction2.replace("," , " ").split("\n") # remove , from between of instructions and every line will split to an array
length_instruction = len(instruction2)
for i in range (length_instruction):
    instruction2[i] = instruction2[i].split() # every line split into an array with registers and instructions
print(instruction2)
check_error() # check if there is an syntax error in code to exit the program



labels = []
labels_line =[]
k=0
for i in range (0, length_instruction):   # check every line of instruction to find the labels with : this  and save the label and line that label is in 2 arrays
    for j in range (0, len (instruction2[i])):
        if len(instruction2[i][j]) > 0 and instruction2[i][j][-1] == ":":
            labels.append(instruction2[i][j].replace(":",""))
            labels_line.append(i)
            k+=1

#print(labels)
stackk ="0x0" # creat the stack numbers for print at the end


def findregrm_mod1(n):# find r/m for memory 
    if instruction[n] == "[eax]": # if it has memory 
        Rm_mod[7]=0
    elif instruction[n] == "[ecx]":
        Rm_mod[7] =1
    elif instruction[n] == "[edx]":
        Rm_mod[6] =1
    elif instruction[n] == "[ebx]":
        Rm_mod[6] =1
        Rm_mod[7] =1
    elif instruction[n] == "[esi]":
        Rm_mod[5] =1
        Rm_mod[6] =1
    elif instruction[n] == "[edi]":
        Rm_mod[6] =1
        Rm_mod[5] =1
        Rm_mod[7] =1
    else:
        print("something is wrng!")
        exit()

def reg(n): # find reg base on the other one with reg or second one in all reg
    if (instruction[n] == "al" or instruction[n] == "ax" or instruction[n] == "eax" ) :
        Rm_mod[2] = 0 #reg = 000
    elif (instruction[n] == "cl" or instruction[n] == "cx" or instruction[n] == "ecx") :
        Rm_mod[4] = 1
    elif (instruction[n] == "dl" or instruction[n] == "dx" or instruction[n] == "edx") :
        Rm_mod[3] = 1
    elif (instruction[n] == "bl" or instruction[n] == "bx" or instruction[n] == "ebx") :
        Rm_mod[3] =1
        Rm_mod[4] = 1
    elif (instruction[n] == "ah" or instruction[n] == "sp" or instruction[n] == "esp" ) :
        Rm_mod[2] = 1
    elif (instruction[n] == "ch" or instruction[n] == "bp" or instruction[n] == "ebp") :
        Rm_mod[2] = 1
        Rm_mod[4] =1
    elif (instruction[n] == "dh" or instruction[n] == "si" or instruction[n] == "esi"):
        Rm_mod[2]= 1
        Rm_mod[3] =1
    elif (instruction[n] == "bh" or instruction[n] == "edi" or instruction[n] == "di"):
        Rm_mod[2] = 1
        Rm_mod[3] = 1
        Rm_mod[4] = 1
    else:
        print("something is wrng!")
        exit()




def rm_mod():
    global stackk 
    if instruction[1][0] == "[" :
        Rm_mod[0] = 0 # if first on is memory mod 00 
        Rm_mod[1] =0
        findregrm_mod1(1)
        reg(2)
    elif instruction[2][0] == "[":
        Rm_mod[0] =0 # if second one is memory mod is 00
        Rm_mod[1] = 0
        findregrm_mod1(2)
        reg(1)
    else: # if both are reg then mod 11
        Rm_mod[0]  = 1  #mod 11
        Rm_mod[1] = 1  #mod 11 
        reg(2)

    if Rm_mod[0] ==1 and Rm_mod[1] ==1: # find r/m for both reg
        global phase2Array
        if (instruction[1] == "al" or instruction[1] == "ax" or instruction[1] == "eax" ) :
            Rm_mod[7] =0
        elif (instruction[1] == "cl" or instruction[1] == "cx" or instruction[1] == "ecx" ) :
            Rm_mod[7] =1
        elif (instruction[1] == "dl" or instruction[1] == "dx" or instruction[1] == "edx") :
            Rm_mod[6] =1
        elif (instruction[1] == "bl" or instruction[1] == "bx" or instruction[1] == "ebx") :
            Rm_mod[6] =1
            Rm_mod[7] =1
        elif (instruction[1] == "ah" or instruction[1] == "sp" or instruction[1] == "esp" ) :
            Rm_mod[5] =1
        elif (instruction[1] == "ch" or instruction[1] == "bp" or instruction[1] == "ebp") :
            Rm_mod[5] =1
            Rm_mod[7] =1
        elif (instruction[1] == "dh" or instruction[1] == "si" or instruction[1] == "esi"):
            Rm_mod[5] =1
            Rm_mod[6] =1
        elif (instruction[1] == "bh" or instruction[1] == "edi" or instruction[1] == "di"):
            Rm_mod[5] =1
            Rm_mod[6] =1
            Rm_mod[7] =1
        else:
            print("something is wrng!")
            exit()
   
    Rm_mod_hex = hex(int(''.join(map(str, Rm_mod)), 2)) # make it to hex
    phase2Array += [str(Rm_mod_hex)]
    print(Rm_mod_hex , end = " ")
    stackk = str(hex(int(stackk, 16)+ int("1" ,16))) # add stack one every time prints smth


def findaddition(): # depends on reg the addition will be set and if it's 16 bit 0x66 will be too
    global phase2Array
    global stackk 
    if instruction[1] == "ax" :
        print("0x66" , end=" ")
        phase2Array += ["0x66"]
        stackk = str(hex(int(stackk, 16)+ int("1" ,16)))
        return '0'
    elif instruction[1] == "cx":
        print("0x66" , end=" ")
        phase2Array += ["0x66"]
        stackk = str(hex(int(stackk, 16)+ int("1" ,16)))
        return '1'
    elif instruction[1] == "dx":
        print("0x66" , end=" ")
        phase2Array += ["0x66"]
        stackk = str(hex(int(stackk, 16)+ int("1" ,16)))
        return '2'
    elif instruction[1] == "bx":
        print("0x66" , end=" ")
        phase2Array += ["0x66"]
        stackk = str(hex(int(stackk, 16)+ int("1" ,16)))
        return '3'
    elif instruction[1] == "sp":
        print("0x66" , end=" ")
        phase2Array += ["0x66"]
        stackk = str(hex(int(stackk, 16)+ int("1" ,16)))
        return '4'
    elif instruction[1] == "bp":
        print("0x66" , end=" ")
        phase2Array += ["0x66"]
        stackk = str(hex(int(stackk, 16)+ int("1" ,16)))
        return '5'
    elif instruction[1] == "si":
        print("0x66" , end=" ")
        phase2Array += ["0x66"]
        stackk = str(hex(int(stackk, 16)+ int("1" ,16)))
        return '6'
    elif instruction[1] == "di":
        print("0x66" , end=" ")
        phase2Array += ["0x66"]
        stackk = str(hex(int(stackk, 16)+ int("1" ,16)))
        return '7'
    elif instruction[1] == "eax":
        return '0'
    elif instruction[1] == "ecx":
        return '1'
    elif instruction[1] == "edx":
        return '2'
    elif instruction[1] == "ebx":
        return '3'
    elif instruction[1] == "esp":
        return '4'
    elif instruction[1] == "ebp":
        return '5'
    elif instruction[1] == "esi":
        return '6'
    elif instruction[1] == "edi":
        return '7'
    else:
        print("something is wrng!")
        exit()

def findds():
    global phase2Array
    flag = 0 
    global stackk 
    if instruction[1][0] == "[" and instruction[2][0] != "[": # checks if first one is memory
        op_code[6] =0
        flag = 1
    elif instruction[1][0] != "[" and instruction[2][0] == "[":# checks if second one is memory
        op_code[6] =1
        flag = 2
    elif instruction[1][0] == "[" and instruction[2][0] == "[": # if both are memory it's an error
        print("something is wrong")
        exit()
    else :
        op_code[6] =0 # if both are reg then d is 0

    temp = instruction[1].replace("[" , "") # if there is a memory remove the "[]"
    temp = temp.replace("]" , "")
    # set s in op code with reg 1 if it's 8 -> 0 16 or 32 -> 1
    if temp == "al" or temp == "bl" or temp == "cl" or temp =="dl" or temp == "ah" or temp == "bh" or temp== "ch" or temp == "dh":
        op_code[7] = 0
    elif temp == "eax" or temp == "ebx" or temp == "ecx" or temp =="edx" or temp == "esi" or temp == "edi" or temp == "ebp" or temp == "esp" or temp == "ax" or temp == "bx" or temp == "cx" or temp == "dx" or temp == "si" or temp == "di" or temp == "bp" or temp == "sp" :
        op_code[7] = 1
        if flag ==1 :
            if instruction[2][-1] == "l":
                op_code[7] = 0
        if  temp == "ax" or temp == "bx" or temp == "cx" or temp == "dx" or temp == "si" or temp == "di" or temp == "bp" or temp == "sp":
            print("0x66" , end=" ") # if reg is 16 print this
            phase2Array += ["0x66"]
            stackk = str(hex(int(stackk, 16)+ int("1" ,16)))
    else:
        print("something is wrng!") # if the reg name is wrong
        exit()
            
   

def main(khat):
    global stackk 
    global phase2Array
    if instruction[0] == "add":
        op_code [0]=0 #first 6 bits of add are 0 and d & s depends
        findds() # set ds
        op_code_hex = hex(int(''.join(map(str, op_code)), 2)) # change it to hex  
        phase2Array += [str(op_code_hex)] 
        print(op_code_hex , end = " ") 
        stackk = str(hex(int(stackk, 16)+ int("1" ,16))) # add the stack 1 
        rm_mod() # find rm and mod 
    elif instruction[0] == "sub":
        op_code[2]=1
        op_code[4]=1
        findds()
        op_code_hex = hex(int(''.join(map(str, op_code)), 2))
        phase2Array += [str(op_code_hex)] 
        print(op_code_hex , end = " ")
        stackk = str(hex(int(stackk, 16)+ int("1" ,16)))
        rm_mod()
    elif instruction[0] == "xor":
        op_code[2]=1
        op_code[3] = 1
        findds()
        op_code_hex = hex(int(''.join(map(str, op_code)), 2))
        print(op_code_hex , end = " ")
        phase2Array += [str(op_code_hex)] 
        stackk = str(hex(int(stackk, 16)+ int("1" ,16)))
        rm_mod()
    elif instruction[0] == "or":
        op_code[4]=1
        findds()
        op_code_hex = hex(int(''.join(map(str, op_code)), 2))
        print(op_code_hex , end = " ")
        phase2Array += [str(op_code_hex)] 
        stackk = str(hex(int(stackk, 16)+ int("1" ,16)))
        rm_mod()
    elif instruction[0] =="and":
        op_code[2] =1
        findds()
        op_code_hex = hex(int(''.join(map(str, op_code)), 2))
        print(op_code_hex , end = " ")
        phase2Array += [str(op_code_hex)] 
        stackk = str(hex(int(stackk, 16)+ int("1" ,16)))
        rm_mod()
    elif instruction[0] == "push": # find the proper addotion from reg and add it to constant
        if "0"<= instruction[1][0] <= "9":
            flagg = 0 
            if instruction[1][-1] == "h":
                adad= "0x" + instruction[1].replace("h" , "")
                flagg =1
            if instruction[1][0] == "-":
                sflag = 1
                instruction[1] = instruction[1].replace("-" , "")
            if instruction[1][-1] == "b":
                instruction[1]= instruction[1].replace("b" , "")
                instruction[1]= str(int(instruction[1] , 2))
            if instruction[1][-1] == "o":
                instruction[1] = instruction[1].replace("o", "")
                instruction[1]= str(int(instruction[1] , 8))
            instruction[1]= instruction[1].replace("h" , "")
            adadindec = int(instruction[1] , 10)
            if -2147483648<=adadindec <=2147483647:
                if -128 <= adadindec<= 128:
                    print("0x6a" , end = " ")
                    phase2Array += ["0x6a"] 
                    stackk = str(hex(int(stackk, 16)+ int("1" ,16)))
                else:
                    print("0x68" , end = " ")
                    phase2Array += ["0x68"] 
                    stackk = str(hex(int(stackk, 16)+ int("1" ,16)))
                    #if -32768 <= adadindec <= 32767:
                        #stackk = str(hex(int(stackk, 16)+ int("3" ,16)))
                    #else : 
                        #stackk = str(hex(int(stackk, 16)+ int("5" ,16)))
            else :
                print("smth is wrong!")
                exit()
            if flagg ==1 : 
                print(adad , end = " ")
                phase2Array += [str(adad)] # for 32 bits please part it up 
                stackk = str(hex(int(stackk, 16)+ int("1" ,16)))
            else : 
                print(hex(int(instruction[1])) , end = " ")
                phase2Array += [str(hex(int(instruction[1])))]
                stackk = str(hex(int(stackk, 16)+ int("1" ,16)))
        else : 
            addition = findaddition() # find the addition
            op_code_hex = hex(int('50' , 16) + int(addition,16)) #add in hex
            print(op_code_hex , end = " ")
            phase2Array += [str(op_code_hex)]
            stackk = str(hex(int(stackk, 16)+ int("1" ,16))) # add stack one
    elif instruction[0] == "pop":
        addition = findaddition()
        op_code_hex = hex(int("58" , 16) + int(addition,16))
        print(op_code_hex , end = " ")
        phase2Array += [str(op_code_hex)]
        stackk = str(hex(int(stackk, 16)+ int("1" ,16)))
    elif instruction[0] == "inc":
        if instruction[1] == "al" or instruction[1] == "bl" or instruction[1] == "cl" or instruction[1] == "dl" or instruction[1] == "ah" or instruction[1] == "bh" or instruction[1] == "ch" or instruction[1] == "dh" :
            if instruction[1] == "al":
                print("0xfe" , end=" ")
                phase2Array += ["0xfe"]
                phase2Array += ["0xc0"]
                print("0xc0" , end = " ")
                return
            elif instruction[1] == "bl":
                print("0xfe" , end=" ")  # inc for 8 regs
                print("0xc3" , end = " ")
                phase2Array += ["0xfe"]
                phase2Array += ["0xc3"]
                return
            elif instruction[1] == "cl":
                print("0xfe" , end=" ")
                print("0xc1" , end = " ")
                phase2Array += ["0xfe"]
                phase2Array += ["0xc1"]
                return
            elif instruction[1] == "dl":
                print("0xfe" , end=" ")
                print("0xc2" , end = " ")
                phase2Array += ["0xfe"]
                phase2Array += ["0xc2"]
                return
            elif instruction[1] == "ah":
                print("0xfe" , end=" ")
                print("0xc4" , end = " ")
                phase2Array += ["0xfe"]
                phase2Array += ["0xc4"]
                return
            elif instruction[1] == "bh":
                print("0xfe" , end=" ")
                print("0xc7" , end = " ")
                phase2Array += ["0xfe"]
                phase2Array += ["0xc7"]
                return
            elif instruction[1] == "dh":
                print("0xfe" , end=" ")
                print("0xc6" , end = " ")
                phase2Array += ["0xfe"]
                phase2Array += ["0xc6"]
                return
            elif instruction[1] == "ch":
                print("0xfe" , end=" ")
                print("0xc5" , end = " ")
                phase2Array += ["0xfe"]
                phase2Array += ["0xc5"]
                return
        addition = findaddition()
        op_code_hex = hex(int("40" , 16) + int(addition,16))
        print(op_code_hex , end = " ")
        phase2Array += [str(op_code_hex)]
        stackk = str(hex(int(stackk, 16)+ int("1" ,16)))
    elif instruction[0] == "dec":
        if instruction[1] == "al" or instruction[1] == "bl" or instruction[1] == "cl" or instruction[1] == "dl" or instruction[1] == "ah" or instruction[1] == "bh" or instruction[1] == "ch" or instruction[1] == "dh" :
            if instruction[1] == "al":
                print("0xfe" , end=" ")
                print("0xc8" , end = " ")
                phase2Array += ["0xfe"]
                phase2Array += ["0xc8"]
                return
            elif instruction[1] == "bl":
                print("0xfe" , end=" ") # inc for 8 regs
                print("0xcb" , end = " ")
                phase2Array += ["0xfe"]
                phase2Array += ["0xcb"]
                return
            elif instruction[1] == "cl":
                print("0xfe" , end=" ")
                print("0xc9" , end = " ")
                phase2Array += ["0xfe"]
                phase2Array += ["0xc9"]
                return
            elif instruction[1] == "dl":
                print("0xfe" , end=" ")
                print("0xca" , end = " ")
                phase2Array += ["0xfe"]
                phase2Array += ["0xca"]
                return
            elif instruction[1] == "ah":
                print("0xfe" , end=" ")
                print("0xcc" , end = " ")
                phase2Array += ["0xfe"]
                phase2Array += ["0xcc"]
                return
            elif instruction[1] == "bh":
                print("0xfe" , end=" ")
                print("0xcf" , end = " ")
                phase2Array += ["0xfe"]
                phase2Array += ["0xcf"]
                return
            elif instruction[1] == "dh":
                print("0xfe" , end=" ")
                print("0xce" , end = " ")
                phase2Array += ["0xfe"]
                phase2Array += ["0xce"]
                return
            elif instruction[1] == "ch":
                print("0xfe" , end=" ")
                print("0xcd" , end = " ")
                phase2Array += ["0xfe"]
                phase2Array += ["0xcd"]
                return
        addition = findaddition()
        op_code_hex = hex(int("48" , 16) + int(addition,16))
        print(op_code_hex , end = " ")
        phase2Array += [str(op_code_hex)]
        stackk = str(hex(int(stackk, 16)+ int("1" ,16)))
    elif instruction[0][-1] == ":" :
        j=0
    elif instruction[0] == "jmp": # for jmp find the label and it's line compare it with jmp line and find if it's backward or forward then find the fasele 
        print("0xeb" , end = " ") # print this at the beginning

        j=0
        stackk = str(hex(int(stackk, 16)+ int("1" ,16))) # add one after print
        for k in range ( 0 , len ( labels)):
            if labels[k] == instruction[1]: # find the label of the jmp
                if labels_line[k] < khat: #backward
                    fasele = 2 
                    adad_label = labels_line[k] + 1
                    for j in range (adad_label  , khat):
                        if j in labels_line:
                            fasele+= 0
                        elif instruction2[j][0] == "jmp":
                            fasele+= 2
                        elif len(instruction2[j][1]) ==2: # find the fasale beetwen jmp and label
                            fasele += 3
                        elif len(instruction2[j]) == 2:
                            fasele+=1
                        elif len(instruction2[j][1])>= 3 or len(instruction2[j][1]) == 1:
                            fasele += 2
                        else:
                            print("something is wrng!")
                            exit()
                    fasele_hex = hex(int(str(fasele) , 16))
                    fasele_hex = (1 << 8) - fasele
                    fasele_hex = hex(fasele_hex & (2**8 - 1)) # find the 2's compliment
                    print(fasele_hex , end = " ")
                    stackk = str(hex(int(stackk, 16)+ int("1" ,16))) #add one to stack
                    break
                else : #forward
                    fasele = 0
                    adad_label = labels_line[k] 
                    for j in range(khat+1 ,adad_label): # find fasele
                        if j in labels_line:
                            fasele+= 0
                        elif instruction2[j][0] == "jmp":
                            fasele+=2
                        elif len(instruction2[j][1]) ==2:
                            fasele += 3
                        elif len(instruction2[j]) == 2:
                            fasele+=1
                        elif len(instruction2[j][1])>= 3 or len(instruction2[j][1]) == 1:
                            fasele += 2
                        else:
                            print("something is wrng!")
                            exit()
                    print(hex(int(str(fasele) , 16)) , end =" ") # convert to hex and print
                    stackk = str(hex(int(stackk, 16)+ int("1" ,16)))
                    break

    else:
        print("some thing is wrong")
        exit()


for i in range ( 0,length_instruction): # the loop to read every instruction and print stack and assemble code and the instruction it self
    phase2Array += [","]
    op_code= [0] * 8
    Rm_mod= [0] * 8
    instruction = instruction2[i] 
    stack_figure =  stackk.split("x")
    len_stack = len(stackk[1])
    print("0x" + (16 - len_stack)* "0" + stack_figure[1] , end=": ")
    main(i) 
    if instruction[0][-1] ==":":
        print("( " + instruction[0] + " )" )
    else : 
        print("(" + instruction[0] + " " +instruction[1] + " " , end = "")
        if len( instruction) == 2:
            print(")")
        else:
            print(", " + instruction[2] + ")")    

#print(phase2Array)

            
