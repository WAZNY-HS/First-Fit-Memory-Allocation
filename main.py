import tkinter as tk
from tkinter import messagebox

# First Fit Memory Allocation Simulation
# This program simulates the First Fit algorithm for dynamic memory allocation.

# Function to allocate memory using the First Fit algorithm
def first_fit(blocks, processes):
    allocation = [-1] * len(processes)  # Initialize allocation array with -1 (indicating unallocated)
    original_blocks = blocks[:]  # Keep a copy of the original block sizes for fragmentation calculation

    # Iterate through each process to allocate memory
    for i, process in enumerate(processes):
        for j, block in enumerate(blocks):
            # Check if the block can fit the process
            if process <= block:
                allocation[i] = j  # Allocate block j to process i
                blocks[j] -= process  # Reduce the block size by the allocated process size
                break

    fragments = [original_blocks[i] - blocks[i] for i in range(len(blocks))]  # Calculate fragments

    return allocation, fragments

# Function to handle the UI logic
def allocate_memory():
    try:
        # Get input from user
        blocks = list(map(int, block_entry.get().split(',')))
        processes = list(map(int, process_entry.get().split(',')))

        # Perform allocation
        allocation, fragments = first_fit(blocks, processes)

        # Prepare results for display
        result_text = "Process No.\tProcess Size\tBlock No.\n"
        for i, (process, block) in enumerate(zip(processes, allocation)):
            if block != -1:
                result_text += f"{i + 1}\t\t{process}\t\t{block + 1}\n"
            else:
                result_text += f"{i + 1}\t\t{process}\t\tNot Allocated\n"

        # Display results
        result_label.config(text=result_text)

        # Update memory status
        memory_status_text = "Memory Status:\n\n"
        memory_status_text += "Categories\t\tDetails\n"
        memory_status_text += "-------------------------\n"

        # Free Blocks
        free_blocks = ", ".join([f"Block {idx + 1}: {block} KB" for idx, block in enumerate(blocks)])
        memory_status_text += f"Free Blocks\t\t{free_blocks}\n"

        # Fragments
        fragments_detail = ", ".join([f"Block {idx + 1}: {fragment} KB" for idx, fragment in enumerate(fragments)])
        memory_status_text += f"Fragments\t\t{fragments_detail}\n"

        # Allocations
        allocations_detail = "\n".join([
            f"Process {idx + 1} allocated to Block {block + 1}" if block != -1 else f"Process {idx + 1} not allocated"
            for idx, block in enumerate(allocation)
        ])
        memory_status_text += f"Allocations\t\t{allocations_detail}\n"

        memory_status_label.config(text=memory_status_text)

    except ValueError:
        messagebox.showerror("Input Error", "Please enter valid integers separated by commas.")

# Function to clear all inputs and results
def clear_all():
    block_entry.delete(0, tk.END)
    process_entry.delete(0, tk.END)
    result_label.config(text="")
    memory_status_label.config(text="")

# Set up the UI
root = tk.Tk()
root.title("First Fit Memory Allocation")
root.configure(bg="#f0f8ff")  # Set background color

# Styling options
label_font = ("Arial", 14, "bold")
entry_font = ("Arial", 12)
button_font = ("Arial", 14, "bold")
result_font = ("Courier", 12)

# Input for blocks
block_label = tk.Label(root, text="Enter Block Sizes (comma-separated):", bg="#f0f8ff", font=label_font)
block_label.pack(pady=5)
block_entry = tk.Entry(root, width=50, font=entry_font)
block_entry.pack(pady=5)

# Input for processes
process_label = tk.Label(root, text="Enter Process Sizes (comma-separated):", bg="#f0f8ff", font=label_font)
process_label.pack(pady=5)
process_entry = tk.Entry(root, width=50, font=entry_font)
process_entry.pack(pady=5)

# Button to perform allocation
allocate_button = tk.Button(root, text="Allocate Memory", command=allocate_memory, font=button_font, bg="#4caf50", fg="white")
allocate_button.pack(pady=10)

# Button to clear all results
clear_button = tk.Button(root, text="Clear All Results", command=clear_all, font=button_font, bg="#f44336", fg="white")
clear_button.pack(pady=10)

# Label to display results
result_label = tk.Label(root, text="", justify="left", anchor="w", bg="#f0f8ff", font=result_font)
result_label.pack(pady=10)

# Label to display memory status after allocation
memory_status_label = tk.Label(root, text="", justify="left", anchor="w", bg="#f0f8ff", font=result_font)
memory_status_label.pack(pady=10)

# Run the application
root.mainloop()
