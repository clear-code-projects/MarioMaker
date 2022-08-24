import timeit

print(timeit.timeit("[(a, b) for a in (1, 3, 5) for b in (2, 4, 6)]", number = 1000))