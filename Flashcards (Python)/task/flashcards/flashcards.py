class Card:
    def __init__(self, term, definition):
        self.term = term
        self.definition = definition

    def check_answer(self, answer, true_msg='Correct!', false_msg='Wrong!'):
        return true_msg if answer == self.definition else false_msg


class Flashcards:
    def __init__(self, n):
        self.deck = []
        self.make_deck(n)

    def make_deck(self, n):
        for i in range(1, n + 1):
            t = input(f'The term for card #{i}:\n')
            d = input(f'The definition for card #{i}:\n')
            self.deck.append(Card(t, d))

    def play(self):
        for card in self.deck:
            ans = input(f'Print the definition of "{card.term}":\n')
            print(card.check_answer(ans, 'Correct!', f'Wrong. The right answer is "{card.definition}".'))


def main():
    game = Flashcards(int(input('Input the number of cards:\n')))
    game.play()


if __name__ == '__main__':
    main()
