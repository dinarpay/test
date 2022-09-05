#coded for python 3.5
import random
import string

def gen_hex(length): #this helps generate valid HEX addresses.
    return ''.join(random.choice('0123456789abcdef') for _ in range(length))

def gen_00mac(): #this generates a 00-XX-XX-XX-XX-XX mac address
    generated = '00' + '04' + 'f2' + gen_hex(2) + gen_hex(2) + gen_hex(2) + '.cfg'
    return generated

def gen_list(what): #this generates our hex list.
    list1 = ""
    for i in range(what):
        if (what < i):
            list1+=gen_00mac()
        else:
            list1+=gen_00mac() + "\n"
    return list1

def gen_save(filename, output): #save our list
    file = open(filename, "w")
    print("Saving to: " + filename)
    file.write(output)
    print("Finished saving!")
    return

def gen_yn(): #simple check func
    option = input("Do you wish to save (y/n): ") #our Y/N option
    print ("Generating results...")
    tempgen = gen_list(numgen) #save our generated list to a variable
    print ("Results generated.")
    if (option == "y"):
        print ("Please wait for results...\n")
        print (tempgen) #print out the results
        gen_save("PyMAC.txt", tempgen) #filename, data
    else:
        print ("Please wait for results...\n")
        print (tempgen) #print out the results
    return

print ("PyMAC Generator v0.1 by LeftBased")
numgen = int(input("Generate # of MACs: "))
gen_yn()
