class DuplicatedData(Exception):
    def __init__(self, d_type, data):
        self.d_type = d_type
        self.data = data
        super().__init__()

    def __str__(self):
        return f'The {self.d_type} "{self.data}" already exists. Try again:\n'


class Flashcards:
    def __init__(self, n):
        self.deck = {}
        self.make_deck(n)

    def make_deck(self, n):
        for i in range(1, n + 1):
            t = input(f'The term for card #{i}:\n')
            t = self.check_duplicate('term', t)
            d = input(f'The definition for card #{i}:\n')
            d = self.check_duplicate('definition', d)
            self.deck[t] = d

    def check_duplicate(self, d_type, data):
        while True:
            try:
                if d_type == 'term' and data in self.deck.keys() \
                        or d_type == 'definition' and data in self.deck.values():
                    raise DuplicatedData(d_type, data)
            except DuplicatedData as dupl:
                data = input(dupl)
            else:
                break
        return data

    def play(self):
        for term, definition in self.deck.items():
            ans = input(f'Print the definition of "{term}":\n')
            if ans == definition:
                print('Correct!')
            elif ans in self.deck.values():
                r_term = list(filter(lambda x: x[1] == ans, self.deck.items()))[0]
                print(f'Wrong. The right answer is "{definition}", but your definition is correct for "{r_term}".')
            else:
                print(f'Wrong. The right answer is "{definition}".')


def main():
    game = Flashcards(int(input('Input the number of cards:\n')))
    game.play()


if __name__ == '__main__':
    main()
