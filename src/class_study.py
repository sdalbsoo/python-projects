class ABC():
    def __init__(self, val):
        self.v = val
        print("init called")

    def g(self):
        print(self)

    def h(self):
        self.v += 2

    @staticmethod
    def f():
        pass


a = ABC(3)  # <=> ABC(a, 3)
a.g(5)  # <=> ABC.g(a, 5)
# 에러를 이해하세요
