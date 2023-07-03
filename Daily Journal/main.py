date = input("Enter the date of the journal(DD-MM-YYYY): ")
mood = input("Enter your mood today on a scale of 1 to 10?: ")+"\n"

journal = input("Enter you thoughts: ")

para = [f"Moode={mood}",journal]

with open(f"Journals/{date}.txt","w") as f:
    f.writelines(para)
