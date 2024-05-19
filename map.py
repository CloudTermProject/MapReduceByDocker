import sys

def map_function():
    for line in sys.stdin:
        words = line.strip().split()
        for word in words:
            print(f"{word}\t1")

if __name__ == "__main__":
    map_function()