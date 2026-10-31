import threading
import time

def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

def single_thread_experiment():
    targets = [35, 38, 40]
    start_time = []
    end_time = []

    for val in targets:
        start = time.time_ns()
        start_time.append(start)

        fibonacci(val)

        end = time.time_ns()
        end_time.append(end)

    t1 = min(start_time)
    t2 = max(end_time)
    return t2 - t1

def multithread_experiment():
    targets = [35, 38, 40]
    threads = []

    start_time = []
    end_time = []

    def worker(n):
        # Tracking and recording the start time
        start = time.time_ns()
        start_time.append(start)

        fibonacci(n)

        # Tracking and recording the end time
        end = time.time_ns()
        end_time.append(end)

    for val in targets:
        # Creating an object and assigning task
        t = threading.Thread(target=worker, args=(val,))
        threads.append(t)

    # Start
    for t in threads:
        t.start()

    # Waits for all to finish
    for t in threads:
        t.join()

    # Takes the longest end time - fastest start time
    t1 = min(start_time)
    t2 = max(end_time)

    return t2 - t1

def main():
    rounds = 10
    multithread_time = []
    single_thread_time = []

    print("Single-thread fibonacci experiments for 10 rounds")
    for r in range(1, rounds + 1):
        t_elapsed = single_thread_experiment()
        single_thread_time.append(t_elapsed)
        print(f"Round {r:2d}: T = {t_elapsed:,} ns")

    single_avg_time = sum(single_thread_time) / rounds
    print(f"Average Time over {rounds} rounds: {single_avg_time:,.2f} ns")

    print("\nMultithreaded fibonacci experiments for 10 rounds")
    for r in range(1, rounds + 1):
        t_elapsed = multithread_experiment()
        multithread_time.append(t_elapsed)
        print(f"Round {r:2d}: T = {t_elapsed:,} ns")

    multi_avg_time = sum(multithread_time) / rounds
    print(f"Average Time over {rounds} rounds: {multi_avg_time:,.2f} ns")

    print("Performance Comparison")
    if multi_avg_time < single_avg_time:
        speedup = single_avg_time / multi_avg_time
        time_saved_pct = ((single_avg_time - multi_avg_time) / single_avg_time) * 100
        print(f"Result: Multithreading was {speedup:.2f}x faster than single-threading.")
        print(f"Time Reduction: Saved approximately {time_saved_pct:.2f}% execution time.")
    else:
        slowdown = multi_avg_time / single_avg_time
        time_added_pct = ((multi_avg_time - single_avg_time) / single_avg_time) * 100
        print(f"Result: Multithreading was {slowdown:.2f}x slower than single-threading.")
        print(f"Performance Overhead: Added approximately {time_added_pct:.2f}% execution overhead due to GIL and thread context switching.")

if __name__ == "__main__":
    main()