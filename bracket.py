import copy
import math
import random
import sys


def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n): yield l[i:i + n]


class Match:
    def __repr__(self):
        y = "[{} ".format(self.p1)
        y += "<" if self.result == 1 else ""
        y += "--"
        y += ">" if self.result == 2 else ""
        y += " {}]".format(self.p2)
        return y

    def __init__(self, pair):
        self.p1 = pair[0]
        self.p2 = pair[1] if len(pair) == 2 else None

        self.result = 0

        # p1 is automatic winner if there's no p2
        if not self.p2:
            self.result = 1
            
    def is_recorded(self):
        return bool(self.result)

    def contains_participants(self, p1, p2):
        return (self.p1 == p1 and self.p2 == p2) or (self.p1 == p2 and self.p2 == p1)

    def record_winner(self, winner):
        self.result = 1 if self.p1 == winner else 2 if self.p2 == winner else 0
        if not self.result:
            print("Match.record_winner: winner does not exist in this match")
        return self.result

    @property
    def winner(self):
        return self.p1 if self.result == 1 else self.p2 if self.result == 2 else None

    @property
    def players(self):
        return [self.p1, self.p2]

class Bracket:
    def __repr__(self):
        y = "-- Current Round {} --\n".format(self.round+1)
        y += repr(self.matchlist_for_round) + "\n"
        return y

    def __init__(self, names):
        self.round = 0
        self.participants = names
        self.n = len(names)
        self.n_matches = math.ceil(math.log2(self.n))

        random.shuffle(self.participants)
        self.matches = [[] for i in range(self.n_matches)]
        self.matches[0] = [Match(pair) for pair in chunks(self.participants, 2)]

    @property
    def matchlist_for_round(self):
        return self.matches[self.round]

    @property
    def bracket_is_done(self):
        return self.round == self.n_matches

    @property
    def round_is_ready(self):
        return bool(self.matchlist_for_round)

    @property
    def round_is_done(self):
        return sum(match.is_recorded() for match in self.matchlist_for_round) == len(self.matchlist_for_round)

    def all_participants_in_round(self, i):
        y = list()
        for match in self.matches[i]: y.extend(match.players)
        return y

    def record_match(self, winner, loser):
        if not self.round_is_ready:
            print("Bracket.record_match: match is not ready yet. call Bracket.setup_round()")
            return False

        # Search for the right match
        for match in self.matchlist_for_round:
            if match.contains_participants(winner, loser):
                break
        
        # Record victor
        success = match.record_winner(winner)

        # Check for end of round
        if self.round_is_done:
            print("Bracket.record_match: round {} is over".format(self.round))
            self.complete_round()

        return True

    def complete_round(self):
        # Make sure this doesn't get called before the round is done
        if not self.round_is_done:
            print("Bracket.complete_round: round is not done yet")
            return False

        # Increment round and set it up
        self.round += 1
        if self.bracket_is_done:
            print("Bracket.complete_round: bracket is complete")
            print("  The Winner is {}".format(self.matches[self.round-1][0].winner))
            return

        print("Bracket.complete_round: Starting round {}".format(self.round))

        next_rd = [match.winner for match in self.matches[self.round-1]]
        #random.shuffle(next_rd)

        self.matches[self.round] = [Match(pair) for pair in chunks(next_rd, 2)]
        return True

    def simulate_round(self):
        for match in self.matchlist_for_round: match.result = random.randint(1, 2)
        self.complete_round()

    @staticmethod
    def load_from_file(fname):
        with open(fname) as fp:
            names = fp.read().split("\n")
        return Bracket(names)
        
    @staticmethod
    def prompt_for_bracket():
        done = False
        names = []
        while not done:
            print(names)
            user_input = input("Please type in a name: ")
            if not len(user_input):
                break
                
            names.append(user_input)
    
        return Bracket(names)
