class FruitSeller(object):
    def __init__(self, num_apples, price_apple):
        self.num_apples = num_apples
        self.price_apple = price_apple
        self.money = 0

    def sell_apple(self, money):
        num_apple = money // self.price_apple
        self.money += num_apple * self.price_apple
        self.num_apples -= num_apple
        change = money - num_apple * self.price_apple
        return num_apple, change

    def __str__(self):
        return (
            f"<FruitSeller: 남은 사과: {self.num_apples}, 얻은 돈:{self.money}>"
        )

    def __repr__(self):
        return str(self)


class FruitBuyer(object):
    def __init__(self, money):
        self.money = money
        self.num_apples = 0

    def buy_apple(self, seller, money):
        num_apple, change = seller.sell_apple(money)
        self.num_apples += num_apple  # 구매자가 얻는 사과 총 개수
        self.money = self.money - money + change  # 구매자의 재산
        print(f"{money}천원어치 사과 주세요!")

    def __str__(self):
        return (
            f"FruitBuyer : 받은 사과:{self.num_apples}, "
            f"남은 돈:{self.money}, 받은 거스름돈:{self.change}>"
        )

    def __repr__(self):
        return str(self)


class FruitBroker(object):
    def __init__(self, seller_list):
        self.cheap_seller = seller_list[0]
        for seller in seller_list:
            if self.cheap_seller.price_apple > seller.price_apple:
                self.cheap_seller = seller

    def sell_apple(self, money):
        return self.cheap_seller.sell_apple(money)
