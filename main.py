import trivia as tr
from tqdm import tqdm

if __name__ == "__main__":
    qs, ns = tr.open_questions()

    # Infinite loop to ask questions until the program is closed
    while True:
        print('')
        tr.select_question(qs, ns)
        continue_asking = input("Do you want to answer another question? (Y/N): ")
        if continue_asking.lower() != 'y':
            print("Thanks for playing! Goodbye.")
            break