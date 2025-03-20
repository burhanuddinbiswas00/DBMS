import threading
import time
from account import Account
from deadlock_detector import DeadlockDetector

def transfer(from_account, to_account, amount, detector):
    print(f"Attempting to transfer ${amount} from Account {from_account.id} to Account {to_account.id}")
    
    # Acquire locks in a specific order to avoid deadlocks
    if from_account.id < to_account.id:
        first, second = from_account, to_account
    else:
        first, second = to_account, from_account

    with first.lock:
        print(f"Lock acquired on Account {first.id}")
        time.sleep(1)  # Simulate delay
        with second.lock:
            print(f"Lock acquired on Account {second.id}")
            if from_account.balance >= amount:
                from_account.balance -= amount
                to_account.balance += amount
                print(f"Transferred ${amount} from Account {from_account.id} to Account {to_account.id}")
            else:
                print(f"Insufficient balance in Account {from_account.id}")

def simulate_deadlock():
    # Create accounts
    account1 = Account(1, 1000)
    account2 = Account(2, 1000)

    # Create a deadlock detector
    detector = DeadlockDetector()

    # Simulate transactions
    def transaction1():
        detector.add_edge(1, 2)  # Transaction 1 is waiting for Transaction 2
        transfer(account1, account2, 100, detector)

    def transaction2():
        detector.add_edge(2, 1)  # Transaction 2 is waiting for Transaction 1
        transfer(account2, account1, 100, detector)

    # Start threads
    t1 = threading.Thread(target=transaction1)
    t2 = threading.Thread(target=transaction2)
    t1.start()
    t2.start()

    # Wait for threads to finish
    t1.join()
    t2.join()

    # Check for deadlock
    if detector.detect_cycle():
        print("Deadlock detected!")
    else:
        print("No deadlock detected.")

if __name__ == "__main__":
