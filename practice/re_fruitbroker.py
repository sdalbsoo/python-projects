class FruitBuyer():
    def __init__(self, money):
        self.money = money
        self.apple_count = 0

    def buy_apples(self, broker, money):
        apples_num, change = broker.cheap_seller.sell_apples(money, broker)
        broker.select_cheapest_seller()
        if self.money < (broker.cheap_seller.price_apple * apples_num):
            raise ValueError()
        elif self.money >= (broker.cheap_seller.price_apple * apples_num):
            self.apple_count += apples_num
            self.money = self.money - broker.cheap_seller.price_apple * apples_num  # noqa

    def __str__(self):
        return(
            f"FruitBuyer: <받은 사과:{self.apple_count}, "
            f"남은 돈: {self.money}>"
        )

    def __repr__(self):
        return str(self)


class FruitSeller():
    def __init__(self, apple_count, price_apple):
        self.apple_count = apple_count
        self.price_apple = price_apple
        self.money = 0
        self.apples_num = 0

    def sell_apples(self, money, broker):
        if (money // self.price_apple) >= self.apple_count:
            self.apples_num = self.apple_count
            self.apple_count = 0
            self.money += (self.apples_num * self.price_apple) - broker.money()  # noqa
            change = money - self.apples_num * self.price_apple
            return self.apples_num, change
        elif 0 <= (money // self.price_apple) < self.apple_count:
            self.apples_num = money // self.price_apple
            self.apple_count -= self.apples_num
            self.money += self.apples_num * self.price_apple - broker.money()
            change = money - (self.apples_num * self.price_apple)
            return self.apples_num, change
        else:
            raise ValueError()

    def __str__(self):
        return (f"FruitSeller: <남은 사과: {self.apple_count}, 얻은 돈:{self.money}>")  # noqa

    def __repr__(self):
        return str(self)


class FruitBroker():
    commission = 0.10

    def __init__(self, sellers):
        self.cheap_seller = sellers[0]
        for seller in sellers:
            if self.cheap_seller.price_apple > seller.price_apple:
                self.cheap_seller = seller
        self.sum_money = 0

    def select_cheapest_seller(self):
        return self.cheap_seller

    def money(self):
        money = (self.cheap_seller.price_apple * self.cheap_seller.apples_num * self.commission)  # noqa
        self.sum_money += money
        return money

    def __str__(self):
        return(f"Broker: <수수료 합계: {self.sum_money}>")

    def __repr__(self):
        return str(self)


def main():
    sellers = [
        FruitSeller(30, 3000), FruitSeller(50, 2500),
        FruitSeller(20, 7000), FruitSeller(40, 1000),
    ]
    broker = FruitBroker(sellers)
    buyer = FruitBuyer(70000)
    buyer.buy_apples(broker, 30000)
    print("=" * 40)
    print(buyer)
    print(broker.select_cheapest_seller())
    print(broker)
    print("=" * 40)
    buyer.buy_apples(broker, 30000)
    print("=" * 40)
    print(buyer)
    print(broker.select_cheapest_seller())
    print(broker)
    print("=" * 40)


if __name__ == "__main__":
    main()
