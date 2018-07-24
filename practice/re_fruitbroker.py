class FruitBuyer():
    def __init__(self, money):
        self.money = money
        self.num_apples = 0
        self.change = 0

    def buy_apples(self, broker, money):
        num_apples, self.change = broker.sell_apples(money)
        if self.money < (broker.cheap_seller.price_apple * num_apples):
            raise ValueError("입력을 잘못하셨습니다.")
        elif self.money >= (broker.cheap_seller.price_apple * num_apples):
            self.num_apples += num_apples
            self.money = self.money - broker.cheap_seller.price_apple * num_apples # noqa

    def __str__(self):
        return(
            f"FruitBuyer: <받은 사과:{self.num_apples}, "
            f"남은 돈: {self.money}, "
            f"거스름돈: {self.change}>"
        )

    def __repr__(self):
        return str(self)


class FruitSeller():
    commission = 0.1

    def __init__(self, num_apples, price_apple):
        self.num_apples = num_apples
        self.price_apple = price_apple
        self.money = 0

    def sell_apples(self, money):
        if (money // self.price_apple) >= self.num_apples:
            num_apples = self.num_apples
            self.num_apples = 0
            self.money += (num_apples * self.price_apple) - (self.commission * num_apples * self.price_apple)  # noqa
            return num_apples
        elif 0 <= (money // self.price_apple) < self.num_apples:
            num_apples = money // self.price_apple
            self.num_apples -= num_apples
            self.money += num_apples * self.price_apple - (self.commission * num_apples * self.price_apple)  # noqa
            return num_apples
        else:
            raise ValueError("입력을 잘못하셨습니다.")

    def __str__(self):
        return (f"FruitSeller: <남은 사과: {self.num_apples}, 얻은 돈:{self.money}>")  # noqa

    def __repr__(self):
        return str(self)


class FruitBroker():
    def __init__(self, sellers):
        self.cheap_seller = sellers[0]
        self.sellers = sellers
        self.money = 0

    def select_cheapest_seller(self):
        for seller in self.sellers:
            if self.cheap_seller.price_apple > seller.price_apple:
                self.cheap_seller = seller
        return self.cheap_seller

    def sell_apples(self, money):
        cheap_seller = self.select_cheapest_seller()
        num_apples = cheap_seller.sell_apples(money)
        self.money += (num_apples * cheap_seller.price_apple * cheap_seller.commission)  # noqa
        change = money - (num_apples * cheap_seller.price_apple)
        return num_apples, change

    def __str__(self):
        return(f"Broker: <수수료 합계: {self.money}>")

    def __repr__(self):
        return str(self)


def main():
    sellers = [
        FruitSeller(30, 3000), FruitSeller(50, 2500),
        FruitSeller(20, 7000), FruitSeller(90, 1500),
    ]
    broker = FruitBroker(sellers)
    buyer = FruitBuyer(50000)
    buyer.buy_apples(broker, 11200)
    print("=" * 40)
    print(buyer)
    print(broker.cheap_seller)
    print(broker)
    print("=" * 40)
    buyer.buy_apples(broker, 10000)
    print("=" * 40)
    print(buyer)
    print(broker.cheap_seller)
    print(broker)
    print("=" * 40)


if __name__ == "__main__":
    main()
