
from re import L


mainarray= ["XX"] * 256
# initialize the stack array 



def dataSegment ( arraynum , dataArray ):# function for data segment
    global mainarray
    for i in range(len(dataArray)): # loop into all data code  and find key words "word" , "byte" , "dword"
        if (dataArray[i].lower() == "byte"):
            mainarray[arraynum] = dataArray[i-1] 
            arraynum += 1
        elif (dataArray[i].lower() == "word"):
            for j in range(2):
                mainarray[arraynum] = dataArray[i-1] # add name of variable into stack until it get wtight amount of space
                arraynum += 1
        elif (dataArray[i].lower() == "dword"):
            for j in range(4):
                mainarray[arraynum] = dataArray[i-1]
                arraynum += 1

    return    

def stackSegment (arraynum , codeArray ):# function for stack segment 
    global mainarray
    codeArray = [element for row in codeArray for element in row] # make matrix into flatted array for instructions
    for i in range(len(codeArray)): # loop into instructions to find push or pop ones
        if codeArray[i].lower() == "push": 
            if (codeArray[i+ 1] == "eax" or codeArray[i+ 1] == "ebx" or codeArray[i+ 1] == "ecx" or codeArray[i+ 1] == "edx" or codeArray[i+ 1] == "esi" or  
            codeArray[i+ 1] == "esp"  or codeArray[i+ 1] == "edp" or codeArray[i+ 1] == "edi" ): # if it was register push the name of reg for 4 times
                for j in range(4):
                    mainarray[arraynum] = codeArray[i+1]
                    arraynum += 1
            elif (codeArray[i+ 1] == "ax"  or codeArray[i+ 1] == "dx"  or codeArray[i+ 1] == "cx"  or codeArray[i+ 1] == "bx" or codeArray[i+1] == "si" or 
            codeArray[i+1] == "sp" or codeArray[i+1] == "dp" or codeArray[i+1] == "di"):# 2 times for 16 bit regs
                for j in range(2):
                    mainarray[arraynum] = codeArray[i + 1]
                    arraynum += 1
                for j in range(2):
                    mainarray[arraynum] = "MM" # make it word align
                    arraynum += 1
            elif (codeArray[i+1] == "al" or codeArray[i+1] == "ah" or codeArray[i+1] == "bl" or codeArray[i+1] == "bh" or codeArray[i+1] == "cl" or
            codeArray[i+1] == "ch" or codeArray[i+1] == "dl" or codeArray[i+1] == "dh"):# one time for bytes
                mainarray[arraynum] = codeArray[i+1] # we find reg name from element after push or pop
                arraynum += 1
                for j in range(3):
                    mainarray[arraynum] = "MM"
                    arraynum += 1
            else :# if it's not reg it's immidiet
                if codeArray[i+1][-1] == "b":
                    pushNum = int(codeArray[i+1][:-1] , 2)
                elif codeArray[i+1][-1] == "h":
                    pushNum = int(codeArray[i+1][:-1] , 16)
                elif codeArray[i+1][-1] == "d":
                    pushNum = int(codeArray[i+1][:-1])
                elif codeArray[i+1][-1] == "o":
                    pushNum = int(codeArray[i+1][:-1] , 8)
                else :
                    pushNum = int(codeArray[i+1])
                if ( pushNum<= 127 and pushNum>= -128): # if it's 8 bit imm:
                    mainarray[arraynum] = str(hex(pushNum)) # add hex of imm into stack
                    arraynum+= 1
                    for j in range(3):
                        mainarray[arraynum] = "MM"
                        arraynum += 1
                elif (pushNum <= 32767 and pushNum>= -32768): # if it's 16 bit add it in little indian order
                    pushNum = str(hex(pushNum))
                    pushNum = pushNum[2:]
                    if len(pushNum)<4:
                        j = 4 - len(pushNum)
                        pushNum=(j*"0")+pushNum
                    for j in range ( 2):
                        mainarray[arraynum]= pushNum[-2:] # add hex of imm into stack in 2 bytes
                        pushNum = pushNum[:-2] 
                        arraynum +=1
                    for j in range(2):
                        mainarray[arraynum] = "MM"
                        arraynum += 1
                elif (pushNum <= 2147483647 and pushNum >= -2147483648):
                    pushNum = str(hex(pushNum))
                    pushNum = pushNum[2:]
                    if len(pushNum)<8:
                        j = 8 - len(pushNum)
                        pushNum=(j*"0")+pushNum
                    for j in range(4):
                        mainarray[arraynum] = pushNum[-2:]
                        pushNum = pushNum[:-2]
                        arraynum += 1
                else : 
                    exit
        elif codeArray[i].lower() == "pop": # if it's pop simply remove 4 bytes 
            for j in range( 4):
                mainarray[arraynum] == "XX"
                arraynum -= 1


