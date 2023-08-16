# Python Games made with Pygame

These are the games I made a couple of years ago when I was learning to code and started building projects.
I didn't uploaded these on Github at that time because I didn't knew how to to use Github very well.
So I am uploading these all now. They were created by me in about 2019 - 2021.


## Contents
- Setup and Installation
- Games Description
    - Car Game
    - Knife Hit
    - Pong Game
    - Space Invaders
    - Space Ship
    - Tic Tac Toe
- Contribution
- License

## Setup and Installation

Before running the game, you need to have Python installed on your system.
<br>
You can download Python from the official website: https://www.python.org/downloads/

1. Download and extract this project and open the terminal on the same location where **all python files** are present.

2. Use the following command to create a virtual environment and activate it: [Learn More](https://rb.gy/n20ae)

    For Windows
    ```bash
    python -m venv .venv
    ```
    For MacOS / Linux
    ```
    python3 -m venv .venv
    ```

3. Activate the virtual environment by using:

    For Windows
    ```
    .venv/Scripts/activate.bat
    ```
    For macOS
    ```
    source .venv/bin/activate
    ```
  
   - For more info: [click here](https://rb.gy/n20ae)

4. To install Pygame, just run the following command:
   ```
   pip install pygame
   ```
5. The installation process is complete and you can now play all of the games easily.

## Games Description

### Car Game
A simple Car controlling game where you have to dodge incoming cars.

- Use the following command in terminal to play:
    ```bash
    python car_game.py # Windows
    python3 car_game.py # MacOS/Linux
    ```
- Use **Arrow Keys** to control the car.
- The longer you dodge the more score you get.
- When you collide with a car, just wait for 2 seconds and game will restart.

### Knife Hit
Throw all the knifes without failing onto the board and advance to next stage.

- Use the following command in terminal to play:
    ```bash
    python knife_hit.py # Windows
    python3 knife_hit.py # MacOS/Linux
    ```
- Pres **Space bar** to throw the knifes on the board.
- Press **Any other Key** when all the knifes are thrown to go to next stage.
- When you fail to throw the knife, game will automatically restart from stage 1.

### Pong Game
A Simple two player pong game.

- Use the following command in terminal to play:
    ```bash
    python pong_game.py # Windows
    python3 pong_game.py # MacOS/Linux
    ```
- Player on **left** uses **W and S** keys to move their paddle.
- Player on **right** uses **Up and Down** keys to move their paddle.
- When an opponent misses the ball, the player gets a points and game continue.

### Space Invaders
Defend your planet by destroying enemy ships and preventing invasion.

- Use the following command in terminal to play:
    ```bash
    python space_invaders.py # Windows
    python3 space_invaders.py # MacOS/Linux
    ```
- Use **W A S D** keys to move your ship and Use **Space** to shoot lasers at enemies.
- Collision with an enemy ship reduces 10 health. Red laser reduces 10 health. Blue laser reduces 5 health and Green laser reduces 2 health.
- If 5 ships invades the planet then game is over.
- Click on the **pause** button to pause/play the game at any time.

### Space Ship
Simple asteroid avoidance game where you have to dodge asteroids and survive for as long as possible.

- Use the following command in terminal to play:
    ```bash
    python space_ship.py # Windows
    python3 space_ship.py # MacOS/Linux
    ```
- Move your ship with the help of mouse pointer.
- Use **Space Key** to shoot lasers and destroy asteroids.
- You have 5 lives and each time to collide with an asteroid you lose one life.
- When the game is Over, press **Any Key** to restart the game.

### Tic Tac Toe
 
A Simple two player game of Tic Tac Toe to play with your friends.

- Use the following command in terminal to play:
    ```bash
    python tic_tac_toe.py # Windows
    python3 tic_tac_toe.py # MacOS/Linux
    ```
- When the above command is executed, it will ask for players name, enter the names you want.
- Move the box by pressing **Arrow Keys** and choose your desired location.
- Press **Enter Key** to put your symbol in the location you have choosen.
- The game continues whenever someone wins or the game draws. The points are added to the winning player score.
