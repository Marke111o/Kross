import random

def show_instructions():
    print("""
THIS IS SMASH--THE GAME THAT SIMULATES A CAR RACE.
YOU WILL RESPOND WITH ONE OF THE FOLLOWING MANEUVERS
WHEN A '?' IS TYPED.  THE POSITION NUMBERS REFER TO THE
POINT AT WHICH YOU ARE ON THE TRACK-THEY GO AS FOLLOWS:

  1-THE START LINE
  2-MID STRAIGHT-AWAY
  3-COMING UP ON A LEFT TURN
  4-MID LEFT TURN
  5-COMING UP ON A RIGHT TURN
  6-MID-RIGHT TURN
  7-THE FINISH LINE

     MANEUVERS
  1-FLOOR IT
  2-ACCELERATE(MODERATE)
  3-BRAKE SLIGHT
  4-JAM ON THE BRAKES
  5-SHARP RIGHT
  6-MODERATE RIGHT
  7-SHARP LEFT
  8-MODERATE LEFT
""")

def play_game():
    print("TIME(SEC)".ljust(15), "MILES TO GO".ljust(15), "M.P.H.".ljust(10), "POSITION".ljust(10), "MOVE")
    total_distance = random.randint(10, 15)
    time_elapsed = 0
    mph = 0
    position = 1

    while total_distance > 0:
        print(f"{str(time_elapsed).ljust(15)}{str(total_distance).ljust(15)}{str(mph).ljust(10)}{str(position).ljust(10)}", end="")
        try:
            move = int(input("Enter your move (1-8): "))
            if move < 1 or move > 8:
                raise ValueError("Invalid move")
        except ValueError:
            print("ONE THRU EIGHT ONLY")
            continue

        # Simulate movement
        if move == 1:  # Floor it
            mph = mph * 3 + 20 + random.randint(1, 10)
        elif move == 2:  # Accelerate (moderate)
            mph = mph * 3 // 2 + 7 + random.randint(1, 6)
        elif move == 3:  # Brake slight
            mph = mph * 7 // 8 - 6 + random.randint(1, 4)
        elif move == 4:  # Jam on the brakes
            mph = mph * 4 // 7 - 26 + random.randint(1, 8)
        elif move in (5, 6, 7, 8):  # Turns
            mph = mph * 9 // 10 * (0.7 + random.random() * 0.6)

        if mph < 0:
            mph = 0

        # Check for collisions
        collision_chance = random.randint(1, 100)
        if collision_chance < 10:  # 10% chance of collision
            print("SMASH--YOU HAVE BEEN HIT BY ANOTHER CAR!!")
            print("GAME OVER!")
            return

        time_elapsed += 1
        total_distance -= mph // 120

        if total_distance <= 0:
            print(f"FINISH! You completed the race in {time_elapsed} seconds.")
            print(f"YOUR AVERAGE SPEED WAS {round(total_distance * 3600 / max(1, time_elapsed))} M.P.H.")
            print("THAT ENDS THE RACE.")
            break

        position = random.randint(1, 7)  # Simulate position change

    print("DO YOU WANT TO PLAY AGAIN?")
    again = input("Play again (Y/N)? ").strip().upper()
    if again == "Y":
        play_game()

def main():
    print("                          SMASH")
    print("                    CREATIVE COMPUTING")
    print("                  MORRISTOWN, NEW JERSEY")

    print()
    need_instructions = input("DO YOU NEED INSTRUCTIONS? ").strip().upper()
    if need_instructions == "Y":
        show_instructions()

    play_game()

if __name__ == "__main__":
    main()
