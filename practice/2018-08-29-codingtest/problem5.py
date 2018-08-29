import random


def insert_sort(list_nums):
    for k in range(1, len(list_nums)):
        j = list_nums[k]
        i = k
        while i > 0 and list_nums[i-1] > j:
            list_nums[i] = list_nums[i-1]
            i -= 1
        list_nums[i] = j

    for i in range(len(list_nums)-1):
        print(list_nums[i])


def main():
    list_nums = random.sample(range(30), 10)
    print(list_nums)
    insert_sort(list_nums)


if __name__ == "__main__":
    main()

# 거의 완성된 배열에서의 시간 복잡도는 O(n)이다.
