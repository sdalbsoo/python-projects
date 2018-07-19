from re_fruitbroker import FruitBuyer
from re_fruitbroker import FruitSeller
from re_fruitbroker import FruitBroker


def test_FruitBroker():
    buyer = FruitBuyer(70000)
    seller = [
        FruitSeller(30, 3000), FruitSeller(50, 2000),
        FruitSeller(20, 7000), FruitSeller(40, 1500),
    ]
    broker = FruitBroker(seller)
    buyer.buyapple(broker, broker.sellapple(), 30000)
    assert buyer.numapples == 20
    assert buyer.money == 40000
    assert broker.sum_money == 3000
    assert seller[3].money == 27000
    assert seller[3].apple == 20
    assert seller[3].numapples == 20
    buyer.buyapple(broker, broker.sellapple(), 35000)
    assert buyer.numapples == 40
    assert buyer.money == 10000
    assert broker.sum_money == 6000
    assert seller[3].money == 54000
    assert seller[3].apple == 20
    assert seller[3].numapples == 0
