def fibo_recur(n):
    if n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fibo_recur(n-1) + fibo_recur(n-2)


print(fibo_recur(5))
