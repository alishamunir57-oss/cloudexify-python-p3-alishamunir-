import random
import time
import os
from datetime import datetime
from colorama import init, Fore, Style

# needed so colors reset automatically after every print, otherwise the
# whole terminal stays red/green after the first colored line
init(autoreset=True)

LEADERBOARD_FILE = "leaderboard.txt"
QUESTIONS_PER_ROUND = 10
TIME_LIMIT_SECONDS = 25
PRACTICE_TIME_LIMIT = 999   # basically unlimited, used for practice mode


# question format: (topic, difficulty, question text, list of choices, correct choice)
# keeping the answer as plain text instead of "A"/"B"/"C" so we can shuffle
# the choices every time without messing up the answer check
QUESTION_BANK = [
    # ---- Basics ----
    ("Basics", "Easy", "What does print(5 // 2) output?",
     ["2.5", "2", "3", "2.0"], "2"),
    ("Basics", "Easy", "What does bool('') evaluate to?",
     ["True", "False", "Error", "None"], "False"),
    ("Basics", "Easy", "What is printed by: print('5' + '5')?",
     ["10", "'55'", "55", "Error"], "55"),
    ("Basics", "Easy", "What type does 7 / 2 return in Python 3?",
     ["int", "float", "str", "complex"], "float"),
    ("Basics", "Easy", "Which of these is a valid variable name?",
     ["2total", "total_2", "total-2", "total 2"], "total_2"),
    ("Basics", "Medium", "What is the value of x after: x = 3; x += 2; x *= 2?",
     ["10", "8", "5", "7"], "10"),
    ("Basics", "Medium", "Which line correctly swaps a and b in one line?",
     ["a, b = b, a", "swap(a, b)", "a = b, b = a", "a <-> b"], "a, b = b, a"),
    ("Basics", "Medium", "What does print(10 == 10.0) output?",
     ["False", "True", "Error", "None"], "True"),
    ("Basics", "Medium", "What does print(2 ** 3) output?",
     ["6", "8", "9", "23"], "8"),
    ("Basics", "Hard", "What's wrong with: if x = 5:",
     ["Nothing, it's valid", "Should use == not =", "Missing colon", "x isn't defined"], "Should use == not ="),
    ("Basics", "Hard", "What does print(0.1 + 0.2 == 0.3) output?",
     ["True", "False", "Error", "None"], "False"),
    ("Basics", "Medium", "What is the result of print(bool(0), bool(1), bool(-1))?",
     ["False True True", "True True True", "False False True", "True False True"], "False True True"),

    # ---- Loops ----
    ("Loops", "Easy", "How many times does 'hi' print? for i in range(2, 8, 2): print('hi')",
     ["2", "3", "4", "6"], "3"),
    ("Loops", "Easy", "What does continue do inside a for loop?",
     ["Ends the loop completely", "Skips to the next iteration", "Restarts the whole program", "Pauses execution"], "Skips to the next iteration"),
    ("Loops", "Easy", "Which loop runs while a condition is True?",
     ["for", "while", "if", "do"], "while"),
    ("Loops", "Medium", "i=0; while i<3: print(i); i+=1  -->  what prints?",
     ["0 1 2", "1 2 3", "0 1 2 3", "Infinite loop"], "0 1 2"),
    ("Loops", "Medium", "Which condition never becomes False, causing an infinite loop?",
     ["while i < 10:", "while i != 10:", "while True:", "while i in range(10):"], "while True:"),
    ("Loops", "Medium", "for i in range(5): (if i==3: break) else print(i)  -->  what prints before the break?",
     ["0 1 2", "0 1 2 3", "0 1 2 3 4", "3"], "0 1 2"),
    ("Loops", "Hard", "What does else attached to a for loop run?",
     ["Never", "Only if the loop wasn't broken out of", "Only if it was broken out of", "Every iteration"], "Only if the loop wasn't broken out of"),
    ("Loops", "Hard", "What's the bug in: for i in range(5)   print(i)   (colon missing on purpose)",
     ["range should be len()", "Missing colon after range(5)", "print needs a semicolon", "i is undefined"], "Missing colon after range(5)"),
    ("Loops", "Medium", "What does list(range(1, 10, 3)) return?",
     ["[1, 4, 7]", "[1, 2, 3]", "[1, 4, 7, 10]", "[3, 6, 9]"], "[1, 4, 7]"),
    ("Loops", "Easy", "What does the keyword pass do inside a loop?",
     ["Skips to next iteration", "Does nothing, just a placeholder", "Ends the loop", "Raises an error"], "Does nothing, just a placeholder"),

    # ---- Strings ----
    ("Strings", "Easy", "What does 'Python Rocks'.lower().replace(' ', '_') return?",
     ["python_rocks", "Python_Rocks", "python rocks", "PYTHON_ROCKS"], "python_rocks"),
    ("Strings", "Easy", "What does 'abcdef'[::-1] produce?",
     ["abcdef", "fedcba", "Error", "''"], "fedcba"),
    ("Strings", "Easy", "What's the result of [1, 2] + [3, 4]?",
     ["[1, 2, 3, 4]", "[4, 6]", "Error", "[[1,2],[3,4]]"], "[1, 2, 3, 4]"),
    ("Strings", "Easy", "What does len('hello') return?",
     ["4", "5", "6", "Error"], "5"),
    ("Strings", "Medium", "Given nums = [4, 1, 7, 2], what does sorted(nums) return?",
     ["[4, 1, 7, 2]", "[1, 2, 4, 7]", "[7, 4, 2, 1]", "None"], "[1, 2, 4, 7]"),
    ("Strings", "Medium", "Which correctly checks if 'cat' is inside a list called pets?",
     ["'cat' in pets", "pets.has('cat')", "pets == 'cat'", "'cat'.in(pets)"], "'cat' in pets"),
    ("Strings", "Medium", "What does ', '.join(['a', 'b', 'c']) return?",
     ["a, b, c", "['a','b','c']", "abc", "Error"], "a, b, c"),
    ("Strings", "Hard", "What does [x*2 for x in range(3)] evaluate to?",
     ["[0, 2, 4]", "[0, 1, 2]", "[2, 4, 6]", "Error"], "[0, 2, 4]"),
    ("Strings", "Hard", "What does 'Hello World'.split()[-1] return?",
     ["Hello", "World", "d", "Error"], "World"),
    ("Strings", "Medium", "What does 'Python'.startswith('Py') return?",
     ["True", "False", "Error", "None"], "True"),

    # ---- Files ----
    ("Files", "Easy", "Which mode opens a file for reading only?",
     ["'w'", "'a'", "'r'", "'x'"], "'r'"),
    ("Files", "Easy", "What happens if you open an existing file in 'w' mode?",
     ["Appends new content", "Its old content is erased", "It raises an error", "Nothing changes"], "Its old content is erased"),
    ("Files", "Medium", "You want to read a file without worrying about closing it manually. Best practice?",
     ["open() then close()", "with open(...) as f:", "os.read()", "file.auto_close()"], "with open(...) as f:"),
    ("Files", "Medium", "Opening a file in 'a' mode that doesn't exist yet will...",
     ["Raise FileNotFoundError", "Create the file", "Return None", "Crash the program"], "Create the file"),
    ("Files", "Medium", "Given scores = {'Ali': 90, 'Sara': 85}, how do you safely get 'Ahmed' with a default of 0?",
     ["scores['Ahmed']", "scores.get('Ahmed', 0)", "scores.find('Ahmed')", "scores.default('Ahmed')"], "scores.get('Ahmed', 0)"),
    ("Files", "Hard", "Which loop iterates over both keys and values of a dict called d?",
     ["for k in d.values():", "for k, v in d.items():", "for k in d.pairs():", "for k, v in d:"], "for k, v in d.items():"),
    ("Files", "Hard", "What does int(f.read()) do if the file just contains '42'?",
     ["Returns '42' as a string", "Returns 42 as an integer", "Raises an error", "Returns 42.0"], "Returns 42 as an integer"),
    ("Files", "Easy", "Which mode adds text to the end of an existing file?",
     ["'r'", "'w'", "'a'", "'r+'"], "'a'"),
    ("Files", "Medium", "What data structure stores data as key-value pairs?",
     ["list", "tuple", "dict", "set"], "dict"),

    # ---- Functions ----
    ("Functions", "Easy", "What does a function return if it has no return statement?",
     ["0", "None", "Empty string", "Error"], "None"),
    ("Functions", "Easy", "Which correctly defines a function with a default argument?",
     ["def f(x, y=2):", "def f(x, y:=2):", "def f(x, default y=2):", "def f(x, y=2)"], "def f(x, y=2):"),
    ("Functions", "Easy", "Which keyword is used to define a function in Python?",
     ["function", "define", "def", "func"], "def"),
    ("Functions", "Medium", "What does this return? def add(a, b=5): return a + b  -->  add(3)",
     ["3", "5", "8", "Error"], "8"),
    ("Functions", "Medium", "Why use a function instead of copy-pasting the same code block 3 times?",
     ["Functions run faster always", "It's required by Python", "Easier to maintain and reuse", "It uses less memory always"], "Easier to maintain and reuse"),
    ("Functions", "Hard", "What does *args let a function do?",
     ["Accept any number of positional arguments", "Force exactly one argument", "Return multiple values only", "Import other functions"], "Accept any number of positional arguments"),
    ("Functions", "Hard", "What will this print? def f():\n    x = 5\nf()\nprint(x)",
     ["5", "0", "NameError", "None"], "NameError"),
    ("Functions", "Medium", "What is the term for a variable defined inside a function?",
     ["Global variable", "Local variable", "Constant", "Static variable"], "Local variable"),
]

