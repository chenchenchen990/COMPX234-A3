import subprocess
import time

def run_all_clients():
    host = "localhost"
    port = 51234
    base_path = r"F:\个人作业\系统与网络\Testproject\test-workload-1\test-workload"

    for i in range(1, 11):
        file_path = f"{base_path}\\client_{i}.txt"
        print(f"\n--- Running client {i} ---")
        subprocess.run(["python", "client.py", host, str(port), file_path])