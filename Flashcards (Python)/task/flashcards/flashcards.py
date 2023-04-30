import argparse
import io
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
        self.deck = []
        self.log_buffer = io.StringIO()
        self.args = self.arguments()
        if self.args.import_from:
            self.import_cards(self.args.import_from)

    def log_out(self, msg):
        print(msg, file=self.log_buffer)
        print(msg)

    def log_in(self, msg):
        print(msg, file=self.log_buffer, end='')
        inp = input(msg)
        print(inp, file=self.log_buffer)
        return inp

    @staticmethod
    def arguments():
        parser = argparse.ArgumentParser()
        parser.add_argument('--import_from')
        parser.add_argument('--export_to')
        return parser.parse_args()

    def menu(self):
        while True:
            cmd = self.log_in('Input the action '
                              '(add, remove, import, export, ask, exit, log, hardest card, reset stats):\n')
            if cmd == 'exit':
                self.log_out('Bye bye!')
                if self.args.export_to:
                    self.export_cards(self.args.export_to)
                break
            elif cmd == 'add':
                self.add_card()
            elif cmd == 'remove':
                self.remove_card(self.log_in('Which card?\n'))
            elif cmd == 'import':
                self.import_cards(self.log_in('File name:\n'))
            elif cmd == 'export':
                self.export_cards(self.log_in('File name:\n'))
            elif cmd == 'ask':
                self.play(int(self.log_in('How many times to ask?\n')))
            elif cmd == 'log':
                self.log(self.log_in('File name:\n'))
            elif cmd == 'hardest card':
                self.hardest_card()
            elif cmd == 'reset stats':
                self.reset_stats()

    def add_card(self):
        t = self.log_in(f'The card:\n')
        t = self.check_duplicate('card', t)
        d = self.log_in(f'The definition of the card:\n')
        d = self.check_duplicate('definition', d)
        self.deck.append({'term': t, 'definition': d, 'mistakes': 0})
        self.log_out(f'The pair ("{t}":"{d}") has been added.\n')

    def remove_card(self, card):
        to_remove = [x for x in self.deck if x['term'] == card]
        if to_remove:
            self.deck.remove(to_remove[0])
            self.log_out('The card has been removed.\n')
        else:
            self.log_out(f'Can\'t remove "{card}": there is no such card.\n')

    def import_cards(self, file):
        if os.access(file, os.F_OK):
            with open(file, 'rt') as f:
                imported = json.loads(f.read())
                for card in imported:
                    if card not in self.deck:
                        self.deck.append(card)
                self.log_out(f'{len(imported)} cards have been loaded.\n')
        else:
            self.log_out('File not found\n')

    def export_cards(self, file):
        with open(file, 'wt') as f:
            f.write(json.dumps(self.deck))
            self.log_out(f'{len(self.deck)} cards have been saved.\n')

    def check_duplicate(self, d_type, data):
        while True:
            try:
                if d_type == 'card' and data in [x['term'] for x in self.deck] \
                        or d_type == 'definition' and data in [x['definition'] for x in self.deck]:
                    raise DuplicatedData(d_type, data)
            except DuplicatedData as dupl:
                data = self.log_in(dupl)
            else:
                break
        return data

    def play(self, n):
        for card in random.choices(list(self.deck), k=n):
            ans = self.log_in(f"Print the definition of \"{card['term']}\":\n")
            if ans == card['definition']:
                self.log_out('Correct!\n')
            else:
                card['mistakes'] += 1
                if ans in [x['definition'] for x in self.deck]:
                    r_term = list(filter(lambda x: x['definition'] == ans, self.deck))[0]['term']
                    self.log_out(f"Wrong. The right answer is \"{card['definition']}\", "
                                 f"but your definition is correct for \"{r_term}\".\n")
                else:
                    self.log_out(f"Wrong. The right answer is \"{card['definition']}\".\n")

    def log(self, file):
        with open(file, 'wt') as f:
            f.write(self.log_buffer.getvalue())
            self.log_out('The log has been saved.\n')

    def hardest_card(self):
        max_mistakes = max([x['mistakes'] for x in self.deck]) if self.deck else 0
        if max_mistakes:
            mistaken = ['"' + x['term'] + '"' for x in self.deck if x['mistakes'] == max_mistakes]
            words = ['card is', 'it'] if len(mistaken) == 1 else ['cards are', 'them']
            self.log_out(f'The hardest {words[0]} {", ".join(mistaken)}. '
                         f'You have {max_mistakes} errors answering {words[1]}.\n')
        else:
            self.log_out('There are no cards with errors.\n')

    def reset_stats(self):
        for card in self.deck:
            card['mistakes'] = 0
        self.log_out('Card statistics have been reset.\n')


def main():
    game = Flashcards()
    game.menu()


if __name__ == '__main__':
    main()
