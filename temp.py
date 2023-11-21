life = 3
hearts = []
for i in range(3):
    if life > i:
        hearts.insert(0, "a")
    else:
        hearts.insert(0, "b")
print(hearts)