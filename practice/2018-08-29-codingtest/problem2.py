def zigzag_arr(i, a):
    num = 1
    for k in range(i):
        for j in range(i):
            if k % 2 == 0:
                a[j][k] = num
                num += 1
            else:
                a[i - j - 1][k] = num
                num += 1
    for i in a:
        print(i)


def main():
    i = int(input("가로, 세로 길이를 입력해주세요: "))
    a = [[0]*i for k in range(i)]
    zigzag_arr(i, a)


if __name__ == "__main__":
    main()
