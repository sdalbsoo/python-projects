from abc import abstractmethod


# SRP 적용이 필요한 예제
class Book1():
    def get_title(self):
        print("What is SRP")

    def get_author(self):
        print("Shin")

    def turn_page(self):
        pass

    def print_current_page(self):
        current_page = 1
        print("현재 페이지:{}".format(current_page))


# SRP 적용이 된 예제
class Book2():
    def get_title(self):
        print("What is SRP")

    def get_author(self):
        print("Shin")

    def turn_page(self):
        pass

    def get_current_page(self):
        current_page = 1
        print("현재 페이지:{}".format(current_page))


class Printer():
    @abstractmethod
    def print_current_page(self):
        pass


class Text_Printer(Printer):
    def print_current_page(self):
        print("현재 텍스트 페이지를 출력합니다.")


class Python_Printer(Printer):
    def print_current_python(self):
        print("현재 파이썬 페이지를 출력합니다.")
