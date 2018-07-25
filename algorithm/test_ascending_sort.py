import random

import sort


def test_ascending():
    nums = [2, 1, 5, 3, 6, 2, 5]
    sort.bubble_sort(nums)
    ans = [1, 2, 2, 3, 5, 5, 6]
    assert nums == ans


def test_ascending_sort():
    nums = random.sample(range(10), 5)
    sorted_ans = sorted(nums)
    sort.bubble_sort(nums)
    assert nums == sorted_ans
