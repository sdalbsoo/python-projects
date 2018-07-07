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
        return "<FruitSeller: 남은 사과:{}, 얻은 돈:{}>".format(self.num_apples, self.money)  # noqa


class FruitBuyer(object):
    def __init__(self, money):
        self.money = money
        self.num_apples = 0

    def buy_apple(self, seller, money):
        self.num_apple, self.change = seller.sell_apple(money)
        self.num_apples += self.num_apple     # 구매자가 얻는 사과 총 개수
        self.money = self.money - money + self.change    # 구매자의 재산
        print(f"{money}천원어치 사과 주세요!")

    def __str__(self):
        return "FruitBuyer : 받은 사과:{}, 남은 돈:{}, 받은 거스름돈:{}>".format(self.num_apples, self.money, self.change)  # noqa


class FruitBroker(object):
    def __init__(self, seller):
       self.money = 0
        
    def choice_cheap_apple(self, seller):
        sorted(seller, key = lambda x: x[1])
        return seller[0]
        



seller_list = [
    FruitSeller(30, 3000), FruitSeller(50, 2000), FruitSeller(70, 1000)
]

buyer1 = FruitBuyer(50000)  # buyer1은 5만원 보유 중
broker = FruitBroker(seller)  # 브로커가 판매자1,2,3중 가장 싼 사과 선택
print(broker.choice_cheap_apple(seller))

buyer1.buy_apple(seller1, 6000)  # 구매자가 6천원어치 사과를 주문
buyer1.buy_apple(seller1, 7000)  # 구매자가 7천원어치 사과를 주문
print('-------------------------------------------')
print('-------------------------------------------')