TOPICS = ["Basics", "Loops", "Strings", "Files", "Functions"]
DIFFICULTIES = ["Easy", "Medium", "Hard", "ALL"]


class QuizEngine:
    # keeps track of everything happening during one play session -
    # the question bank, and a full history of what was asked/answered
    # so we can review + report on it later

    def __init__(self, bank, questions_per_round=QUESTIONS_PER_ROUND, time_limit=TIME_LIMIT_SECONDS):
        self.bank = bank
        self.questions_per_round = questions_per_round
        self.time_limit = time_limit
        self.history = []

    def build_round(self, topic, difficulty):
        pool = self.bank

        if topic != "ALL":
            pool = [q for q in pool if q[0] == topic]
        if difficulty != "ALL":
            pool = [q for q in pool if q[1] == difficulty]

        # random.sample picks a random subset without repeats, so every
        # round looks different even if you pick the same topic again
        size = min(self.questions_per_round, len(pool))
        return random.sample(pool, size)

    def ask(self, index, total, question):
        topic, difficulty, text, choices, correct = question

        options = choices[:]
        random.shuffle(options)
        labels = ["A", "B", "C", "D"][:len(options)]
        label_map = dict(zip(labels, options))

        print_divider()
        print(f"[{index}/{total}] ({difficulty}) {text}")
        for label in labels:
            print(f"   {label}) {label_map[label]}")

        start_time = time.time()
        while True:
            answer = input(f"Answer ({'/'.join(labels)}) - {self.time_limit}s limit: ").strip().upper()
            time_used = time.time() - start_time

            if time_used > self.time_limit:
                print(Fore.RED + f"Time's up! Correct answer: {correct}")
                chosen_text = "(no answer, ran out of time)"
                correct_answer_given = False
                break

            if answer in labels:
                chosen_text = label_map[answer]
                correct_answer_given = (chosen_text == correct)
                break

            print("That's not one of the options, try again.")

        # save this attempt so we can build the review + topic report later
        self.history.append({
            "topic": topic,
            "question": text,
            "picked": chosen_text,
            "correct": correct,
            "was_correct": correct_answer_given,
        })

        if correct_answer_given:
            print(Fore.GREEN + "Correct!")
        else:
            print(Fore.RED + f"Wrong. Correct answer: {correct}")

        return correct_answer_given


