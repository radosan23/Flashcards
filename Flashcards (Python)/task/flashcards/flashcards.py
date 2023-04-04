class Card:
    def __init__(self, term, definition):
        self.term = term
        self.definition = definition

    def check_answer(self, answer, true_msg='Right answer!', false_msg='Wrong answer!'):
        return true_msg if answer == self.definition else false_msg


def main():
    card = Card(input(), input())
    print(card.check_answer(input()))


if __name__ == '__main__':
    main()
