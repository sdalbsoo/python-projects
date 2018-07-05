# (Stupid) Recursion
def fibo_recur(n):
    if n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fibo_recur(n-1) + fibo_recur(n-2)

## Tail Recursion
# A tail recursive function to 
# calculate n th fibnacci number
def fibo_tail(n, a=0, b=1):
    if n == 0:
        return a
    if n == 1:
        return b
    return fibo_tail(n - 1, b, a + b);

## Iterative
def fibo_iter(n):
    prev, next_ = 0, 1
    for i in range(n):
        prev, next_= next_, prev+next_
    return prev

## Memoization & Dynamic Programming
def fibo_memo(n):
    list_nums = [0, 1]
    for i in range(n-1):
        next_val = list_nums[i] + list_nums[i+1]
        list_nums.append(next_val)
    return list_nums[n]
