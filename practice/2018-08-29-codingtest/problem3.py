def fibo_memo(n):
    fibo_list = [0, 1]
    for i in range(n-1):
        next_value = fibo_list[i] + fibo_list[i+1]
        fibo_list.append(next_value)
    return fibo_list[n-1]


print(fibo_memo(5))

# 시간 복잡도 : O(n)
