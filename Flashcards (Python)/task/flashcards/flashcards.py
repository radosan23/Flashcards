import json
import os
import random


class DuplicatedData(Exception):
    def __init__(self, d_type, data):
        self.d_type = d_type
        self.data = data
        super().__init__()

    def __str__(self):
        return f'The {self.d_type} "{self.data}" already exists. Try again:\n'


class Flashcards:
    def __init__(self):
        self.deck = {}

    def menu(self):
        while True:
            cmd = input('Input the action (add, remove, import, export, ask, exit):\n')
            if cmd == 'exit':
                print('Bye bye!')
                break
            elif cmd == 'add':
                self.add_card()
            elif cmd == 'remove':
                self.remove_card(input('Which card?\n'))
            elif cmd == 'import':
                self.import_cards(input('File name:\n'))
            elif cmd == 'export':
                self.export_cards(input('File name:\n'))
            elif cmd == 'ask':
                self.play(int(input('How many times to ask?\n')))

    def add_card(self):
        t = input(f'The card:\n')
        t = self.check_duplicate('card', t)
        d = input(f'The definition of the card:\n')
        d = self.check_duplicate('definition', d)
        self.deck[t] = d
        print(f'The pair ("{t}":"{d}") has been added.\n')

    def remove_card(self, card):
        if card in self.deck.keys():
            self.deck.pop(card)
            print('The card has been removed.\n')
        else:
            print(f'Can\'t remove "{card}": there is no such card.\n')

    def import_cards(self, file):
        if os.access(file, os.F_OK):
            with open(file, 'rt') as f:
                imported = json.loads(f.read())
                self.deck.update(imported)
                print(f'{len(imported)} cards have been loaded.\n')
        else:
            print('File not found\n')

    def export_cards(self, file):
        with open(file, 'wt') as f:
            f.write(json.dumps(self.deck))
            print(f'{len(self.deck)} cards have been saved.\n')

    def check_duplicate(self, d_type, data):
        while True:
            try:
                if d_type == 'card' and data in self.deck.keys() \
                        or d_type == 'definition' and data in self.deck.values():
                    raise DuplicatedData(d_type, data)
            except DuplicatedData as dupl:
                data = input(dupl)
            else:
                break
        return data

    def play(self, n):
        for term, definition in random.choices(list(self.deck.items()), k=n):
            ans = input(f'Print the definition of "{term}":\n')
            if ans == definition:
                print('Correct!')
            elif ans in self.deck.values():
                r_term = list(filter(lambda x: x[1] == ans, self.deck.items()))[0]
                print(f'Wrong. The right answer is "{definition}", but your definition is correct for "{r_term}".')
            else:
                print(f'Wrong. The right answer is "{definition}".')


def main():
    game = Flashcards()
    game.menu()


if __name__ == '__main__':
    main()
