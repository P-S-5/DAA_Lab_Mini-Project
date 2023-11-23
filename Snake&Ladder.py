import random

class Square:
    def __init__(self, number):
        self.number = number
        self.touchpoints = []

    def add_touchpoint(self, touchpoint):
        self.touchpoints.append(touchpoint)

    def display(self, player_positions):
        if not self.touchpoints:
            return f"* {player_positions.get(self.number, ' ')} "
        else:
            return f"{self.touchpoints[0].display()}({player_positions.get(self.number, ' ')})"


class TouchPoint:
    def __init__(self, symbol, sequence_number, entry, exit):
        self.symbol = symbol
        self.sequence_number = sequence_number
        self.entry = entry
        self.exit = exit

    def display(self):
        return f"{self.symbol}{self.sequence_number}"


class Player:
    def __init__(self, sequence_number):
        self.sequence_number = sequence_number
        self.position = 0
        self.entered_game = False
        self.turns = 0


class Board:
    def __init__(self, rows, cols, num_players):
        self.rows = rows
        self.cols = cols
        self.num_players = num_players
        self.board = [[Square(i * cols + j + 1)
                       for j in range(cols)] for i in range(rows)]
        self.players = [Player(i + 1) for i in range(num_players)]
        self.populate_board()

    def populate_board(self):
        # Add snakes and ladders with random touchpoints
        for i in range(1, min(self.rows, self.cols) - 1):
            entry, exit = 0, 0
            while entry >= exit:
                entry = random.randint(1, self.rows * self.cols - 1)
                exit = random.randint(1, self.rows * self.cols - 1)
            if random.choice([True, False]):  # True for ladder, False for snake
                self.board[entry // self.cols][entry % self.cols].add_touchpoint(
                    TouchPoint('L', i, entry, exit)
                )
                self.board[exit // self.cols][exit % self.cols].add_touchpoint(
                    TouchPoint('L', i, entry, exit)
                )
            else:
                self.board[entry // self.cols][entry % self.cols].add_touchpoint(
                    TouchPoint('S', i, entry, exit)
                )
                self.board[exit // self.cols][exit % self.cols].add_touchpoint(
                    TouchPoint('S', i, entry, exit)
                )

    def display(self):
        for i in range(self.rows):
            for j in range(self.cols):
                print(self.board[i][j].display(
                    self.get_player_positions()), end=" ")
            print()

    def get_player_positions(self):
        positions = {}
        for player in self.players:
            if player.entered_game:
                positions[player.position] = f"p{player.sequence_number}"
        return positions

    def play_game(self):
        print("Welcome to the Snakes and Ladders Game!")
        while not all(player.position == self.rows * self.cols for player in self.players[:-1]):
            for player in self.players:
                if not player.entered_game:
                    self.roll_dice_and_enter_game(player)
                else:
                    self.roll_dice_and_move(player)
                self.display()
                if player.position == self.rows * self.cols:
                    print(
                        f"Player {player.sequence_number} won the game with position {player.position} in {player.turns} turns.")
                    self.players.remove(player)
                elif player.position > self.rows * self.cols:
                    print(
                        f"Player {player.sequence_number} lost the game in {player.turns} turns.")
                    self.players.remove(player)
                print()

        print("Game Over!")
        for player in self.players:
            print(
                f"Player {player.sequence_number} lost the game in {player.turns} turns.")

    def roll_dice_and_enter_game(self, player):
        input(
            f"It is player {player.sequence_number}'s turn. Press Enter to roll the dice.")
        dice_value = random.randint(1, 6)
        print(f"Dice is rolled and the value is {dice_value}")
        if dice_value == 6:
            player.entered_game = True
            print(f"Player {player.sequence_number} enters the game.")
        else:
            print("Better luck next time.")

    def roll_dice_and_move(self, player):
        input(f"It is player {player.sequence_number}'s turn. Press Enter to roll the dice.")
        dice_value = random.randint(1, 6)
        print(f"Dice is rolled and the value is {dice_value}")
        player.position += dice_value
        player.turns += 1

        if player.position <= self.rows * self.cols:
            row_index = (player.position - 1) // self.cols
            col_index = (player.position - 1) % self.cols
            square = self.board[row_index][col_index]

            for touchpoint in square.touchpoints:
                if touchpoint.entry == player.position:
                    player.position = touchpoint.exit
                    print(f"Player {player.sequence_number} encountered {touchpoint.symbol}{touchpoint.sequence_number}. "
                        f"Moved to position {player.position}.")
                    break
        else:
            print(f"Player {player.sequence_number} moved beyond the board. Current position: {player.position}")



print("Welcome to the Snakes and Ladders Game!")

if __name__ == "__main__":
    while True:
        try:
            grid_size = input("Enter the grid size (e.g., 5x5): ")
            rows, cols = map(int, grid_size.split("x"))
            if rows <= 0 or cols <= 0:
                raise ValueError("Grid size must be positive.")
            break
        except ValueError as e:
            print(f"Invalid input: {e}")

    while True:
        try:
            num_players = int(
                input("Enter the number of players (at least 2): "))
            if num_players < 2:
                raise ValueError("Number of players should be at least two.")
            break
        except ValueError as e:
            print(f"Invalid input: {e}")

    game_board = Board(rows, cols, num_players)
    print("Initializing the {}x{} Board.".format(rows, cols))
    print("Board is initialized.")
    print("Starting the Game:")
    game_board.display()
    game_board.play_game()
