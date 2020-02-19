'''https://programmers.co.kr/learn/courses/30/lessons/42862#
시간복잡도: O(n)
공간복잡도: O(1)
'''

# 첫번째 한 시도. -> test는 통과했으나 제출하니 66.7/100 점 받음
def solution(n, lost, reserve):
    answer = 0
    list_ = []
    total_student = [k+1 for k in range(n)]
    for i in total_student:
        if i in lost:
            if (i-1) in reserve:
                reserve.remove((i-1))
                list_.append(i)
            elif (i+1) in reserve:
                reserve.remove((i+1))
                list_.append(i)
    print(reserve)
    print(f"체육복 받은 사람: {list_}")
    answer = len(list_) + (n - len(lost))
    return answer


# 두번째 시도
def solution(n, lost, reserve):
    setLost = set(lost) - set(reserve)
    setReserve= set(reserve) - set(lost)
    for i in setReserve:
        if i-1 in setLost:
            setLost.remove(i-1)
        elif i+1 in setLost:
            setLost.remove(i+1)
    return n-len(setLost)
