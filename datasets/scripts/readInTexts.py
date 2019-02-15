
print("Enter the file name!")
inputFileName = input()

with open(inputFileName, "r") as readF:
    content = readF.read().split();

print("How many do you want printed out?");
numberToPrint = int(input())

numberToPrint = numberToPrint if numberToPrint<len(content) else len(content)

print(content[:numberToPrint])