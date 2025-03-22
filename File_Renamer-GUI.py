import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from pathlib import Path

class FileRenamerApp:
    def __init__(self, root):
        # Initialize the main application window
        self.root = root
        self.root.title("File Renamer")  # Set the window title

        # Set an initial window size
        self.root.geometry("500x300")

        # Set a minimum window size to prevent hiding essential elements
        self.root.minsize(500, 300)  # Width: 500, Height: 300

        # Configure grid weights for resizing
        self.root.columnconfigure(1, weight=1)  # Make the second column expandable
        self.root.rowconfigure(2, weight=1)  # Make the third row expandable

        # Folder Path Section
        self.folder_path_label = tk.Label(root, text="Folder Path:")  # Label for folder path
        self.folder_path_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")  # Place label in the grid
        self.folder_path_entry = tk.Entry(root, width=50)  # Entry widget for folder path
        self.folder_path_entry.grid(row=0, column=1, padx=10, pady=10, sticky="ew")  # Place entry in the grid
        self.browse_button = tk.Button(root, text="Browse", command=self.browse_folder)  # Browse button
        self.browse_button.grid(row=0, column=2, padx=10, pady=10, sticky="e")  # Place button in the grid

        # Number of Changes Section
        self.num_changes_label = tk.Label(root, text="Number of Changes:")  # Label for number of changes
        self.num_changes_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")  # Place label in the grid
        self.num_changes_entry = tk.Entry(root, width=10)  # Entry widget for number of changes
        self.num_changes_entry.grid(row=1, column=1, padx=10, pady=10, sticky="w")  # Place entry in the grid
        self.num_changes_button = tk.Button(root, text="Create Fields", command=self.create_change_entries)  # Button to create fields
        self.num_changes_button.grid(row=1, column=2, padx=10, pady=10, sticky="e")  # Place button in the grid

        # Create a canvas and scrollbar for the changes frame
        self.canvas = tk.Canvas(root, highlightthickness=0)  # Canvas widget to hold the scrollable frame (disable focus highlight)
        self.canvas.grid(row=2, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")  # Place canvas in the grid

        # Add a vertical scrollbar
        self.scrollbar = ttk.Scrollbar(root, orient="vertical", command=self.canvas.yview)  # Scrollbar widget
        self.scrollbar.grid(row=2, column=3, sticky="ns")  # Place scrollbar in the grid

        # Configure the canvas
        self.canvas.configure(yscrollcommand=self.scrollbar.set)  # Link scrollbar to canvas
        self.canvas.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))  # Update scroll region when canvas size changes
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)  # Bind mouse wheel to scroll

        # Create a frame inside the canvas to hold the "Change" fields
        self.changes_frame = tk.Frame(self.canvas)  # Frame to hold "Change" fields
        self.canvas.create_window((0, 0), window=self.changes_frame, anchor="nw")  # Place frame inside canvas

        # Store references to "from" and "to" fields
        self.before_entries = []  # List to store "from" entry widgets
        self.after_entries = []  # List to store "to" entry widgets

        # Rename Button
        self.rename_button = tk.Button(root, text="Rename Files", command=self.rename_files)  # Button to rename files
        self.rename_button.grid(row=3, column=1, padx=10, pady=20, sticky="ew")  # Place button in the grid

    def browse_folder(self):
        # Open a folder dialog to select a folder
        folder_path = filedialog.askdirectory()
        if folder_path:
            self.folder_path_entry.delete(0, tk.END)  # Clear the entry widget
            self.folder_path_entry.insert(0, folder_path)  # Insert the selected folder path

    def create_change_entries(self):
        # Clear any existing fields in the changes frame
        for widget in self.changes_frame.winfo_children():
            widget.destroy()

        # Clear the lists storing references to entries
        self.before_entries.clear()
        self.after_entries.clear()

        # Get the number of changes from the entry widget
        try:
            num_changes = int(self.num_changes_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number of changes.")
            return

        # Create "from" and "to" fields for each change
        for i in range(num_changes):
            # Label for "from" field
            before_label = tk.Label(self.changes_frame, text=f"Change {i+1} from:")
            before_label.grid(row=i, column=0, padx=5, pady=5, sticky="w")

            # Entry widget for "from" field
            before_entry = tk.Entry(self.changes_frame, width=20)
            before_entry.grid(row=i, column=1, padx=5, pady=5, sticky="ew")
            self.before_entries.append(before_entry)  # Store reference to "from" field

            # Label for "to" field
            to_label = tk.Label(self.changes_frame, text="to:")
            to_label.grid(row=i, column=2, padx=5, pady=5, sticky="w")

            # Entry widget for "to" field
            after_entry = tk.Entry(self.changes_frame, width=20)
            after_entry.grid(row=i, column=3, padx=5, pady=5, sticky="ew")
            self.after_entries.append(after_entry)  # Store reference to "to" field

        # Update the scroll region to encompass the changes frame
        self.changes_frame.update_idletasks()
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def rename_files(self):
        # Get the folder path from the entry widget
        folder_path = self.folder_path_entry.get()
        if not folder_path:
            messagebox.showerror("Error", "Please select a folder path.")
            return

        # Get all "from" and "to" values from the fields
        before_values = [entry.get() for entry in self.before_entries]
        after_values = [entry.get() for entry in self.after_entries]

        print(f"Folder Path: {folder_path}")
        print(f"Before Values: {before_values}")
        print(f"After Values: {after_values}")

        try:
            # Iterate through all files in the folder
            for file in Path(folder_path).iterdir():
                if not file.is_file():  # Skip non-file items (e.g., folders)
                    print(f"Skipping non-file: {file.name}")
                    continue

                file_name = file.stem  # Get the file name without extension
                print(f"Original File Name: {file_name}")

                # Apply all changes to the file name
                for before, after in zip(before_values, after_values):
                    if before == "":  # If "from" is blank, skip this change
                        print(f"Skipping blank 'from' value.")
                        continue
                    print(f"Replacing '{before}' with '{after}' in '{file_name}'")
                    file_name = file_name.replace(before, after)

                new_file_name = file_name + file.suffix  # Add the file extension back
                print(f"New File Name: {new_file_name}")

                # Rename the file
                new_file_path = file.parent / new_file_name
                file.rename(new_file_path)
                print(f"Renamed '{file.name}' to '{new_file_name}'")

            messagebox.showinfo("Success", "Files renamed successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def _on_mousewheel(self, event):
        """Handle mouse wheel scrolling for the canvas."""
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

if __name__ == "__main__":
    root = tk.Tk()  # Create the main application window
    app = FileRenamerApp(root)  # Initialize the application
    root.mainloop()  # Start the main event loop
