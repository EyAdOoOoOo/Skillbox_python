import os

def process_count(username: str) -> int:
    """
    Returns the number of processes currently running for the specified user.
    """
    # Run shell command to list processes for the given user and count the lines
    process_data = os.popen(f'ps --user {username} | wc -l').read()
    
    # Subtract 1 to remove the header line from the count and return the result as an integer
    return int(process_data) - 1

def total_memory_usage(root_pid: int) -> float:
    """
    Returns the total memory usage (in KB) of a process and its child processes.
    """
    # Get the memory usage of the root process (column 8 from `ps -v`)
    process_memory = float(os.popen(f'ps -v {root_pid}').readlines()[1].split()[8])

    # Get memory usage of all child processes (PPID refers to the root process ID)
    child_processes_data = os.popen(f'ps -v --ppid {root_pid}').readlines()[1:]

    # Extract memory usage for child processes from column 8 and sum the values
    child_memory = sum(float(proc_info.split()[8]) for proc_info in child_processes_data)

    # Return the total memory usage (root process + child processes)
    return process_memory + child_memory

# Example usage
print(f'Root process count: {process_count("root")}')
print(f'Total memory usage of process_pid 40970 (Firefox): {total_memory_usage(40970)}')
