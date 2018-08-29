import random


def bubble_sort(li):
    for i in range(len(li)-1):
        for j in range(len(li)-(i+1)):
            if li[j] > li[j+1]:
                li[j], li[j+1] = li[j+1], li[j]
    print(li)


def main():
    li = random.sample(range(30), 10)
    bubble_sort(li)


if __name__ == "__main__":
    main()

# 전체를 반복적으로 돌면서 큰 값을 뒤로 보낸다. 따라서 O(n^2) 시간복잡도를 가진다.
