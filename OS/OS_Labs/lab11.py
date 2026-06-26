import copy
class MemoryBlock:
    def __init__(self, size, is_free=True, process_id=None):
        self.size = size
        self.is_free = is_free
        self.process_id = process_id

class Process:
    def __init__(self, pid, size):
        self.pid = pid
        self.size = size

def print_memory_layout(memory):
    print("\n--- Memory Layout ---")
    layout = "|"
    for block in memory:
        if block.is_free:
            layout += f" Free({block.size}K) |"
        else:
            layout += f" P{block.process_id}({block.size}K) |"
    print(layout)
    print("-" * len(layout))

def best_fit(initial_holes, processes):
    print("\n\n>>>--- Starting Best Fit Simulation ---<<<")
    memory = [MemoryBlock(size=h) for h in initial_holes]
    for process in processes:
        allocated = False
        best_idx = None
        best_size_diff = float('inf')
        for i, block in enumerate(memory):
            if block.is_free and block.size >= process.size:
                size_diff = block.size - process.size
                if size_diff < best_size_diff:
                    best_size_diff = size_diff
                    best_idx = i
        if best_idx is not None:
            block = memory[best_idx]
            print(f"Allocating Process P{process.pid} (size {process.size}K)" 
                  "to best-fit hole of size {block.size}K.")
            if block.size > process.size:
                remaining_size = block.size - process.size
                new_block = MemoryBlock(size=remaining_size)
                memory.insert(best_idx + 1, new_block)
            block.size = process.size
            block.is_free = False
            block.process_id = process.pid
            allocated = True
        if not allocated:
            print(f"Process P{process.pid} (size {process.size}K) could not be allocated.")

    print_memory_layout(memory)
    return memory

def worst_fit(initial_holes, processes):
    print("\n\n>>>--- Starting Worst Fit Simulation ---<<<")
    memory = [MemoryBlock(size=h) for h in initial_holes]
    for process in processes:
        allocated = False
        worst_idx = None
        worst_size_diff = -1  
        for i, block in enumerate(memory):
            if block.is_free and block.size >= process.size:
                size_diff = block.size - process.size
                if size_diff > worst_size_diff:
                    worst_size_diff = size_diff
                    worst_idx = i
        if worst_idx is not None:
            block = memory[worst_idx]
            print(f"Allocating Process P{process.pid} (size {process.size}K) "
                  " to worst-fit hole of size {block.size}K.")
            if block.size > process.size:
                remaining_size = block.size - process.size
                new_block = MemoryBlock(size=remaining_size)
                memory.insert(worst_idx + 1, new_block)
            block.size = process.size
            block.is_free = False
            block.process_id = process.pid
            allocated = True

        if not allocated:
            print(f"Process P{process.pid} (size {process.size}K) could not be allocated.")

    print_memory_layout(memory)
    return memory


def first_fit(initial_holes, processes):
    print("\n\n>>>--- Starting First Fit Simulation ---<<<")
    memory = [MemoryBlock(size=h) for h in initial_holes]

    for process in processes:
        allocated = False
        for i, block in enumerate(memory):
            if block.is_free and block.size >= process.size:
                print(f"Allocating Process P{process.pid} (size {process.size}K) to first available hole of size {block.size}K.")
                
                # Split the block if it is bigger than needed
                if block.size > process.size:
                    remaining_size = block.size - process.size
                    new_block = MemoryBlock(size=remaining_size)
                    memory.insert(i + 1, new_block)
                
                block.size = process.size
                block.is_free = False
                block.process_id = process.pid
                allocated = True
                break  # Move to next process

        if not allocated:
            print(f"Process P{process.pid} (size {process.size}K) could not be allocated.")

    print_memory_layout(memory)
    return memory

def analyze_algorithms_table(holes, processes):
    results = []

    # First Fit
    ff_memory = first_fit(holes, processes)
    total_free = sum(b.size for b in ff_memory if b.is_free)
    largest_free = max((b.size for b in ff_memory if b.is_free), default=0)
    results.append(("First Fit", total_free, largest_free))

    # Best Fit
    bf_memory = best_fit(holes, processes)
    total_free = sum(b.size for b in bf_memory if b.is_free)
    largest_free = max((b.size for b in bf_memory if b.is_free), default=0)
    results.append(("Best Fit", total_free, largest_free))

    # Worst Fit
    wf_memory = worst_fit(holes, processes)
    total_free = sum(b.size for b in wf_memory if b.is_free)
    largest_free = max((b.size for b in wf_memory if b.is_free), default=0)
    results.append(("Worst Fit", total_free, largest_free))

    # Print table
    print("\n========= Memory Allocation Comparison =========")
    print(f"{'Algorithm':<12} | {'Total Free (K)':<15} | {'Largest Free Block (K)':<20}")
    print("-" * 55)
    for alg, total, largest in results:
        print(f"{alg:<12} | {total:<15} | {largest:<20}")
    print("-" * 55)



if __name__ == "__main__":
# Define initial memory state and processes
    initial_memory_holes = [100, 500, 200, 300, 600] # Sizes in KB
    processes_to_allocate = [
    Process(1, 212), Process(2, 417), Process(3, 112), Process(4, 426)
    ]
    analyze_algorithms_table(initial_memory_holes,processes_to_allocate)
    # # Run the First Fit simulation
    # first_fit_memory = first_fit(copy.deepcopy(initial_memory_holes), processes_to_allocate)
    # best_fit_memory = best_fit(copy.deepcopy(initial_memory_holes), processes_to_allocate)
    # worst_fit_memory = worst_fit(copy.deepcopy(initial_memory_holes), processes_to_allocate)