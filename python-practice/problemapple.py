class FruitSeller(object):
    def __init__(self, num_apple, price_apple):
        self.num_apple = num_apple
        self.price_apple = price_apple
        self.money = 0

    def give_apple(self, order_apple_money):
        give_num_apple = order_apple_money // self.price_apple
        self.money += give_num_apple*self.price_apple
        self.num_apple -= give_num_apple
        return give_num_apple, self.price_apple        

    def __str__(self):
        return "<FruitSeller: apple:{}, money:{}>".format(self.num_apple, self.money)
        
class FruitBuyer(object):
    def __init__(self, money):
        self.money = money
        self.get_num_apple = 0
        self.charge = 0

    def order_fruit(self, seller, order_apple_money):
        self.get_apple, price_apple = seller.give_apple(order_apple_money) # 리턴값 2개이니까 주고 받는 사과 개수, 사과 1개 당 가격 리턴됨
        self.get_num_apple += self.get_apple     # 구매자가 얻는 사과 총 개수
        self.money -= self.get_apple*price_apple    # 구매자의 재산
        self.charge = (order_apple_money - self.get_apple * price_apple)

    def __str__(self):
        return "<FruitBuyer : apple:{}, money:{}, charge:{}>".format(self.get_num_apple, self.money, self.charge)


seller1 = FruitSeller(30, 3000) # seller1은 사과 30개 보유 및 3000원에 판매 중
print(seller1) # 사과 보유량 확인.

buyer1 = FruitBuyer(50000) # buyer1은 5만원 보유 중
buyer1.order_fruit(seller1, 5000) # 구매자가 5천원어치 사과를 주문
print("5천원어치 사과 줘!")
print(buyer1, seller1) # 구매자와 판매자의 상황 출력
buyer1.order_fruit(seller1, 6000) # 구매자가 6천원어치 사과를 주문
print("6천원어치 사과 줘!")
print(buyer1, seller1) # 구매자와 판매자의 상황 출력
buyer1.order_fruit(seller1, 7000) # 구매자가 7천원어치 사과를 주문
print("7천원어치 사과 줘!")
print(buyer1, seller1) # 구매자와 판매자의 상황 출력
print('-------------------------------------------')
print('-------------------------------------------')

seller2 = FruitSeller(50, 2000)
print(seller2)
buyer2 = FruitBuyer(50000)
buyer2.order_fruit(seller2, 7000)
print("7천원어치 사과 줘!")
print(buyer2, seller2)
buyer2.order_fruit(seller2, 9000)
print("9천원어치 사과 줘!")
print(buyer2, seller2)