def print_divider():
    print(Fore.CYAN + "-" * 46)


def calc_grade(percent):
    # simple cutoffs, nothing fancy
    if percent >= 90:
        return "A"
    if percent >= 75:
        return "B"
    if percent >= 60:
        return "C"
    if percent >= 40:
        return "D"
    return "F"


def ask_player_name():
    # keeps asking until we get something that actually looks like a name
    while True:
        name = input("Enter your name: ").strip()

        if name == "":
            print("Name can't be blank.")
        elif not name.replace(" ", "").isalpha():
            print("Please use letters only (no numbers/symbols).")
        elif len(name) > 20:
            print("That's a bit long, keep it under 20 characters.")
        else:
            return name.title()


def choose_from_menu(prompt, options):
    # generic little menu picker, used for topic / difficulty / mode
    print(prompt)
    for i, opt in enumerate(options, 1):
        print(f"  {i}. {opt}")

    while True:
        pick = input("\nYour choice: ").strip()
        if pick.isdigit() and 1 <= int(pick) <= len(options):
            return options[int(pick) - 1]
        print("Please pick a valid number from the list above.")


def load_leaderboard():
    # returns a dict of {player_name: best_percentage}
    if not os.path.exists(LEADERBOARD_FILE):
        return {}

    scores = {}
    with open(LEADERBOARD_FILE, "r") as f:
        for line in f:
            bits = line.strip().split(",")
            if len(bits) == 2:
                try:
                    scores[bits[0]] = float(bits[1])
                except ValueError:
                    pass  # skip corrupted lines instead of crashing
    return scores


