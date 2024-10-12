import random
import time
import json
import os
import sys
from sympy import symbols, Eq, solve, expand, integrate, diff, simplify
from sympy.core.sympify import SympifyError
from statistics import multimode, mean, median, stdev
from colorama import init, Fore, Style

init(autoreset=True)

INTERFACE_WIDTH = 120

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_centered(text, color=Fore.WHITE):
    lines = text.split('\n')
    for line in lines:
        print(color + line.center(INTERFACE_WIDTH))

def print_header():
    clear_console()
    title_art = r"""
        _        _                  _              _                   _         _               
       / /\     /\_\               /\ \           / /\                /\_\      /\_\             
      / /  \   / / /         _    /  \ \         / /  \              / / /  _  / / /         _   
     / / /\ \__\ \ \__      /\_\ / /\ \_\       / / /\ \            / / /  /\_\\ \ \__      /\_\ 
    / / /\ \___\\ \___\    / / // / /\/_/      / / /\ \ \          / / /__/ / / \ \___\    / / / 
    \ \ \ \/___/ \__  /   / / // / / ______   / / /  \ \ \        / /\_____/ /   \__  /   / / /  
     \ \ \       / / /   / / // / / /\_____\ / / /___/ /\ \      / /\_______/    / / /   / / /   
 _    \ \ \     / / /   / / // / /  \/____ // / /_____/ /\ \    / / /\ \ \      / / /   / / /    
/_/\__/ / /    / / /___/ / // / /_____/ / // /_________/\ \ \  / / /  \ \ \    / / /___/ / /     
\ \/___/ /    / / /____\/ // / /______\/ // / /_       __\ \_\/ / /    \ \ \  / / /____\/ /      
 \_____\/     \/_________/ \/___________/ \_\___\     /____/_/\/_/      \_\_\ \/_________/       
                                                                                                  
"""
    border_top = '┌' + '─' * (INTERFACE_WIDTH - 2) + '┐'
    border_bottom = '└' + '─' * (INTERFACE_WIDTH - 2) + '┘'
    print(Fore.MAGENTA + border_top)
    for line in title_art.strip('\n').split('\n'):
        print(Fore.CYAN + '│' + line.center(INTERFACE_WIDTH - 2) + '│')
    print(Fore.MAGENTA + border_bottom)

def main_menu():
    print(Fore.MAGENTA + '\n' + '┌' + '─' * (INTERFACE_WIDTH - 2) + '┐')
    print_centered("MAIN MENU", Fore.YELLOW)
    print(Fore.MAGENTA + '├' + '─' * (INTERFACE_WIDTH - 2) + '┤\n')
    print_centered("1. Start Game", Fore.GREEN)
    print_centered("2. View Statistics", Fore.GREEN)
    print_centered("3. Reset Statistics", Fore.GREEN)
    print_centered("4. Exit", Fore.GREEN)
    print('\n' + Fore.MAGENTA + '└' + '─' * (INTERFACE_WIDTH - 2) + '┘')

def generate_math_problem():
    x = symbols('x')
    problem_types = ['equation', 'expand', 'mode', 'integration', 'derivative', 'median', 'standard_deviation']
    problem_type = random.choice(problem_types)

    if problem_type == 'equation':
        a = random.randint(1, 10)
        b = random.randint(1, 10)
        equation = Eq(a * x + b, 0)
        question = f"Solve for x: {a}*x + {b} = 0"
        answer = solve(equation, x)[0]
    elif problem_type == 'expand':
        n1 = random.randint(1, 5)
        n2 = random.randint(1, 5)
        expr = (x + n1) * (x - n2)
        question = f"Expand the expression: ({x} + {n1})*({x} - {n2})"
        answer = expand(expr)
    elif problem_type == 'mode':
        data = [random.randint(1, 10) for _ in range(10)]
        question = "Find the mode of the following numbers:\n" + ', '.join(map(str, data))
        modes = multimode(data)
        if len(modes) == 1:
            answer = modes[0]
        else:
            answer = mean(modes)
    elif problem_type == 'integration':
        a = random.randint(1, 5)
        b = random.randint(1, 5)
        expr = a * x**b
        question = f"Integrate the expression: {a}*x**{b}"
        answer = integrate(expr, x)
    elif problem_type == 'derivative':
        a = random.randint(1, 5)
        b = random.randint(1, 5)
        expr = a * x**b
        question = f"Find the derivative of the expression: {a}*x**{b}"
        answer = diff(expr, x)
    elif problem_type == 'median':
        data = [random.randint(1, 20) for _ in range(9)]
        question = "Find the median of the following numbers:\n" + ', '.join(map(str, data))
        answer = median(data)
    elif problem_type == 'standard_deviation':
        data = [random.randint(1, 20) for _ in range(10)]
        question = "Find the standard deviation of the following numbers:\n" + ', '.join(map(str, data))
        answer = round(stdev(data), 2)

    return question, answer

def assign_level(accuracy):
    if accuracy >= 90:
        return 'S'
    elif accuracy >= 80:
        return 'A'
    elif accuracy >= 70:
        return 'B'
    elif accuracy >= 60:
        return 'C'
    else:
        return 'D'

def save_statistics(player_stats):
    try:
        with open('player_stats.json', 'w') as f:
            json.dump(player_stats, f)
    except Exception as e:
        print(Fore.RED + f"Error saving statistics: {e}")

