term1 = 3
term2 = 4
term = 4
sum_term = 0
while term < 7_000_000:
    if term % 2 == 0:
        sum_term += term
    term = term1 + term2
    term1 = term2
    term2 = term
print(sum_term)
