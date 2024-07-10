import threading

class SecureCounter:
    """
    A thread-safe secure counter class.

    This class provides a secure counter with a maximum and minimum value.
    The counter value can be incremented or decremented, and it will
    raise a ValueError if the new value exceeds the allowed range.

    The class uses a threading.Lock to ensure thread-safety when
    modifying the counter value.
    """
    def __init__(self, max_value=100, min_value=0, initial_value=0):
        """
        Initialize the SecureCounter.

        Args:
            max_value (int): The maximum allowed value for the counter.
            min_value (int): The minimum allowed value for the counter.
            initial_value (int): The initial value of the counter.
        """
        self.max_value = max_value
        self.min_value = min_value
        self.value = initial_value
        self.lock = threading.Lock()

    def increment(self):
        """
        Increment the counter value by 1.

        Returns:
            int: The new value of the counter.

        Raises:
            ValueError: If the new value would exceed the maximum allowed value.
        """
        with self.lock:
            if self.value >= self.max_value:
                raise ValueError("Value exceeds maximum allowed value")
            self.value += 1
            return self.value

    def decrement(self):
        """
        Decrement the counter value by 1.

        Returns:
            int: The new value of the counter.

        Raises:
            ValueError: If the new value would be below the minimum allowed value.
        """
        with self.lock:
            if self.value <= self.min_value:
                raise ValueError("Value is below minimum allowed value")
            self.value -= 1
            return self.value

def worker(counter, name):
    """
    Simulate a worker thread that increments the counter 10 times.

    Args:
        counter (SecureCounter): The SecureCounter instance to be used.
        name (str): The name of the worker thread.
    """
    for _ in range(10):
        try:
            new_value = counter.increment()
            print(f"{name}: Incremented counter to {new_value}")
        except ValueError as e:
            print(f"{name}: {e}")

def main():
    """
    The main function that creates multiple worker threads and a SecureCounter.

    The worker threads will try to increment the counter 10 times each,
    demonstrating the thread-safe behavior of the SecureCounter class.
    """
    counter = SecureCounter(max_value=100, min_value=0, initial_value=50)

    threads = []
    for i in range(5):
        t = threading.Thread(target=worker, args=(counter, f"Thread-{i}"))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

if __name__ == "__main__":
    main()