def load_statistics():
    if os.path.exists('player_stats.json'):
        try:
            with open('player_stats.json', 'r') as f:
                return json.load(f)
        except Exception as e:
            print(Fore.RED + f"Error loading statistics: {e}")
            return {'problems_attempted': 0, 'problems_correct': 0, 'total_time': 0.0}
    else:
        return {'problems_attempted': 0, 'problems_correct': 0, 'total_time': 0.0}

def reset_statistics():
    if os.path.exists('player_stats.json'):
        os.remove('player_stats.json')
        print(Fore.GREEN + "\nStatistics have been reset.")
    else:
        print(Fore.YELLOW + "\nNo statistics to reset.")

def start_game(player_stats):
    num_questions = 5
    correct_answers = 0
    total_time = 0
    clear_console()
    print_header()
    for i in range(num_questions):
        question, answer = generate_math_problem()
        print(Fore.MAGENTA + '\n' + '┌' + '─' * (INTERFACE_WIDTH - 2) + '┐')
        print_centered(f"Question {i+1}:", Fore.YELLOW)
        print(Fore.MAGENTA + '├' + '─' * (INTERFACE_WIDTH - 2) + '┤\n')
        print_centered(question, Fore.YELLOW)
        print('\n' + Fore.MAGENTA + '└' + '─' * (INTERFACE_WIDTH - 2) + '┘')
        start_time = time.time()
        user_input = input(Fore.CYAN + "Your answer: ").strip()
        end_time = time.time()
        try:
            if isinstance(answer, (int, float)):
                try:
                    user_answer = float(user_input)
                    is_correct = abs(user_answer - answer) < 1e-2
                except ValueError:
                    is_correct = False
            elif isinstance(answer, str):
                user_answer = user_input
                is_correct = user_answer == str(answer)
            else:
                try:
                    user_answer = simplify(user_input)
                    is_correct = user_answer == answer
                except SympifyError:
                    is_correct = False
            if is_correct:
                print(Fore.GREEN + "\n" + "Correct!".center(INTERFACE_WIDTH))
                correct_answers += 1
            else:
                print(Fore.RED + "\n" + f"Incorrect! The correct answer was {answer}.".center(INTERFACE_WIDTH))
        except Exception as e:
            print(Fore.RED + "\n" + f"An error occurred: {e}".center(INTERFACE_WIDTH))
        time_taken = end_time - start_time
        total_time += time_taken
        player_stats['problems_attempted'] += 1
        player_stats['problems_correct'] += int(is_correct)
        player_stats['total_time'] += time_taken
        time.sleep(2)
        clear_console()
        print_header()
    accuracy = (correct_answers / num_questions) * 100
    level = assign_level(accuracy)
    print(Fore.MAGENTA + '\n' + '┌' + '─' * (INTERFACE_WIDTH - 2) + '┐')
    print_centered("GAME OVER!", Fore.YELLOW)
    print(Fore.MAGENTA + '├' + '─' * (INTERFACE_WIDTH - 2) + '┤\n')
    print_centered(f"You answered {correct_answers} out of {num_questions} correctly.", Fore.GREEN)
    print_centered(f"Your accuracy: {accuracy:.2f}%", Fore.GREEN)
    print_centered(f"Your level: {level}", Fore.GREEN)
    print('\n' + Fore.MAGENTA + '└' + '─' * (INTERFACE_WIDTH - 2) + '┘')
    save_statistics(player_stats)
    input(Fore.CYAN + "\nPress Enter to return to the main menu...")
    clear_console()

def view_statistics(player_stats):
    clear_console()
    print_header()
    print(Fore.MAGENTA + '\n' + '┌' + '─' * (INTERFACE_WIDTH - 2) + '┐')
    print_centered("STATISTICS", Fore.YELLOW)
    print(Fore.MAGENTA + '├' + '─' * (INTERFACE_WIDTH - 2) + '┤\n')
    total_attempted = player_stats.get('problems_attempted', 0)
    total_correct = player_stats.get('problems_correct', 0)
    total_time = player_stats.get('total_time', 0)
    if total_attempted > 0:
        accuracy = (total_correct / total_attempted) * 100
        avg_time = total_time / total_attempted
        level = assign_level(accuracy)
        print_centered(f"Total problems attempted: {total_attempted}", Fore.GREEN)
        print_centered(f"Total correct answers: {total_correct}", Fore.GREEN)
        print_centered(f"Accuracy: {accuracy:.2f}%", Fore.GREEN)
        print_centered(f"Average time per problem: {avg_time:.2f} seconds", Fore.GREEN)
        print_centered(f"Current level: {level}", Fore.GREEN)
    else:
        print_centered("No statistics available. Play the game first.", Fore.YELLOW)
    print('\n' + Fore.MAGENTA + '└' + '─' * (INTERFACE_WIDTH - 2) + '┘')
    input(Fore.CYAN + "\nPress Enter to return to the main menu...")
    clear_console()

def main():
    player_stats = load_statistics()
    while True:
        print_header()
        main_menu()
        choice = input(Fore.CYAN + "Enter your choice: ").strip()
        if choice == '1':
            start_game(player_stats)
        elif choice == '2':
            view_statistics(player_stats)
        elif choice == '3':
            reset_statistics()
            player_stats = {'problems_attempted': 0, 'problems_correct': 0, 'total_time': 0.0}
            input(Fore.CYAN + "\nPress Enter to return to the main menu...")
            clear_console()
        elif choice == '4':
            print(Fore.GREEN + "\n" + "Thank you for playing!".center(INTERFACE_WIDTH))
            sys.exit()
        else:
            print(Fore.RED + "\n" + "Invalid choice. Please try again.".center(INTERFACE_WIDTH))
            time.sleep(2)
            clear_console()

if __name__ == "__main__":
    main()
