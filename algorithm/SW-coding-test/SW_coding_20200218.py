'''https://programmers.co.kr/learn/courses/30/lessons/42748
시간복잡도: 최악 O(n^2) / 최선 O(nlogn)
공간복잡도: O(n)
'''
# 내 풀이
def solution(array, commands):
    answer = []
    for i in commands:
        if i[0] == i[1]:
            answer.append(array[i[0]-1])
        else:
            result = quickSort(array[i[0]-1:i[1]])
            answer.append(result[i[2]-1])
    return answer


def quickSort(x):
    if len(x) <= 1:
        return x
    pivot = x[len(x)//2]
    left,right,equal =[],[],[]
    for a in x:
        if a < pivot:
            left.append(a)
        elif a > pivot:
            right.append(a)
        else:
            equal.append(a)
    return quickSort(left) + equal + quickSort(right)


# 다른 사람의 풀이
def solution(array, commands):
    return list(map(lambda x:sorted(array[x[0]-1:x[1]])[x[2]-1], commands))

def solution(array, commands):
    answer = []
    for command in commands:
        i,j,k = command
        answer.append(list(sorted(array[i-1:j]))[k-1])
    return answer
