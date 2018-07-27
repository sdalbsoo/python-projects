import copy


def bubble_sort(nums):
    nums_copy = copy.deepcopy(nums)
    for i in range(len(nums_copy)-1):
        for j in range(1, len(nums_copy)-i):
            if nums_copy[j-1] > nums_copy[j]:
                temp = nums_copy[j-1]
                nums_copy[j-1] = nums_copy[j]
                nums_copy[j] = temp
    return nums_copy


def main():
    nums = [9, 7, 1, 3, 6, 10, 1, 4]
    print(nums)
    print(bubble_sort(nums))


if __name__ == "__main__":
    main()
