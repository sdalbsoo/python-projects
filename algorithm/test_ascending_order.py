import random


def test_ascending():
    nums = [2, 1, 5, 3, 6, 2, 5]
    for i in range(len(nums)):
        for j in range(len(nums)-1):
            if nums[j] > nums[j+1]:
                temp = nums[j]
                nums[j] = nums[j+1]
                nums[j+1] = temp
    ans = [1, 2, 2, 3, 5, 5, 6]
    assert nums == ans


def test_ascending_order():
    ans = random.sample(range(10), 5)
    stash = tuple(ans)
    ans.sort()
    nums = list(stash)
    for i in range(len(nums)):
        for j in range(len(nums)-1):
            if nums[j] > nums[j+1]:
                temp = nums[j]
                nums[j] = nums[j+1]
                nums[j+1] = temp
    assert nums == ans
