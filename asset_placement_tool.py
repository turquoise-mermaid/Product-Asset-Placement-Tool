"""
Asset Placement Tool
Batch processes design files into multiple product sizes with correct DPI
"""

from PIL import Image
import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import traceback


class AssetPlacementTool:
    def __init__(self, root):
        self.root = root
        self.root.title("Asset Placement Tool v1.0")
        self.root.geometry("700x600")
        self.root.resizable(False, False)
        
        # Variables
        self.cat_folder = tk.StringVar()
        self.logo_file = tk.StringVar()
        self.output_folder = tk.StringVar()
        
        # Product sizes (width, height, DPI) - Printful specs
        self.product_specs = {
            'stickers': {'size': (1250, 1250), 'dpi': 300},
            'mugs': {'size': (1250, 1250), 'dpi': 300},
            'tshirts': {'size': (3375, 3375), 'dpi': 300},
            'pillows': {'size': (4000, 4000), 'dpi': 150},
            'posters': {'size': (2400, 3000), 'dpi': 300},
            '300dpi': {'size': None, 'dpi': 300}  # Original size, just DPI change
        }
        
        # Logo placement for pillows (x, y coordinates)
        self.logo_position = (3600, 3626)
        
        self.setup_ui()
    
    def setup_ui(self):
        # Header
        header = tk.Label(
            self.root, 
            text="Asset Placement Tool", 
            font=("Arial", 18, "bold"),
            pady=20
        )
        header.pack()
        
        # Main frame
        main_frame = tk.Frame(self.root, padx=30, pady=10)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Input folder selection
        self.create_folder_selector(
            main_frame, 
            "Design Files Folder:", 
            self.cat_folder, 
            self.browse_cat_folder,
            0
        )
        
        # Logo file selection
        self.create_file_selector(
            main_frame,
            "Logo File (optional):",
            self.logo_file,
            self.browse_logo_file,
            1
        )
        
        # Output folder selection
        self.create_folder_selector(
            main_frame,
            "Output Folder:",
            self.output_folder,
            self.browse_output_folder,
            2
        )
        
        # Info section
        info_frame = tk.LabelFrame(main_frame, text="Output Products", padx=10, pady=10)
        info_frame.grid(row=3, column=0, columnspan=3, sticky="ew", pady=20)
        
        info_text = """
        This tool will create:
        • Stickers (1250×1250px @ 300 DPI)
        • Mugs (1250×1250px @ 300 DPI)
        • T-Shirts (3375×3375px @ 300 DPI)
        • Pillows (4000×4000px @ 150 DPI with logo)
        • Posters (2400×3000px @ 300 DPI)
        • 300 DPI versions (original size)
        """
        tk.Label(info_frame, text=info_text, justify=tk.LEFT).pack()
        
        # Progress bar
        self.progress = ttk.Progressbar(main_frame, mode='indeterminate')
        self.progress.grid(row=4, column=0, columnspan=3, sticky="ew", pady=10)
        
        # Status label
        self.status_label = tk.Label(main_frame, text="Ready to process", fg="blue")
        self.status_label.grid(row=5, column=0, columnspan=3, pady=5)
        
        # Process button
        process_btn = tk.Button(
            main_frame,
            text="Process Files",
            command=self.process_files,
            bg="#4CAF50",
            fg="white",
            font=("Arial", 12, "bold"),
            padx=30,
            pady=10,
            cursor="hand2"
        )
        process_btn.grid(row=6, column=0, columnspan=3, pady=20)
    
    def create_folder_selector(self, parent, label_text, variable, command, row):
        tk.Label(parent, text=label_text, font=("Arial", 10)).grid(
            row=row, column=0, sticky="w", pady=10
        )
        tk.Entry(parent, textvariable=variable, width=40).grid(
            row=row, column=1, padx=10
        )
        tk.Button(parent, text="Browse", command=command).grid(
            row=row, column=2
        )
    
    def create_file_selector(self, parent, label_text, variable, command, row):
        tk.Label(parent, text=label_text, font=("Arial", 10)).grid(
            row=row, column=0, sticky="w", pady=10
        )
        tk.Entry(parent, textvariable=variable, width=40).grid(
            row=row, column=1, padx=10
        )
        tk.Button(parent, text="Browse", command=command).grid(
            row=row, column=2
        )
    
    def browse_cat_folder(self):
        folder = filedialog.askdirectory(title="Select Design Files Folder")
        if folder:
            self.cat_folder.set(folder)
    
    def browse_logo_file(self):
        file = filedialog.askopenfilename(
            title="Select Logo File",
            filetypes=[("PNG files", "*.png"), ("All files", "*.*")]
        )
        if file:
            self.logo_file.set(file)
    
    def browse_output_folder(self):
        folder = filedialog.askdirectory(title="Select Output Folder")
        if folder:
            self.output_folder.set(folder)
    
    def validate_inputs(self):
        """Validate all required inputs"""
        if not self.cat_folder.get():
            messagebox.showerror("Error", "Please select a design files folder")
            return False
        
        if not os.path.isdir(self.cat_folder.get()):
            messagebox.showerror("Error", "Design files folder does not exist")
            return False
        
        if not self.output_folder.get():
            messagebox.showerror("Error", "Please select an output folder")
            return False
        
        # Check if there are any PNG files
        png_files = [f for f in os.listdir(self.cat_folder.get()) if f.lower().endswith('.png')]
        if not png_files:
            messagebox.showerror("Error", "No PNG files found in the design files folder")
            return False
        
        # Validate logo file if provided
        if self.logo_file.get() and not os.path.isfile(self.logo_file.get()):
            messagebox.showerror("Error", "Logo file does not exist")
            return False
        
        return True
    
    def process_files(self):
        """Main processing function"""
        if not self.validate_inputs():
            return
        
        try:
            self.progress.start()
            self.status_label.config(text="Processing files...", fg="orange")
            self.root.update()
            
            # Create output subfolders
            output_base = self.output_folder.get()
            output_folders = {
                '300dpi': os.path.join(output_base, '300_DPI'),
                'stickers': os.path.join(output_base, 'Stickers'),
                'mugs': os.path.join(output_base, 'Mugs'),
                'tshirts': os.path.join(output_base, 'Tshirts'),
                'pillows': os.path.join(output_base, 'Pillows'),
                'posters': os.path.join(output_base, 'Posters')
            }
            
            for folder in output_folders.values():
                os.makedirs(folder, exist_ok=True)
            
            # Load logo if provided
            logo_img = None
            if self.logo_file.get():
                try:
                    logo_img = Image.open(self.logo_file.get()).convert("RGBA")
                except Exception as e:
                    messagebox.showwarning("Warning", f"Could not load logo: {e}\nContinuing without logo...")
            
            # Process each PNG file
            cat_folder = self.cat_folder.get()
            png_files = [f for f in os.listdir(cat_folder) if f.lower().endswith('.png')]
            
            processed_count = 0
            for file in png_files:
                try:
                    cat_path = os.path.join(cat_folder, file)
                    base_name = os.path.splitext(file)[0]
                    
                    # Process for each product type
                    self.process_300dpi(cat_path, base_name, output_folders['300dpi'])
                    self.process_sticker(cat_path, base_name, output_folders['stickers'])
                    self.process_mug(cat_path, base_name, output_folders['mugs'])
                    self.process_tshirt(cat_path, base_name, output_folders['tshirts'])
                    self.process_pillow(cat_path, base_name, output_folders['pillows'], logo_img)
                    self.process_poster(cat_path, base_name, output_folders['posters'])
                    
                    processed_count += 1
                    self.status_label.config(
                        text=f"Processed {processed_count}/{len(png_files)} files",
                        fg="orange"
                    )
                    self.root.update()
                    
                except Exception as e:
                    error_msg = f"Error processing {file}: {str(e)}"
                    print(error_msg)
                    messagebox.showwarning("Warning", error_msg)
            
            self.progress.stop()
            self.status_label.config(
                text=f"✓ Successfully processed {processed_count} files!",
                fg="green"
            )
            
            messagebox.showinfo(
                "Success", 
                f"Processed {processed_count} files successfully!\n\nOutput saved to:\n{output_base}"
            )
            
        except Exception as e:
            self.progress.stop()
            self.status_label.config(text="Error occurred", fg="red")
            error_message = f"An error occurred:\n{str(e)}\n\n{traceback.format_exc()}"
            messagebox.showerror("Error", error_message)
    
    def process_300dpi(self, cat_path, base_name, output_folder):
        """Save original size with 300 DPI"""
        cat_img = Image.open(cat_path).convert("RGBA")
        output_path = os.path.join(output_folder, f"{base_name}_300dpi.png")
        cat_img.save(output_path, dpi=(300, 300), optimize=True)
    
    def process_sticker(self, cat_path, base_name, output_folder):
        """Process image for sticker"""
        cat_img = Image.open(cat_path).convert("RGBA")
        cat_img = cat_img.resize((1015, 1015), Image.Resampling.LANCZOS)
        sticker_out = cat_img.resize((1250, 1250), Image.Resampling.LANCZOS)
        output_path = os.path.join(output_folder, f"{base_name}_sticker.png")
        sticker_out.save(output_path, dpi=(300, 300), optimize=True)
    
    def process_mug(self, cat_path, base_name, output_folder):
        """Process image for mug"""
        cat_img = Image.open(cat_path).convert("RGBA")
        cat_img = cat_img.resize((1015, 1015), Image.Resampling.LANCZOS)
        mug_out = cat_img.resize((1250, 1250), Image.Resampling.LANCZOS)
        output_path = os.path.join(output_folder, f"{base_name}_mug.png")
        mug_out.save(output_path, dpi=(300, 300), optimize=True)
    
    def process_tshirt(self, cat_path, base_name, output_folder):
        """Process image for t-shirt"""
        cat_img = Image.open(cat_path).convert("RGBA")
        cat_img = cat_img.resize((1015, 1015), Image.Resampling.LANCZOS)
        tshirt_out = cat_img.resize((3375, 3375), Image.Resampling.LANCZOS)
        output_path = os.path.join(output_folder, f"{base_name}_shirt.png")
        tshirt_out.save(output_path, dpi=(300, 300), optimize=True)
    
    def process_pillow(self, cat_path, base_name, output_folder, logo_img):
        """Process image for pillow with optional logo"""
        cat_img = Image.open(cat_path).convert("RGBA")
        cat_img = cat_img.resize((1015, 1015), Image.Resampling.LANCZOS)
        pillow_out = cat_img.resize((4000, 4000), Image.Resampling.LANCZOS)
        
        # Add logo if available
        if logo_img:
            try:
                pillow_out.paste(logo_img, self.logo_position, logo_img)
            except Exception as e:
                print(f"Could not add logo to {base_name}: {e}")
        
        output_path = os.path.join(output_folder, f"{base_name}_pillow.png")
        pillow_out.save(output_path, dpi=(150, 150), optimize=True)
    
    def process_poster(self, cat_path, base_name, output_folder):
        """Process image for poster"""
        cat_img = Image.open(cat_path).convert("RGBA")
        cat_img = cat_img.resize((1015, 1015), Image.Resampling.LANCZOS)
        poster_out = cat_img.resize((2400, 3000), Image.Resampling.LANCZOS)
        output_path = os.path.join(output_folder, f"{base_name}_poster.png")
        poster_out.save(output_path, dpi=(300, 300), optimize=True)


def main():
    root = tk.Tk()
    app = AssetPlacementTool(root)
    root.mainloop()


if __name__ == "__main__":
    main()
