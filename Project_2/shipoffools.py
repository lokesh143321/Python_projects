from random import randint
""" Import randint() function from random module to obtain random values of dices"""


class Die:
    """ Die class is responsible for handling randomly generated integer values between 1 and 6."""

    def __init__(self):
        self._value = 1  # initialize default value to variable _value as 1 to store the die value

    # A func which return th integer value if dice
    def get_value(self) -> int:
        return self._value

    # Func which generates the random value of range 1 to 6
    def roll(self) -> None:
        rolling = randint(1, 6)
        self._value = rolling


class DiceCup:

    """This class is responsible to handles dices of class Die.
    and has the ability to bank and release dice individually"""

    # storing the die obj in the list _dice.
    def __init__(self, num_of_dices):
        self.dice_cup_list = [0, 0, 0, 0, 0]
        self.num_of_dices = num_of_dices
        self._dice = []
        i = 0
        while (i < self.num_of_dices):
            self._dice.append(Die())
            i += 1

    # this func calls the roll() func in Die class for every single Die obj
    def roll(self) -> None:
        i = 0
        while i < self.num_of_dices:
            if(self.dice_cup_list[i] == 0):
                # print(self._dice[i].get_value())
                self._dice[i].roll()
            i = i+1
        i = i-1
        return self._dice[i].get_value()

    # This function takes index as parameter and returns the integer random value of respective Die index
    def value(self, index: int) -> int:
        index_val = self._dice[index].get_value()
        return index_val

    # This function takes index as parameter and banks the value of the given index.
    def bank(self, index: int) -> None:
        self.index = index
        self.dice_cup_list[self.index] = 1

    # This function takes index as parameter and checks whether that particular index is banked or not.

    def is_banked(self, index: int) -> bool:
        # x = True
        # y = False
        if(self.dice_cup_list[index] == 1):
            return True
        else:
            return False

    # This function takes index as a parameter and unbank that particular index and assign
    def release(self, index: int) -> None:
        self.dice_cup_list[index] = 0

    # This function unbank all Dices and assign False for all values in list b_list.

    def release_all(self) -> None:
        self.dice_cup_list = [0, 0, 0, 0, 0]


class ShipOfFoolsGame:

    """ ShipOfFoolsGame class is responsible for the game logic and has the ability to play a round of the game resulting in a score.Each player plays three rounds.Also has a property that tells what accumulated score results in a winning state,for example 21"""

    def __init__(self):
        self._winning_score = 21
        self._cup = DiceCup(5)

    def round(self) -> int:
        has_ship = False
        has_captain = False
        has_crew = False
# sum of the remaining dices,i.e., the score.
        crew = 0
# Repeat 3 times
        self._cup.release_all()
        self._cup.roll()
        i = 0
        while i < 3:
            lst = []
            for j in range(5):
                lst.append(self._cup._dice[j].get_value())
            print(lst)
            if not has_ship and (6 in lst):
                check_1 = lst.index(6)
                self._cup.bank(check_1)
                has_ship = True
            else:
                if(has_ship):
                    pass
                else:
                    self._cup.roll()
            if has_ship and not has_captain and (5 in lst):
                check_2 = lst.index(5)
                self._cup.bank(check_2)
                # A ship but not a captain is banked
                has_captain = True
            else:
                if(has_captain):
                    pass
                else:
                    self._cup.roll()
            if has_captain and not has_crew and (4 in lst):
                # A ship and captain but not a crew is banked
                check_3 = lst.index(4)
                self._cup.bank(check_3)
                has_crew = True
            else:
                if(has_crew):
                    pass
                else:
                    self._cup.roll()
            if has_ship and has_captain and has_crew:
                # We got all needed dice, and can bank the ones we like.
                # bank all unbanked dice > 3
                if(i < 2):
                    dice_list = []
                    k = 0
                    while k < 5:
                        if(self._cup.is_banked(k)):
                            k = k+1
                            pass
                        else:
                            dice_list.append(k)
                            print("Unbanked index: ", k)
                            k = k+1

                    if(len(dice_list) == 2):
                        no_of_indexes = int(
                            input("Enter number of indexes to be banked: "))
                        if(no_of_indexes == 0):
                            self._cup.roll()
                        elif(no_of_indexes == 1):
                            idx_1 = int(
                                input("Enter the index: "))
                            self._cup.bank(idx_1)
                            self._cup.roll()
                        elif(no_of_indexes == 2):
                            self._cup.bank(dice_list[0])
                            self._cup.bank(dice_list[1])
                            print(lst)
                            break
                        else:
                            print(
                                "** wrong input,previous input is considered as input **")
                            break
                    elif(len(dice_list) == 1):
                        x1 = int(input("Enter 1 for roll and 2 for bank: "))
                        if(x1 == 1):
                            self._cup.roll()
                        elif(x1 == 2):
                            print(lst)
                            self._cup.bank(dice_list[0])
                            break
                        else:
                            print(
                                "** wrong input,previous input is considered as input **")
                            break
                else:
                    for y in range(5):
                        if(self._cup.is_banked(y)):
                            pass
                        else:
                            self._cup.bank(y)
            i = i+1
