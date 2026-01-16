import os
import threading
from optparse import OptionParser
from minesweeper import Minesweeper
from agent import ManualGuiAgent, RuleBasedAgent
from utils import read_bomb_map

def main():
    """
    Main function to parse command-line options and start the Minesweeper game with the specified agent.

    Command-line options:
    -a, --agent: Type of agent to use (manual or rule_based)
    -m, --map: Path to the bomb map file
    """
    parser = OptionParser()
    parser.add_option("-a", "--agent", dest="agent_type", help="Type of agent to use (manual or rule_based)")
    parser.add_option("-m", "--map", dest="bomb_map_file", help="Path to the bomb map file")

    (options, args) = parser.parse_args()

    if not options.agent_type or not options.bomb_map_file:
        parser.print_help()
        return

    agent_type = options.agent_type.lower()
    bomb_map_file = options.bomb_map_file

    if not os.path.exists(bomb_map_file):
        print(f"Error: The bomb map file '{bomb_map_file}' does not exist.")
        return

    bomb_map = read_bomb_map(bomb_map_file)

    if agent_type == "manual":
        game = Minesweeper(size=len(bomb_map), bomb_map=bomb_map, gui=True)
        agent = ManualGuiAgent(game)
    elif agent_type == "rule_based":
        game = Minesweeper(size=len(bomb_map), bomb_map=bomb_map)
        agent = RuleBasedAgent(game)
    else:
        print("Unknown agent type. Use 'manual' or 'rule_based'.")
        return

    agent_thread = threading.Thread(target=agent.play)
    agent_thread.start()
    if game.gui:
        game.gui.start_gui()

if __name__ == "__main__":
    main()
