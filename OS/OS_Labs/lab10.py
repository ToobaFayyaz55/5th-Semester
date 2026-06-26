from collections import deque
def fifo_page_replacement(page_reference_string, num_frames):
    print("--- Starting FIFO Simulation ---")
    print(f"Page Reference String: {page_reference_string}")
    print(f"Number of Frames: {num_frames}\n")
    frames = [] # Represents the physical memory frames
    page_faults = 0
    # Use a deque as a queue to easily track the first-in page
    page_queue = deque()
    for page in page_reference_string:
    # Check if the page is already in a frame (a "hit")
        if page in frames:
            status = "Hit"
        # If not in a frame, a "fault" occurs
        else:
            page_faults += 1
            status = "Fault"
        # If there is space in memory, simply add the page
            if len(frames) < num_frames:
                frames.append(page)
                page_queue.append(page)
        # If memory is full, replace the oldest page
            else:
                page_to_replace = page_queue.popleft() # Get the oldest page
                frame_index = frames.index(page_to_replace)
                frames[frame_index] = page # Replace it with the new page
                page_queue.append(page) # Add new page to the queue
    # Print the state at each step for clarity
        print(f"Request: {page}, Frames: {list(frames)}, Status: {status}")
    print("\n--- FIFO Simulation Complete ---")
    print(f"Total Page Faults: {page_faults}")
    return page_faults

def lru_page_replacement(page_reference_string, num_frames):
    memory = []
    page_faults = 0

    print("\n--- LRU Page Replacement Simulation ---")
    print(f"Reference String: {page_reference_string}")
    print(f"Number of Frames: {num_frames}\n")

    for page in page_reference_string:
        if page in memory:
            memory.remove(page)
            memory.append(page)
            hit_or_fault = "Hit"
        else:
            page_faults += 1
            if len(memory) < num_frames:
                memory.append(page)
            else:
                memory.pop(0)
                memory.append(page)
            hit_or_fault = "Fault"
        
        print(f"Request: {page}, Frames: {memory}, Status: {hit_or_fault}")

    print(f"\nTotal Page Faults: {page_faults}")
    return page_faults


if __name__ == "__main__":
# Define a sample workload
    reference_string = [7, 0, 1, 2, 0, 3, 0, 4, 2, 3, 0, 3, 2, 1, 2, 0, 1, 7, 0, 1]
    frame_count = 3
    # Run the FIFO simulation
    fifo_faults = fifo_page_replacement(reference_string, frame_count)
    lru_faults =lru_page_replacement(reference_string, frame_count)
    
    print("\n===== Summary of Page Replacement Algorithms =====")
    print("Algorithm | Total Page Faults")
    print("-----------------------------")
    print(f"FIFO      | {fifo_faults}")
    print(f"LRU       | {lru_faults}")