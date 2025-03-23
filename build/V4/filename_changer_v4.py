import tkinter as tk
from tkinter import ttk, messagebox, filedialog, Toplevel
from pathlib import Path
import re
from transformers import DistilBertTokenizer, DistilBertForSequenceClassification
import torch
import sys

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

        # Add AI Rename button
        self.ai_rename_button = tk.Button(root, text="AI Generate Names", command=self.auto_generate_names)
        self.ai_rename_button.grid(row=1, column=3, padx=10, pady=10, sticky="e")

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


        # Model initalisation - dont know if needed
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.tokenizer = None
        self.model = None
        self.load_model()

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

    def load_model(self):
        """Load the DistilBERT model and tokenizer using pathlib"""
        try:
            # Get base path for compiled/normal execution
            if getattr(sys, 'frozen', False):
                # Running in compiled executable
                base_path = Path(sys._MEIPASS)
            else:
                # Running in script mode
                base_path = Path(__file__).parent

            model_dir = base_path / "trained_episode_classifier"
            
            if not model_dir.exists():
                raise FileNotFoundError(f"Model directory not found at {model_dir}")

            self.tokenizer = DistilBertTokenizer.from_pretrained(str(model_dir))
            self.model = DistilBertForSequenceClassification.from_pretrained(str(model_dir))
            
            # Device management
            self.model.to(self.device)
            self.model.eval()

        except Exception as e:
            messagebox.showerror("Model Error", f"Failed to load model: {str(e)}")
            raise  # Optional: Re-raise if you want error logging

    def predict_filename(self, filename):
        try:
            pattern = r'^(.*?)\.?S(\d{2})E(\d{2})\.?(.*)$'
            match = re.match(pattern, filename, re.IGNORECASE)

            if match:
                show_name = match.group(1).replace('.', ' ').strip()
                season = int(match.group(2))
                episode = int(match.group(3))
                remaining = match.group(4).replace('.', ' ').strip() if match.group(4) else ''
                
                words = remaining.split()                
                potential_title = []
                self.model.eval()

                with torch.no_grad():
                    for word in words:
                        inputs = self.tokenizer(
                        word,
                        return_tensors="pt",
                        padding=True,
                        max_length=32,
                        truncation=True
                        ).to(self.device)

                        outputs = self.model(**inputs)
                        prediction = torch.argmax(outputs.logits, dim=1).item()

                        if prediction == 1:
                            potential_title.append(word)
                        elif potential_title:
                            break
                episode_title = ' '.join(potential_title) if potential_title else None

                # Converts the season/episode to standard format it its a single digit e.g. S1E1 to S01E01
                season = f"{season:02}" if season > 0 else "01"
                episode = f"{episode:02}" if episode > 0 else "01"

                # Returns the show name, season no, episode no and episode title variables
                return (
                    show_name,
                    season,
                    episode,
                    episode_title
                )
            else:
                return None

        except Exception as e:
            # Log the full error for debugging
            import traceback
            traceback.print_exc()
            
            # Show error message with original filename
            messagebox.showerror(
                "Prediction Error", 
                f"Error processing filename '{filename}': {str(e)}\n"
                "Check console for full error details."
            )

            # Return safe defaults
            return (
                "UnknownShow",
                00,
                00,
                "Episode"
            )

    def auto_generate_names(self):
        folder_path = self.folder_path_entry.get()
        if not folder_path:
            messagebox.showerror("Error", "Please select a folder first")
            return

        try:
            folder = Path(folder_path)
            files = [f for f in folder.iterdir() if f.is_file()]
            if not files:
                messagebox.showinfo("Info", "No files found in selected folder")
                return
        except Exception as e:
            messagebox.showerror("Error", f"Could not read files: {str(e)}")
            return

        results = []
        for file in files:
            try:
                original_name = file.stem
                extension = file.suffix
                
                show_name, season, episode, episode_title = self.predict_filename(original_name)
                
                # Generate initial new name with title
                new_name = f"{show_name} - S{season}E{episode} {episode_title}{extension}"
                
                # Store components with title included by default
                results.append((
                    file.name,          # Original
                    new_name,           # New
                    show_name,          # Show
                    season,             # Season
                    episode,            # Episode
                    episode_title,      # Title
                    extension           # Ext
                ))
                
            except Exception as e:
                print(f"Error processing {file.name}: {str(e)}")
                results.append((
                    file.name,
                    f"ERROR: {str(e)}",
                    "", "", "", "", ""
                ))

        if results:
            self.show_ai_results(results)
        else:
            messagebox.showinfo("Info", "No valid files processed")

    def show_ai_results(self, results):
        try:
            preview_win = Toplevel(self.root)
            preview_win.title("AI Generated Names Preview")
            preview_win.geometry("900x500")

            main_frame = ttk.Frame(preview_win)
            main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

            # Create Treeview with checkboxes
            tree = ttk.Treeview(main_frame, 
                            columns=("Include", "Original", "New"),
                            show="headings")
            
            # Configure columns
            tree.heading("Include", text="Include Title")
            tree.heading("Original", text="Original Name")
            tree.heading("New", text="New Name")
            tree.column("Include", width=80, anchor=tk.CENTER)
            tree.column("Original", width=300, anchor=tk.W)
            tree.column("New", width=300, anchor=tk.W)
            
            # Store checkbox states
            self.checkbox_states = {}

            # Add scrollbar
            scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=tree.yview)
            tree.configure(yscrollcommand=scrollbar.set)

            # Populate data with checkboxes
            for idx, (original, new_name, show, season, episode, episode_title, extension) in enumerate(results):
                include_var = tk.BooleanVar(value=True)
                item_id = tree.insert("", "end", values=("✓", original, new_name))
                self.checkbox_states[item_id] = {
                'include': include_var,
                'components': (show, season, episode, episode_title, extension),
                'original': original
                }


            # Bind click event on Include column
            tree.bind("<Button-1>", lambda e: self.on_include_click(tree, e))                

            # Pack components
            tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

            # Add control buttons
            button_frame = ttk.Frame(preview_win)
            button_frame.pack(pady=10)
            
            ttk.Button(button_frame, text="Check All", 
                    command=lambda: self.toggle_all(tree, True)).pack(side=tk.LEFT, padx=5)
            ttk.Button(button_frame, text="Uncheck All", 
                    command=lambda: self.toggle_all(tree, False)).pack(side=tk.LEFT, padx=5)
            ttk.Button(button_frame, text="Apply Renames",
                    command=lambda: self.apply_ai_renames(tree)).pack(side=tk.LEFT, padx=5)

            # Store references
            self.preview_tree = tree

        except Exception as e:
            messagebox.showerror("Display Error", f"Failed to create preview: {str(e)}")

    def on_include_click(self, tree, event):
        """Handle clicks on the Include column"""
        x, y = event.x, event.y
        region = tree.identify_region(event.x, event.y)
        if region == "cell":
            column = tree.identify_column(event.x)
            item = tree.identify_row(event.y)
            if column == "#1":  # Include column is first visible column
                self.toggle_item_state(tree, item)
    
    def toggle_item_state(self, tree, item_id):
        """Toggle individual checkbox state and visual"""
        if item_id in self.checkbox_states:
            state_data = self.checkbox_states[item_id]
            current_state = state_data['include'].get()
            new_state = not current_state
            
            # Update state and visual
            state_data['include'].set(new_state)
            tree.set(item_id, "Include", "✓" if new_state else "✗")

    def toggle_all(self, tree, state):
        """Toggle all checkboxes without updating preview"""
        for item_id in tree.get_children():
            state_data = self.checkbox_states[item_id]
            state_data['include'].set(state)  # Access via dictionary
            tree.set(item_id, "Include", "✓" if state else "✗")
    
    def apply_ai_renames(self, tree):
        """Apply renames using current checkbox states"""
        folder_path = Path(self.folder_path_entry.get())
        try:
            for item_id in tree.get_children():
                data = self.checkbox_states[item_id]
                show, season, episode, episode_title, extension = data['components']
                
                if data['include'].get() and episode_title:  # Correct access
                    new_name = f"{show} - S{season}E{episode} {episode_title}{extension}"
                else:
                    new_name = f"{show} - S{season}E{episode}{extension}"
                
                original_path = folder_path / data['original']
                new_path = folder_path / new_name
                original_path.rename(new_path)
            
            messagebox.showinfo("Success", "Files renamed successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to rename files: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()  # Create the main application window
    app = FileRenamerApp(root)  # Initialize the application
    root.mainloop()  # Start the main event loop