def find_middle(a, b, c): # a function to find mid of three ints
    if a <= b <= c or c <= b <= a:
        return b
    elif b <= a <= c or c <= a <= b:
        return a
    else:
        return c



def printSegments (sArraynum , cArraynum , dArraynum): # a function for print the segments in order and their values
    firstpart = min(sArraynum , cArraynum , dArraynum) # find from the int in front of each segment is min to write that segment first
    secondpart = find_middle(sArraynum , cArraynum , dArraynum)
    thirdpart = max(sArraynum , cArraynum , dArraynum)
    if firstpart == sArraynum: # find which part has min array number that to print it first
        print("SS:")
    elif firstpart == cArraynum :
        print("CS:")
    elif firstpart == dArraynum:
        print("DS:" )
    if firstpart!= 0:
        print("   ------------") # print a ?? segment first
        print("??:/    ..    /")
        print("   ------------")
    while(mainarray[firstpart] != "XX"): # print segments until is finished which means we get to XX
        print("   ------------")
        print("{}:|    {}    |".format(firstpart , mainarray[firstpart]))
        print("   ------------")
        firstpart += 1
    if firstpart != 255 and firstpart != secondpart:
        print("   ------------")
        print("??:/    ..    /")# print a ?? segment after that
        print("   ------------")
        firstpart += 1
    
    if secondpart == sArraynum: # find which one is second to print
        print("SS:")
    elif secondpart == cArraynum :
        print("CS:")
    elif secondpart == dArraynum:
        print("DS:" )
    if secondpart!= firstpart:
        print("   ------------")
        print("??:/    ..    /")
        print("   ------------")
    while( mainarray[secondpart] != "XX"): # print that segment values until is done
        print("   ------------")
        print("{}:|    {}    |".format(secondpart , mainarray[secondpart]))
        print("   ------------")
        secondpart += 1
    if secondpart != 255 and secondpart != thirdpart:
        print("   ------------")
        print("??:/    ..    /")
        print("   ------------")
        secondpart += 1

    if thirdpart == sArraynum:# do the operation for the third time too
        print("SS:")
    elif thirdpart == cArraynum :
        print("CS:")
    elif thirdpart == dArraynum:
        print("DS:" )

    if thirdpart!= secondpart:
        print("   ------------")
        print("??:/    ..    /")
        print("   ------------") 
    
    while( mainarray[thirdpart] != "XX"):
        print("   ------------")
        print("{}:|    {}    |".format(thirdpart , mainarray[thirdpart]))
        print("   ------------")
        thirdpart += 1

    if thirdpart != 255 :
        print("   ------------")
        print("??:/    ..    /")
        print("   ------------")
        thirdpart += 1

    
def codeSegment (arraynum , phase1aaray):# add the machine codes of code into code stack from the number it's told 
    insNum =0
    for j in range(len (phase1aaray)):
        if phase1aaray[j] == ",":
            insNum += 1
    i =0 
    for k in range(insNum):
        adad = 0
        if phase1aaray[i] == ",":
            i+= 1
        while  i != (len(phase1aaray))and phase1aaray[i] != ",":
            adad +=1
            i += 1
        i -= 1
        if arraynum %2 ==1:
            mainarray[arraynum] = "MM"
            arraynum += 1
        while phase1aaray[i] != ",":
            mainarray[arraynum] = phase1aaray[i] # in little indian way
            arraynum += 1
            i-= 1
        i = i +adad +1

def main ():
    stack = input()
    stack = stack[7:]
    stackarraynum = int(stack[:-1]) # find the number of stack that needs to save for
    input()
    data = input()
    if data[0] == ".":
        data =data[6:]
        dataarrayNum = int(data[:-1]) # find the number that date needs to save for
    dataCode = []
    while True:
        data = input()
        if data =="":
            break
        data = data.split()
        dataCode.append(data[0])
        dataCode.append(data[1]) # get the codes of data and add it into a splited array
    
    dataSegment(dataarrayNum , dataCode) # call data segment function to add data's into main stack

    code = input() 
    if code[0] == ".":
        code = code[6:]
        codearraynum = int(code[:-1])# find the number that machine codes needs to save for

    from assembler import phase2Array , instruction2 # call the assembler function to read codes and proccess it and give a array of machine codes 
                                                    # and a array of instructions for stack segments to find push and pops
    codeSegment(codearraynum , phase2Array) # call code segment to add machine codes into main stack
    stackSegment(stackarraynum , instruction2) # call stack segment to add regs or imm into main stack
    printSegments(stackarraynum , codearraynum , dataarrayNum) # call print function to print all


main()
  


    







    