def save_score(name, percent):
    """
    Saves the player's score if it's a new personal best, and keeps only
    the top 5 overall. Returns (top_five, is_new_high_score, previous_best)
    so the caller doesn't need to re-check the leaderboard file itself -
    this used to be checked twice (once here, once in play_round) which
    meant two separate places could disagree about what "best" means.
    Now there's just one place that decides that.
    """
    scores = load_leaderboard()
    previous_best = scores.get(name)
    is_new_high = previous_best is None or percent > previous_best

    if is_new_high:
        scores[name] = percent

    top_five = sorted(scores.items(), key=lambda pair: pair[1], reverse=True)[:5]
    with open(LEADERBOARD_FILE, "w") as f:
        for player, best in top_five:
            f.write(f"{player},{best}\n")

    return top_five, is_new_high, previous_best


def print_leaderboard(entries):
    print_divider()
    print(Fore.YELLOW + "TOP 5 LEADERBOARD (personal best per player)")
    print_divider()
    if not entries:
        print("Nobody's played yet - be the first!")
    for rank, (name, percent) in enumerate(entries, 1):
        print(f"  {rank}. {name:<15}{percent}%")
    print_divider()


def print_review(history):
    missed = [h for h in history if not h["was_correct"]]

    print_divider()
    if not missed:
        print(Fore.GREEN + "Clean round, nothing to review!")
        print_divider()
        return

    print(f"REVIEW - here's what you got wrong ({len(missed)} question(s))")
    print_divider()
    for i, h in enumerate(missed, 1):
        print(f"{i}. {h['question']}")
        print(f"   You answered : {h['picked']}")
        print(f"   Correct was  : {h['correct']}\n")
    print_divider()


def print_topic_breakdown(history):
    # groups the round's history by topic so the player can see where
    # they're actually weak instead of just one overall percentage
    by_topic = {}
    for h in history:
        stats = by_topic.setdefault(h["topic"], {"right": 0, "total": 0})
        stats["total"] += 1
        if h["was_correct"]:
            stats["right"] += 1

    print("TOPIC BREAKDOWN")
    print_divider()

    weakest_topic = None
    weakest_pct = 101   # start above 100 so first topic always "wins"

    for topic, stats in by_topic.items():
        pct = round(stats["right"] / stats["total"] * 100)
        print(f"  {topic:<12}: {stats['right']}/{stats['total']} ({pct}%)")
        if pct < weakest_pct:
            weakest_pct = pct
            weakest_topic = topic

    # only worth pointing out a "weak" topic if the player actually missed
    # something - otherwise every topic tied at 100% and calling one of
    # them "weakest" is just misleading
    if weakest_topic and weakest_pct < 100:
        print(f"\nTip: '{weakest_topic}' was your weakest area this round, worth revisiting.")
    print_divider()


