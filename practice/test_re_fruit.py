import pytest
from re_fruitbroker import FruitBuyer
from re_fruitbroker import FruitSeller
from re_fruitbroker import FruitBroker


def test_FruitBroker():
    buyer = FruitBuyer(70000)
    sellers = [
        FruitSeller(30, 3000), FruitSeller(50, 2000),
        FruitSeller(20, 7000), FruitSeller(40, 1500),
    ]
    broker = FruitBroker(sellers)
    buyer.buy_apples(broker, 30000)
    assert buyer.apple_count == 20
    assert buyer.money == 40000
    assert broker.sum_money == 3000
    assert sellers[3].money == 27000
    assert sellers[3].apples_num == 20
    assert sellers[3].apple_count == 20
    buyer.buy_apples(broker, 35000)
    assert buyer.apple_count == 40
    assert buyer.money == 10000
    assert broker.sum_money == 6000
    assert sellers[3].money == 54000
    assert sellers[3].apples_num == 20
    assert sellers[3].apple_count == 0


    buyer = FruitBuyer(70000)
    sellers = [
        FruitSeller(30, 3000), FruitSeller(50, 1000),
        FruitSeller(20, 7000), FruitSeller(40, 2000),
    ]
    broker = FruitBroker(sellers)
    buyer.buy_apples(broker, 40000)
    assert buyer.apple_count == 40
    assert buyer.money == 30000
    assert broker.sum_money == 4000
    assert sellers[1].money == 36000
    assert sellers[1].apples_num == 40
    assert sellers[1].apple_count == 10
    buyer.buy_apples(broker, 40000)
    assert buyer.apple_count == 50
    assert buyer.money == 20000
    assert broker.sum_money == 5000
    assert sellers[1].money == 45000
    assert sellers[1].apples_num == 10
    assert sellers[1].apple_count == 0

    sellers = [
        FruitSeller(30, 3000), FruitSeller(50, 2000),
        FruitSeller(20, 7000), FruitSeller(40, 1500),
    ]
    broker = FruitBroker(sellers)
    buyer = FruitBuyer(16500)
    with pytest.raises(ValueError,):
        buyer.buy_apples(broker, 19000)
