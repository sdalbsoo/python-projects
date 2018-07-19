import sys


class FruitBuyer():
    def __init__(self, money):
        self.money = money
        self.numapples = 0

    def buyapple(self, broker, seller, money):
        getapple, change = seller.sellapple(money, broker)
        if self.money < (seller.priceapple * getapple):
            print("돈이 부족합니다. 돈 가져오세요.")
            sys.exit(1)
        elif self.money >= (seller.priceapple * getapple):
            self.numapples += getapple
            self.money = self.money - seller.priceapple * getapple

    def __str__(self):
        return(
            f"FruitBuyer: <받은 사과:{self.numapples}, "
            f"남은 돈: {self.money}>"
        )

    def __repr__(self):
        return str(self)


class FruitSeller():
    def __init__(self, numapples, priceapple):
        self.numapples = numapples
        self.priceapple = priceapple
        self.money = 0
        self.apple = 0

    def sellapple(self, money, broker):
        if (money // self.priceapple) >= self.numapples:
            self.apple = self.numapples
            self.numapples = 0
            self.money += (self.apple * self.priceapple) - broker.money()  # noqa
            change = money - self.apple * self.priceapple
            return self.apple, change
        elif 0 <= (money // self.priceapple) < self.numapples:
            self.apple = money // self.priceapple
            self.numapples -= self.apple
            self.money += self.apple * self.priceapple - broker.money()
            change = money - (self.apple * self.priceapple)
            return self.apple, change
        else:
            print("입력을 잘못하셨습니다.")
            sys.exit(1)

    def __str__(self):
        return(f"FruitSeller: <남은 사과: {self.numapples}, 얻은 돈:{self.money}>")  # noqa

    def __repr__(self):
        return str(self)


class FruitBroker():
    commission = 0.10

    def __init__(self, seller):
        self.cheap_seller = seller[0]
        for choice_seller in seller:
            if self.cheap_seller.priceapple > choice_seller.priceapple:
                self.cheap_seller = choice_seller
        self.sum_money = 0

    def sellapple(self):
        return self.cheap_seller

    def money(self):
        money = (self.cheap_seller.priceapple * self.cheap_seller.apple * self.commission)  # noqa
        self.sum_money += money
        return money

    @classmethod
    def change_commission(cls, commission):
        while commission > 1:
            print("[경고] 수수료가 '1'보다 클 수 없습니다.")
            commission = input("[입력] 수수료를 다시 입력하여 주십시오.\n=> ")
            commission = float(commission)
        cls.commission = commission

    def __str__(self):
        return(f"Broker: <수수료 합계: {self.sum_money}>")

    def __repr__(self):
        return str(self)


def main():
    buyer = FruitBuyer(17500)
    seller = [
        FruitSeller(30, 3000), FruitSeller(50, 500),
        FruitSeller(20, 7000), FruitSeller(40, 1500),
    ]
    broker = FruitBroker(seller)
    buyer.buyapple(broker, broker.sellapple(), 17000)
    print("=" * 40)
    print(buyer)
    print(broker.sellapple())
    print(broker)
    print("=" * 40)


if __name__ == "__main__":
    main()
