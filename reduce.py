import sys

def reduce_function():
    current_word = None
    current_count = 0

    for line in sys.stdin:
        word, count = line.strip().split('\t', 1)
        count = int(count)

        if current_word == word:
            current_count += count
        else:
            if current_word:
                print(f"{current_word}\t{current_count}")
            current_word = word
            current_count = count

    if current_word == word:
        print(f"{current_word}\t{current_count}")

if __name__ == "__main__":
    reduce_function()