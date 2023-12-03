finalsum = 0
with open("input.txt", 'r') as fh:
    while lin := fh.readline():
        fil = [int(x) for x in lin if x.isdigit()]
        finalsum += 10*fil[0] + fil[-1]
print(finalsum)
