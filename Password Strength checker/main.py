password = input("Enter your psasword: ")

isStrong = []
flag = 0
isStrong.append(len(password) >= 8)

for char in password:
    if char.isdigit():
        isStrong.append(True)
        flag = 1
        break

if flag==0:
    isStrong.append(False)

flag=0
for char in password:
    if char.isupper():
        isStrong.append(True)
        flag = 1
        break

if flag==0:
    isStrong.append(False)
    
if False in isStrong:
    print("Weak Password")
else:
    print("Strong Password")
