from fruit import FruitBroker
from fruit import FruitBuyer
from fruit import FruitSeller


def test_fruit1():
    seller = FruitSeller(30, 3000)
    buyer = FruitBuyer(50000)
    buyer.buy_apple(seller, 8000)
    assert buyer.money == 44000
    assert buyer.num_apples == 2
    assert seller.num_apples == 28
    assert seller.money == 6000


def test_fruit2():
    seller_list = [
        FruitSeller(30, 3000), FruitSeller(50, 2000), FruitSeller(70, 1000)
    ]
    buyer = FruitBuyer(50000)
    broker = FruitBroker(seller_list)
    buyer.buy_apple(broker, 8000)
    assert buyer.money == 42000
    assert buyer.num_apples == 8
    assert seller_list[0].num_apples == 30
    assert seller_list[1].num_apples == 50
    assert seller_list[2].num_apples == 62
    assert seller_list[2].price_apple == 1000
    assert seller_list[2].money == 8000
