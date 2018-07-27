import random

from sort import bubble_sort


def test_sort_deterministic():
    nums = [2, 1, 5, 3, 6, 2, 5]
    ans = [1, 2, 2, 3, 5, 5, 6]
    assert bubble_sort(nums) == ans


def test_sort_stochastic():
    for i in range(20):
        nums = random.sample(range(10), 5)
        sorted_ans = sorted(nums)
        assert bubble_sort(nums) == sorted_ans
