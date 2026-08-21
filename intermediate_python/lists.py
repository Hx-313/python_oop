myList = ["cars", "bikes", "trucks","planes"]


def printList(list):
    print("-------------------------------------------")
    print("\tstart printing")
    print("-------------------------------------------")
    if len(list) < 1:
       print("List is Empty")
    else:
        for item in list:
         print(f"\t{item}")
    print("-------------------------------------------")
    print("\tend printing")
    print("-------------------------------------------")
print(myList)

# accessingone item using index

print(myList[0])

# or 
printList(myList)
item = myList[-1]

print(item)
print()
# parsing the list 

printList(myList)

# checking specific item 

if "planes" in myList:
    print("yes")

else:
    print("no")

# useful methods

print(f"to find the length of the list {len(myList)}")

# adding new item in the list 

myList.append("ships")

print(f"new item added: {myList[-1]}")

printList(myList)

# insert item at random index 

myList.insert(2, "cruise")
print(f"new item added: {myList[2]} at index 2 that will be position 3 as index are 0-1-2")

printList(myList)

# remove elements 

# it returns the last item and remove it 
item = myList.pop()
print(item)


# remove specific item 
myList.remove("cruise")
printList(myList)

# to remove all item 
#myList.clear()
#printList(myList)

# to reverse the items 

myList.reverse()

printList(myList)

# sort

myList.sort()
printList(myList)


# add item 

myList1 = ["cars"] * 5

printList(myList1)

newList = myList + myList1

printList(newList)