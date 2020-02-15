'''programmers.co.kr/learn/challenges
문제: 완주하지 못한 선수
해쉬 관련 문제
'''

# first
def solution1(participant, completion):
    answer = ''
    for i in participant:
        if i not in completion:
            answer = i
    return answer


# second
def solution2(participant, completion):
    answer = ''
    participant.sort()
    completion.sort()
    for i, j in zip(participant, completion):
        if i != j:
            return i
    return participant[-1]
