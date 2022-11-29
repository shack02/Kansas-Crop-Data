
string = "101010101010"
indexes = []
i = 0
for _ in string:
    if _ == "1":
        indexes.append(i)
    i += 1
print(indexes)



