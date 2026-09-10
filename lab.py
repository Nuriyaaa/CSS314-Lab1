import time
import threading
from concurrent.futures import ProcessPoolExecutor

# --- TASK 2: COMPUTE-BOUND BENCHMARK (Matrix Multiplication) ---
def compute_workload(size=200):
    A = [[1.0] * size for _ in range(size)]
    B = [[2.0] * size for _ in range(size)]
    C = [[0.0] * size for _ in range(size)]
    for i in range(size):
        for j in range(size):
            for k in range(size):
                C[i][j] += A[i][k] * B[k][j]
    return C

def run_task2():
    print("=== TASK 2: MULTI-PROCESS BENCHMARK ===")
    thread_counts = [1, 2, 4, 8, 16, 32]
    workload_count = 32  # Общий объем работы
    
    for n in thread_counts:
        times = []
        for run in range(3):
            start = time.perf_counter()
            with ProcessPoolExecutor(max_workers=n) as executor:
                list(executor.map(compute_workload, [200] * workload_count))
            elapsed = time.perf_counter() - start
            times.append(elapsed)
        avg = sum(times) / len(times)
        print(f"N={n:2d} | Run 1: {times[0]:.2f}s | Run 2: {times[1]:.2f}s | Run 3: {times[2]:.2f}s | Avg: {avg:.2f}s")

# --- TASK 3: RACE CONDITION & LOCK BENCHMARK ---
counter = 0

def unsafe_worker():
    global counter
    for _ in range(1_000_000):
        counter += 1

def safe_worker(lock):
    global counter
    for _ in range(1_000_000):
        with lock:
            counter += 1

def run_task3():
    global counter
    print("\n=== TASK 3: UNSYNCHRONIZED COUNTER (10 RUNS) ===")
    for r in range(1, 11):
        counter = 0
        threads = [threading.Thread(target=unsafe_worker) for _ in range(10)]
        for t in threads: t.start()
        for t in threads: t.join()
        error = 10_000_000 - counter
        print(f"Run #{r:2d} | Measured: {counter:10d} | Error: {error:10d}")

    print("\n=== TASK 3.2: SYNCHRONIZATION PENALTY ===")
    # Unlocked
    counter = 0
    start = time.perf_counter()
    threads = [threading.Thread(target=unsafe_worker) for _ in range(10)]
    for t in threads: t.start()
    for t in threads: t.join()
    unlocked_time = (time.perf_counter() - start) * 1000

    # Locked
    counter = 0
    lock = threading.Lock()
    start = time.perf_counter()
    threads = [threading.Thread(target=safe_worker, args=(lock,)) for _ in range(10)]
    for t in threads: t.start()
    for t in threads: t.join()
    locked_time = (time.perf_counter() - start) * 1000

    print(f"Unlocked = {unlocked_time:.2f} ms vs. Locked = {locked_time:.2f} ms")

if __name__ == "__main__":
    run_task2()
    run_task3()