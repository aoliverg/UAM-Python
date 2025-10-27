import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import xml.etree.ElementTree as ET
import codecs
import threading  # Required to prevent the GUI from freezing

# --- Core Processing Logic ---
# This function runs in a separate thread.
# It takes callback functions to safely update the GUI from the thread.
def process_tbx_file(input_file, l1_lang, l2_lang, output_file, status_callback, final_callback):
    """
    Parses the TBX file and writes the output.
    This function is designed to run in a separate thread.
    """
    try:
        # 1. Notify the GUI that processing has started
        status_callback(f"Processing {input_file}...")
        
        namespaces = {
            'ns': 'urn:iso:std:iso:30042:ed-2',
            'xml': 'http://www.w3.org/XML/1998/namespace'
        }
        
        count = 0
        
        # 2. Open output file and parse input
        with codecs.open(output_file, "w", encoding="utf-8") as output_stream:
            tree = ET.parse(input_file)
            root = tree.getroot()
            concept_entries = root.findall('.//ns:conceptEntry', namespaces)

            for conceptEntry in concept_entries:
                l1_sec = conceptEntry.find(f'./ns:langSec[@xml:lang="{l1_lang}"]', namespaces)
                l2_sec = conceptEntry.find(f'./ns:langSec[@xml:lang="{l2_lang}"]', namespaces)
                
                if l1_sec is not None and l2_sec is not None:
                    l1_term_elements = l1_sec.findall('.//ns:term', namespaces)
                    l1_terms = [term.text.strip() for term in l1_term_elements if term.text]
                    
                    l2_term_elements = l2_sec.findall('.//ns:term', namespaces)
                    l2_terms = [term.text.strip() for term in l2_term_elements if term.text]
                    
                    if l1_terms and l2_terms:
                        l2_string = ", ".join(l2_terms)
                        for l1_term in l1_terms:
                            output_stream.write(f"{l1_term}\t{l2_string}\n")
                            count += 1
        
        # 3. Notify the GUI of success
        final_callback(f"Success! Written {count} lines to {output_file}.", 
                       "Process Complete", 
                       "info")

    except FileNotFoundError:
        final_callback("Error: Input file not found.", "Error", "error")
    except ET.ParseError as e:
        final_callback(f"Error: Could not parse XML.\nDetail: {e}", "XML Error", "error")
    except Exception as e:
        # Catch any other unexpected error
        final_callback(f"An unexpected error occurred.\nDetail: {e}", "Error", "error")


# --- GUI Application Class ---
class TbxApp:
    def __init__(self, root_window):
        self.root = root_window
        self.root.title("TBX Term Extractor")
        self.root.minsize(500, 250) # Set a minimum size

        # --- Main Frame ---
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure resizing
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1) # Allow the entry widgets to expand

        # --- String Variables to hold data ---
        self.input_file_var = tk.StringVar()
        self.output_file_var = tk.StringVar()
        self.l1_var = tk.StringVar(value="en") # Default value
        self.l2_var = tk.StringVar(value="es") # Default value
        self.status_var = tk.StringVar(value="Ready.")

        # --- Widgets ---

        # 1. Input File
        ttk.Label(main_frame, text="Input TBX File:").grid(row=0, column=0, sticky=tk.W, pady=5)
        ttk.Entry(main_frame, textvariable=self.input_file_var, width=50).grid(row=0, column=1, sticky=(tk.W, tk.E), padx=5)
        ttk.Button(main_frame, text="Browse...", command=self.select_input_file).grid(row=0, column=2, padx=5)

        # 2. L1 Language
        ttk.Label(main_frame, text="L1 Language:").grid(row=1, column=0, sticky=tk.W, pady=5)
        ttk.Entry(main_frame, textvariable=self.l1_var, width=10).grid(row=1, column=1, sticky=tk.W, padx=5)

        # 3. L2 Language
        ttk.Label(main_frame, text="L2 Language:").grid(row=2, column=0, sticky=tk.W, pady=5)
        ttk.Entry(main_frame, textvariable=self.l2_var, width=10).grid(row=2, column=1, sticky=tk.W, padx=5)

        # 4. Output File
        ttk.Label(main_frame, text="Output TXT File:").grid(row=3, column=0, sticky=tk.W, pady=5)
        ttk.Entry(main_frame, textvariable=self.output_file_var, width=50).grid(row=3, column=1, sticky=(tk.W, tk.E), padx=5)
        ttk.Button(main_frame, text="Save As...", command=self.select_output_file).grid(row=3, column=2, padx=5)
        
        # 5. Separator
        ttk.Separator(main_frame, orient='horizontal').grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)

        # 6. Run Button
        self.run_button = ttk.Button(main_frame, text="Run Process", command=self.start_processing_thread)
        self.run_button.grid(row=5, column=1, pady=10)

        # 7. Status Bar
        status_label = ttk.Label(main_frame, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        status_label.grid(row=6, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=5, ipady=3)

    # --- Button Callbacks ---

    def select_input_file(self):
        """Opens a dialog to select the input TBX file."""
        filename = filedialog.askopenfilename(
            title="Select TBX File",
            filetypes=[("TBX files", "*.tbx"), ("XML files", "*.xml"), ("All files", "*.*")]
        )
        if filename:
            self.input_file_var.set(filename)

    def select_output_file(self):
        """Opens a dialog to select the output .txt file."""
        filename = filedialog.asksaveasfilename(
            title="Save Output File As",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
            defaultextension=".txt"
        )
        if filename:
            self.output_file_var.set(filename)

    # --- Thread-safe GUI Update Functions ---
    
    def update_status(self, message):
        """Thread-safe method to update the status bar."""
        self.status_var.set(message)

    def final_update(self, message, title, msg_type="info"):
        """
        Thread-safe method to show the final result and re-enable the button.
        This runs in the main GUI thread.
        """
        self.status_var.set(message)
        self.run_button.config(state=tk.NORMAL)  # Re-enable the button
        
        # Show the appropriate popup message
        if msg_type == "info":
            messagebox.showinfo(title, message)
        elif msg_type == "error":
            messagebox.showerror(title, message)

    def start_processing_thread(self):
        """
        Starts the file processing in a separate thread
        to prevent the GUI from freezing.
        """
        # 1. Get values from the GUI
        in_file = self.input_file_var.get()
        out_file = self.output_file_var.get()
        l1 = self.l1_var.get()
        l2 = self.l2_var.get()

        # 2. Validate input
        if not in_file or not out_file or not l1 or not l2:
            messagebox.showwarning("Missing Information", "Please fill in all fields.")
            return
        
        # 3. Disable the button to prevent double-clicks
        self.run_button.config(state=tk.DISABLED)
        self.status_var.set("Processing...")

        # 4. Create thread-safe callback functions
        #    These use root.after() to schedule GUI updates on the main thread
        def safe_status_callback(msg):
            self.root.after(0, self.update_status, msg)
            
        def safe_final_callback(msg, title, msg_type):
            self.root.after(0, self.final_update, msg, title, msg_type)

        # 5. Create and start the processing thread
        process_thread = threading.Thread(
            target=process_tbx_file,  # The function to run
            args=(in_file, l1, l2, out_file, safe_status_callback, safe_final_callback)
        )
        process_thread.daemon = True  # Allows the app to close even if the thread is running
        process_thread.start()

# --- Main Execution ---
if __name__ == "__main__":
    # Create the main window
    root = tk.Tk()
    
    # Create the application instance
    app = TbxApp(root)
    
    # Start the GUI event loop
    root.mainloop()