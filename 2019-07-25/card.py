import collections
import random

Card = collections.namedtuple('Card', ['rank', 'suit'])


class FrenchDeck:
    ranks = [str(n) for n in range(2, 11)] + list('JQKA')
    suits = 'spades dimands clubs hearts'.split()

    def __init__(self):
        self._cards = [Card(rank, suit) for suit in self.suits
                       for rank in self.ranks]

    def __len__(self):
        return len(self._cards)

    def __getitem__(self, positions):  # 把实现[]的方法交给_cards
        return self._cards[positions]

    def __contains__(self, item):
        '''
        只要实现实例是可迭代的 那么 in 运算符就会按顺序做一次迭代搜索
        :param item:
        :return:
        '''
        return item in self._cards

    def shuffle(self):
        '''
        完全公平的洗牌算法
        这个实现并不python,因为FrenchDeck的行为更像序列,如果可以使用random.shuffle就可以更好的利用三方库
        :return:
        '''
        n = len(self._cards) - 1
        while n > 0:
            pos = random.randint(0, n)
            self._cards[n], self._cards[pos] = self._cards[pos], self._cards[n]
            n -= 1

    def __str__(self):
        return 'I am FrenchDeck'


# 使用猴子补丁帮助实现random.shuffle， 需要实现可变协议
def set_card(deck, position, card):
    deck._cards[position] = card


def display(cards):
    for i in cards:
        print(i)


if __name__ == '__main__':
    deck = FrenchDeck()
    # 洗牌
    deck.shuffle()
    # __getitem__
    display(deck[:3])
    # __str__
    print(deck)
    # __contains__
    print(Card(rank='Q', suit='hearts') in deck)
    # 测试第三方库的洗牌 TypeError: 'FrenchDeck' object does not support item assignment
    # 因为FrenchDeck只实现了不可边序列协议
    try:
        print(random.shuffle(deck))
    except Exception as e:
        print(e)

    # 猴子补丁/注意这里是对class
    FrenchDeck.__setitem__ = set_card
    random.shuffle(deck)
    display(deck[:3])

    '''
    特殊方法是给解释器调用的，你自己不需要调用他
    例如len,解释器会直接调用my_obj.__len__()
    如果是内置的数据类型 python解释器会抄近路直接返回
    PyVarObject(内存中长度可变的内置对象C语言结构体) ob_size
    直接读取值比调用方法快多了 复杂度O(1)
    '''

    # 特殊方法的隐式调用
    '''
    for i in x -> for i in iter(x) -> for i in x.__iter__()
    '''


