#OCP의 좋은 예제.

from abc import abstractmethod


class Shape(object):
    @abstractmethod
    def area(self):
        pass


class Rectangle(Shape):
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def area(self):
        area_rectangle = self.width * self.height
        return area_rectangle


class AreaCalculator(object):
    def __init__(self, shapes):
        self.shapes = shapes

    def total_area(self):
        total = 0
        for shape in self.shapes:
            total += shape.area()
        return total


def main():
    shapes = [Rectangle(1, 6), Rectangle(2, 4)]
    calculator = AreaCalculator(shapes)

    print("The total area is: {}".format(calculator.total_area()))


if __name__ == '__main__':
    main()

# OCP의 나쁜 예제

class Rectangle(object):
    def __init__(self, width, height):
        self.width = width
        self.height = height


class AreaCalculator(object):
    def __init__(self, shapes):
        self.shapes = shapes

    def total_area(self):
        total = 0
        for shape in self.shapes:
            total += shape.width * shape.height
        return total


# def main():
    # shapes = [Rectangle(1, 3), Rectangle(1, 6), Rectangle(3, 6)]
    # calculator = AreaCalculator(shapes)
    # print("The total area is: {}".format(calculator.total_area()))


# if __name__ == '__main__':
    # main()
