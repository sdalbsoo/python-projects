'''https://programmers.co.kr/learn/courses/30/lessons/42840#
시간복잡도: O(n)
공간복잡도: O(n^2)
'''

# 내 풀이
def solution(answers):
    answer = []
    supoja = [[1, 2, 3, 4, 5], [2, 1, 2, 3, 2, 4, 2, 5], [3, 3, 1, 1, 2, 2, 4, 4, 5, 5]]
    length = len(answers)
    result = logic(answers, length, supoja)
    max_score = max(result)
    for i in range(3):
        if result[i] == max_score:
            answer.append(i + 1)
    return answer


def logic(answers, length, supoja):
    result = []
    count1 = 0
    count2 = 0
    count3 = 0
    for idx, value in enumerate(supoja):
        x = length // len(value)
        y = length % len(value)
        result.append(value*x + [value[x] for x in range(y)])
    for idx, x in enumerate(answers):
        if result[0][idx] == x:
            count1 += 1
        if result[1][idx] == x:
            count2 += 1
        if result[2][idx] == x:
            count3 += 1
    return [count1, count2, count3]

# 다른 사람의 풀이
'''
시간복잡도: O(n)
공간복잡도: O(n)
'''
def solution(answers):
    pattern1 = [1,2,3,4,5]
    pattern2 = [2,1,2,3,2,4,2,5]
    pattern3 = [3,3,1,1,2,2,4,4,5,5]
    score = [0, 0, 0]
    result = []

    for idx, answer in enumerate(answers):
        if answer == pattern1[idx%len(pattern1)]:
            score[0] += 1
        if answer == pattern2[idx%len(pattern2)]:
            score[1] += 1
        if answer == pattern3[idx%len(pattern3)]:
            score[2] += 1

    for idx, s in enumerate(score):
        if s == max(score):
            result.append(idx+1)

    return result
