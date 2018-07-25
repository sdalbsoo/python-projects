def bubble_sort(nums):
    for i in range(len(nums)-1):
        for j in range(1, len(nums)-i):
            if nums[j-1] > nums[j]:
                temp = nums[j-1]
                nums[j-1] = nums[j]
                nums[j] = temp
    return nums


nums = [9, 7, 1, 3, 6, 10, 1, 4]
print(bubble_sort(nums))
