# blackjack

This project aims to help players of blackjack to increase the winning ratio.

## Program runtime mode

1. Control Mode
    - By setting `game_controller.control = True`.
    - Program will ask user to input cards and the decision of players of whether to request extra cards.
2. Simulation Mode
    - By setting `game_controller.control = False`.
    - Set `game_controller.pause = True` if wish to pause between rounds.
    - Set `game_controller.use_advice = True` if wish to use simulation result as decision. Otherwise the decision will be made depending on the hand value probabilistically.

## Argument Handler

In Control Mode, user can input command for viewing cards, running simulation, restarting game, etc. The list of commands is as follows:

| command | Description |
| ------- | ----------- |
| `/go` | Force bypass the input request. |
| {empty} | Bypass if an input is not required. |
| `/re` | Restart the round by putting the cards in players' hands back to the card deck. |
| `/RE` | Restart the game. |
| `/hands` | View the cards on hand of all players with limited visibility. Add `-f` to enable full visibility. |
| `/info` | View the status, status_reason, and hand of all players with limited visibility. Add `-f` to enable full visibility. |
| `/cards` | Show the number of cards remaining per rank |
| `/sim` | Run simulation and show simulation result. Add `-l` to view detailed simulation result. Add `-r` to re-run simulation. |
| `/ad` | Show advice based on the simulation result. Add `-r` to re-run simulation. |
