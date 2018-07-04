class FruitSeller(object):
    def __init__(self, num_apple, price_apple):
        self.num_apple = num_apple
        self.price_apple = price_apple
        self.money = 0

    def give_apple(self, apple_money):
        num_apple = apple_money // self.price_apple
        self.money += num_apple*self.price_apple
        self.num_apple -= num_apple
        change = apple_money - num_apple * self.price_apple
        return num_apple, change        

    def __str__(self):
        return "<FruitSeller: 남은 사과:{}, 얻은 돈:{}>".format(self.num_apple, self.money)
        
class FruitBuyer(object):
    def __init__(self, money):
        self.money = money
        self.all_apple = 0

    def order_fruit(self, seller, apple_money):
        self.num_apple, self.change = seller.give_apple(apple_money) # 리턴값 2개이니까 주고 받는 사과 개수, 거스름돈 리턴됨 
        self.all_apple += self.num_apple     # 구매자가 얻는 사과 총 개수
        self.money = self.money - apple_money + self.change    # 구매자의 재산
        print("%s천원어치 사과 주세요!" %apple_money)

    def __str__(self):
        return "FruitBuyer : 받은 사과:{}, 남은 돈:{}, 받은 거스름돈:{}>".format(self.all_apple, self.money, self.change)


seller1 = FruitSeller(30, 3000) # seller1은 사과 30개 보유 및 3000원에 판매 중
print(seller1) # 사과 보유량 확인.

buyer1 = FruitBuyer(50000) # buyer1은 5만원 보유 중
buyer1.order_fruit(seller1, 5000) # 구매자가 5천원어치 사과를 주문
print(buyer1, seller1) # 구매자와 판매자의 상황 출력
buyer1.order_fruit(seller1, 6000) # 구매자가 6천원어치 사과를 주문
print(buyer1, seller1) # 구매자와 판매자의 상황 출력
buyer1.order_fruit(seller1, 7000) # 구매자가 7천원어치 사과를 주문
print(buyer1, seller1) # 구매자와 판매자의 상황 출력
print('-------------------------------------------')
print('-------------------------------------------')

seller2 = FruitSeller(50, 2000)
print(seller2)
buyer2 = FruitBuyer(50000)
buyer2.order_fruit(seller2, 7000)
print(buyer2, seller2)
buyer2.order_fruit(seller2, 9000)
print(buyer2, seller2)