def get_badges(history, seconds_taken):
    # small fun extra, not required for grading but makes the game feel
    # more like an actual "game" instead of a plain quiz
    badges = []
    total = len(history)
    right = sum(1 for h in history if h["was_correct"])

    if total > 0 and right == total:
        badges.append("Perfect Round")

    if total > 0 and (seconds_taken / total) < 10:
        badges.append("Speed Runner")

    if history and any(not h["was_correct"] for h in history[:-1]) and history[-1]["was_correct"]:
        badges.append("Comeback Kid")

    return badges


def save_results_file(name, history, correct, total, percent, grade):
    # dumps a little report to disk, mostly so there's proof of each
    # attempt and to double check the scoring logic while testing
    filename = f"results_{datetime.now().strftime('%Y-%m-%d_%H%M%S')}.txt"

    with open(filename, "w") as f:
        f.write(f"Player: {name}\n")
        f.write(f"Score: {correct}/{total}\n")
        f.write(f"Percentage: {percent}%\n")
        f.write(f"Grade: {grade}\n\n")
        f.write("Question by question:\n")
        for i, h in enumerate(history, 1):
            status = "correct" if h["was_correct"] else "wrong"
            f.write(f"{i}. [{status}] {h['question']}\n")
            f.write(f"   your answer: {h['picked']} | correct answer: {h['correct']}\n")

    print(f"(saved a copy of this round to {filename})")


def play_round(engine):
    print("=" * 46)
    print(Fore.MAGENTA + "          PYTHON QUIZ GAME")
    print("=" * 46)

    name = ask_player_name()
    topic = choose_from_menu("\nPick a topic (or ALL for mixed):", TOPICS + ["ALL"])
    difficulty = choose_from_menu("\nPick a difficulty (or ALL for mixed):", DIFFICULTIES)
    mode = choose_from_menu("\nPick a mode:", ["Timed Challenge", "Practice (no timer)"])

    # reset per-round state on the engine since it's reused across replays
    engine.history = []
    engine.time_limit = PRACTICE_TIME_LIMIT if mode.startswith("Practice") else TIME_LIMIT_SECONDS

    questions = engine.build_round(topic, difficulty)
    if not questions:
        print("Couldn't find any questions for that combo, try ALL/ALL instead.")
        return

    correct_count = 0
    start_time = time.time()
    for i, q in enumerate(questions, 1):
        if engine.ask(i, len(questions), q):
            correct_count += 1
    time_taken = time.time() - start_time

    percent = round((correct_count / len(questions)) * 100, 1)
    grade = calc_grade(percent)

    print_divider()
    print("RESULTS")
    print_divider()
    print(f"Player     : {name}")
    print(f"Score      : {correct_count}/{len(questions)}")
    print(f"Percentage : {percent}%")
    print(f"Grade      : {grade}")
    print(f"Time taken : {time_taken:.1f}s")
    print_divider()

    badges = get_badges(engine.history, time_taken)
    if badges:
        print(Fore.YELLOW + "Badges earned: " + ", ".join(badges))
        print_divider()

    print_review(engine.history)
    print_topic_breakdown(engine.history)

    # single call now handles both saving AND telling us if it was a new
    # high score - no more checking the leaderboard file twice
    top_five, is_new_high, previous_best = save_score(name, percent)

    if is_new_high:
        print(Fore.YELLOW + "*** NEW HIGH SCORE! ***")
        if previous_best is not None:
            print(f"Previous best: {previous_best}%  ->  New best: {percent}%")
        print_divider()

    print_leaderboard(top_five)
    save_results_file(name, engine.history, correct_count, len(questions), percent, grade)


def main():
    engine = QuizEngine(QUESTION_BANK)
    while True:
        play_round(engine)
        again = input("\nPlay again? (y/n): ").strip().lower()
        if again != "y":
            print("Thanks for playing, see you next time!")
            break


if __name__ == "__main__":
    main()