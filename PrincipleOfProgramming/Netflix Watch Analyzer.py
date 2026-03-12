from functools import reduce

# -----------------------------
# Recursion: Find longest watch session
# -----------------------------
def recursive_max(lst, index=0, current=None):
    if not lst:
        return None
    if current is None:
        current = lst[0]
    if index == len(lst):
        return current
    if lst[index] > current:
        current = lst[index]
    return recursive_max(lst, index + 1, current)


def load_watch_time():
    times = []
    with open("watchtime.txt", "r") as file:
        for line in file:
            times.append(int(line.strip()))
    return times


def main():
    watch_times = load_watch_time()

    print("\nWatch Times:", watch_times)

    # FILTER: Only binge sessions (> 120 mins)
    binge = list(filter(lambda x: x > 120, watch_times))
    print("\nBinge Sessions (>120 mins):", binge)

    # MAP: Convert minutes to hours
    hours = list(map(lambda x: round(x / 60, 2), watch_times))
    print("\nWatch Time in Hours:", hours)

    # REDUCE: Total watch time
    total_time = reduce(lambda x, y: x + y, watch_times)
    print("\nTotal Watch Time (mins):", total_time)

    # RECURSION: Longest session
    longest = recursive_max(watch_times)
    print("\nLongest Watch Session (Recursion):", longest)


main()