from functools import reduce

# -----------------------------
# Recursion: Count total critical errors
# -----------------------------
def count_critical(errors, index=0):
    if index == len(errors):
        return 0
    if errors[index] >= 500:
        return 1 + count_critical(errors, index + 1)
    return count_critical(errors, index + 1)


# -----------------------------
# Load logs from file
# -----------------------------
def load_logs():
    logs = []
    try:
        with open("logs.txt", "r") as file:
            for line in file:
                logs.append(int(line.strip()))
    except FileNotFoundError:
        print("logs.txt not found!")
    return logs


# -----------------------------
# Main Program
# -----------------------------
def main():
    logs = load_logs()

    print("\nAll Logs:", logs)

    # FILTER: Find server errors
    suspicious = list(filter(lambda x: x >= 500, logs))
    print("\nSuspicious Attempts (>=500):", suspicious)

    # MAP: Convert to alert messages
    alerts = list(map(lambda x: f"⚠ ALERT: Server Error {x}", suspicious))
    print("\nAlert Messages:")
    for a in alerts:
        print(a)

    # REDUCE: Total error codes sum
    total_error_sum = reduce(lambda x, y: x + y, suspicious, 0)
    print("\nTotal Sum of Error Codes:", total_error_sum)

    # RECURSION: Count critical attacks
    critical_count = count_critical(logs)
    print("\nTotal Critical Attacks (Recursion):", critical_count)


main()