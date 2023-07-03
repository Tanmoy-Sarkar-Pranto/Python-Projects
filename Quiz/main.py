import json

with open("quiz.json", "r") as f:
    data = json.load(f)

correct = 0

for i in range(len(data)):
    print(f'{data[i]["question_text"]}')
    for j in range(len(data[i]["alternatives"])):
        print(f'{j+1}:{data[i]["alternatives"][j]}')
    
    answer = int(input("Enter index of your answer: "))
    if answer == data[i]["correct_answer"]:
        correct = correct + 1

print(f"You got {correct} correct answer/s")
print(f"Your score is: {correct/len(data)}")