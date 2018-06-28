def fibo(num):
	list = [0, 1]
	index = 1
	while list[index] <= num:
		list.append(list[index] + list[index-1])
		index += 1
	return list[:-1]

num = 200
print(fibo(num))
