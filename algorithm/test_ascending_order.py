import random


def test_ascending():
    num = [2, 1, 5, 3, 6, 2, 5]
    for i in range(len(num)):
        for j in range(len(num)-1):
            if num[j] > num[j+1]:
                temp = num[j]
                num[j] = num[j+1]
                num[j+1] = temp
    ans = [1, 2, 2, 3, 5, 5, 6]
    assert num == ans


def test_ascending_order():
    ans = random.sample(range(10), 5)
    stash = tuple(ans)
    ans.sort()
    num = list(stash)
    for i in range(len(num)):
        for j in range(len(num)-1):
            if num[j] > num[j+1]:
                temp = num[j]
                num[j] = num[j+1]
                num[j+1] = temp
    assert num == ans
