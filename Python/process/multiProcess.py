import multiprocessing
import time

def square_number(number):
    print(f"Square of {number}: {number ** 2}")
    time.sleep(2)  

if __name__ == "__main__":
    numbers = [1, 2, 3, 4, 5]
    processes = []

    for number in numbers:
        process = multiprocessing.Process(target=square_number, args=(number,))
        processes.append(process)
        process.start()

    for process in processes:
        process.join()

    print("All tasks completed.")
