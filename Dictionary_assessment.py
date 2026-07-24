# write name and percentage marks in a dictionary and display information.
name=input("student's name: ")
percent= float(input("Enter the marks: "))

student={}

student["Name"]=name
student["Percentage"]= percent

print(student)




#Find the number of occurrences of each letter in a string

st=input("enter the string: ")

count={}
for ch in st:
    if ch.isalpha():
        count[ch]=count.get(ch,0)+1
print(count) 



#Find number of occurence of each vowel in a string.

st=input("Enter the string: ")
s=st.lower()
vowels={"a":0, "e":0,"i":0,"o":0,"u":0}
for ch in s:
    if ch in vowels:
        vowels[ch]+=1
print(vowels)



#Store name and marks of  students in a dictionary and display marks of given student

n=int(input("Enter number of students: "))
students={}
for i in range(n):
    name=input("Name: ")
    marks=float(input("Marks: "))
    students[name]=marks

while True:
    select=input("Enter name of student to dispay marks or type 'exit' to quit: ")

    if select.lower()=="exit":
        print("END")
        break
    print("marks",students.get(select,"student not in the list"))




 #program to print the data structures and some properties in teabular format.

headers = ["Property", "List", "Tuple", "Set", "Frozenset", "Dictionary"]

data = [
    ["Syntax", "[]", "()", "{ }/set[()] ", "frozenset()", "{K : V}"],
    ["Ordered", "Yes", "Yes", "No", "No", "Yes"],
    ["Mutable", "Yes", "No", "Yes", "No", "Yes"],
    ["Allow Duplicates", "Yes", "Yes", "No", "No", "Keys: No, Values: Yes"],
    ["Indexed", "Yes", "Yes", "No", "No", "By Key"],
    ["Heterogeneous", "Yes", "Yes", "Yes", "Yes", "Yes"],
    ["Hashable", "No", "Yes", "No", "Yes", "No"],
    ["Can be Nested", "Yes", "Yes", "Yes", "Yes", "Yes"],
    ["Supports Slicing", "Yes", "Yes", "No", "No", "No"],
    ["Lookup Speed", "O(n)", "O(n)", "O(1)", "O(1)", "O(1)"],
    ["Stores", "Values", "Values", "Unique Values", "Unique Values", "Key-Value Pairs"],
    ["Typical Use", "General Purpose", "Fixed Data", "Unique Items", "Immutable Set", "Fast Lookup"]
]

# Print the table
print("{:<18} {:<18} {:<18} {:<18} {:<18} {:<18}".format(*headers))
print("-" * 90)

for row in data:
    print("{:<18} {:<18} {:<18} {:<18} {:<18} {:<18}".format(*row)) 
