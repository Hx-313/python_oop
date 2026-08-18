#----------------------------------------
# Lesson 1: Printing and Working with Strings
# This script shows the basics of printing output,
# creating string variables, and using string methods.
#----------------------------------------

# print() is Python's built-in function to show text on the screen
print("Hello World!") # a simple string in double quotes
print("This is a simple Python script.")

# The "*" operator multiplies (repeats) a string.
# " *" repeated 10 times gives a decorative line
print(" *" * 10 ) # repeats the string " *" ten times

# A variable stores a value so we can use it again later
course = "Time pass for a lifetime"
print(course) # prints the value stored in the variable

# len() returns the number of characters in a string
print (len(course)) # course has 23 characters

# Slicing: [start:end] extracts a part of the string.
# It starts at index 10 and goes up to (but NOT including) index 24
print(course[10:24]) # prints characters from position 10 to 23

# "not in" checks if a word is NOT present in the string.
# Returns True if "pass" is not found, otherwise False
print("pass" not in course) # "pass" is not in the course string, so True

# A plain comment (nothing to do with code)
# how are you

# def creates a new function (a reusable block of code)
def greet():
    print("Hello! How are you?") # code inside the function body
    print("Welcome to the Python course.")

greet() # calling the function runs all the code inside it