# If ship is present, captain and crew (sum 15),
# calculate the sum of the two remaining.
        if has_ship and has_captain and has_crew:
            crew = sum(lst) - 15
            print("\nfinal dices -->", lst)
            print("Score of this round:\n", crew, "\n")

            return crew
        else:
            print("\nfinal dices--> ", lst)
            print("Score of this round: ", crew, "\n")

            return crew


class PlayRoom:

    """PlayRoom class is Responsible for handling a number of players and a game. 
    Every round the room lets each player play, and afterwards check if any player have reached the winning score."""

    def __init__(self):
        self._players = []

    def set_game(self, object: ShipOfFoolsGame) -> None:
        self._game = object

    def add_player(self, player_1) -> None:
        self._players.append(player_1)

    def reset_scores(self) -> None:
        i = 0
        while i < len(self._players):
            # for i in range(len(self._players)):
            self._players[i].reset_score()
            i = i+1

    def play_round(self) -> None:
        i = 0
        while i < len(self._players):
            # for i in range(len(self._players)):
            self._players[i].play_round(self._game)
            i = i+1

    def game_finished(self) -> bool:
        list_1 = []
        i = 0
        while i < len(self._players):
            # for i in range(len(self._players)):
            if(self._players[i].current_score() >= 21):
                # print("True")
                list_1.append(1)
            else:
                # print("False")
                list_1.append(0)
        # print(list_1)
            i = i+1
        return any(list_1)

    # func gives each players score in each round
    def print_scores(self) -> None:
        for i in range(len(self._players)):
            print(Player.name_of_the_player[i], ": ",
                  self._players[i].current_score())
        print()

    # func gives prints the winner of the game who gets score grater than or equal to 21
    def print_winner(self) -> None:
        i = 0
        while i < len(self._players):
            # for i in range(len(self._players)):
            if(self._players[i].current_score() >= 21):
                print("Winner is:", Player.name_of_the_player[i])
            i = i+1


class Player:

    """Player class is responsible for the score of the individual player. 
    Has the ability, given a game logic, play a round of a game. The gained score is accumulated in the attribute score."""

    name_of_the_player = []

    def __init__(self, name):
        self._name = self.set_name(name)
        self._score = 0
        Player.name_of_the_player.append(self._name)

    def set_name(self, namestring: str) -> None:
        return namestring

    def current_score(self) -> None:
        return self._score

    def reset_score(self) -> None:
        self._score = 0

    def play_round(self, game_object: ShipOfFoolsGame) -> None:
        object = game_object
        self._score = self._score + object.round()


if __name__ == "__main__":
    room = PlayRoom()
    room.set_game(ShipOfFoolsGame())
    room.add_player(Player("Lokesh"))
    room.add_player(Player("Sai ram"))
    room.reset_scores()
    i = 1
    while not room.game_finished():
        print("   @Round -->", i)
        room.play_round()
        room.print_scores()
        i = i+1
    room.print_winner()
