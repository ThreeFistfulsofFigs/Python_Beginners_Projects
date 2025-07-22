# ╔════════════════════════════════════════════════════════════════════════════╗
# ║                          Grok Image Generator                             ║
# ║  GUI application to generate and display images using the Grok API        ║
# ║  Features:                                                                ║
# ║  - Prompt-based image generation with quick prompts                       ║
# ║  - Support for input images and real-time display                         ║
# ║  - Progress tracking and status logging                                   ║
# ║  - Threaded API calls for responsiveness                                  ║
# ║  Author: [Your Name]                                                     ║
# ║  Creation Date: July 22, 2025                                            ║
# ║  Last Modified: July 22, 2025                                            ║
# ║  Notes: Requires grok3api and Pillow; uses custom imghdr.py               ║
# ║         Future: Add export options or enhance UI responsiveness          ║
# ╚════════════════════════════════════════════════════════════════════════════╝
import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog, messagebox
from grok3api.client import GrokClient
import threading
import time
import os
from PIL import Image, ImageTk
import io

class GrokImageGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("Grok Image Generator")
        self.root.geometry("800x700")
        self.root.configure(bg='#2b2b2b')

        # Initialize UI first
        self.setup_ui()

        # Initialize client
        try:
            self.client = GrokClient()
            self.client_status = "✅ Connected to Grok"
            self.status_label.config(text=self.client_status)
        except Exception as e:
            self.client = None
            self.client_status = f"❌ Error: {str(e)}"
            self.status_label.config(text=self.client_status)
            self.log_message(f"Client initialization failed: {str(e)}")

        self.generated_images = []

    def setup_ui(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)

        # Title
        title_label = ttk.Label(main_frame, text="🎨 Grok Image Generator",
                                font=('Arial', 16, 'bold'))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 10))

        # Status
        self.status_label = ttk.Label(main_frame, text="Initializing...")
        self.status_label.grid(row=1, column=0, columnspan=3, pady=(0, 10))

        # Prompt input
        ttk.Label(main_frame, text="Image Prompt:").grid(row=2, column=0, sticky=tk.W, pady=5)

        self.prompt_var = tk.StringVar()
        self.prompt_entry = ttk.Entry(main_frame, textvariable=self.prompt_var, width=50)
        self.prompt_entry.grid(row=2, column=1, sticky=(tk.W, tk.E), pady=5, padx=(5, 0))

        # Quick prompts
        quick_frame = ttk.Frame(main_frame)
        quick_frame.grid(row=3, column=0, columnspan=3, pady=5, sticky=(tk.W, tk.E))

        ttk.Label(quick_frame, text="Quick prompts:").pack(anchor=tk.W)

        quick_prompts = [
            "Create an image of a majestic sailing ship on stormy seas",
            "Create an image of a cute cat wearing sunglasses",
            "Create an image of a futuristic cityscape at sunset",
            "Create an image of a magical forest with glowing mushrooms",
            "Create an image of a vintage car in a desert landscape"
        ]

        for i, prompt in enumerate(quick_prompts):
            btn = ttk.Button(quick_frame, text=prompt,  # Display full prompt
                             command=lambda p=prompt: self.set_prompt(p))
            btn.pack(side=tk.LEFT, padx=2, pady=2)
            if i == 2:  # Line break after 3 buttons
                ttk.Frame(quick_frame).pack()

        # Optional input image
        ttk.Label(main_frame, text="Input Image (optional):").grid(row=4, column=0, sticky=tk.W, pady=5)

        image_frame = ttk.Frame(main_frame)
        image_frame.grid(row=4, column=1, sticky=(tk.W, tk.E), pady=5, padx=(5, 0))

        self.image_path_var = tk.StringVar()
        self.image_path_entry = ttk.Entry(image_frame, textvariable=self.image_path_var, width=40)
        self.image_path_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)

        browse_btn = ttk.Button(image_frame, text="Browse", command=self.browse_image)
        browse_btn.pack(side=tk.RIGHT, padx=(5, 0))

        # Generate button
        self.generate_btn = ttk.Button(main_frame, text="🚀 Generate Image",
                                       command=self.generate_image, style='Accent.TButton')
        self.generate_btn.grid(row=5, column=0, columnspan=3, pady=20)

        # Progress bar
        self.progress = ttk.Progressbar(main_frame, mode='indeterminate')
        self.progress.grid(row=6, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=5)

        # Status text
        self.status_text = scrolledtext.ScrolledText(main_frame, height=8, width=70)
        self.status_text.grid(row=7, column=0, columnspan=3, pady=10, sticky=(tk.W, tk.E))

        # Generated images frame
        self.images_frame = ttk.LabelFrame(main_frame, text="Generated Images", padding="10")
        self.images_frame.grid(row=8, column=0, columnspan=3, pady=10, sticky=(tk.W, tk.E))

        # Configure scrollable frame for images
        self.images_canvas = tk.Canvas(self.images_frame, height=200)
        self.images_scrollbar = ttk.Scrollbar(self.images_frame, orient="horizontal", command=self.images_canvas.xview)
        self.images_canvas.configure(xscrollcommand=self.images_scrollbar.set)

        self.images_canvas.pack(side="top", fill="both", expand=True)
        self.images_scrollbar.pack(side="bottom", fill="x")

        self.images_inner_frame = ttk.Frame(self.images_canvas)
        self.images_canvas.create_window((0, 0), window=self.images_inner_frame, anchor="nw")

        # Focus on prompt entry
        self.prompt_entry.focus()

    def set_prompt(self, prompt):
        self.prompt_var.set(prompt)

    def browse_image(self):
        filename = filedialog.askopenfilename(
            title="Select Input Image",
            filetypes=[
                ("Image files", "*.png *.jpg *.jpeg *.gif *.bmp *.tiff"),
                ("All files", "*.*")
            ]
        )
        if filename:
            self.image_path_var.set(filename)

    def log_message(self, message):
        """Add message to status text"""
        self.status_text.insert(tk.END, f"{time.strftime('%H:%M:%S')} - {message}\n")
        self.status_text.see(tk.END)
        self.root.update_idletasks()

    def generate_image(self):
        if not self.client:
            messagebox.showerror("Error", "Grok client not connected!")
            return

        prompt = self.prompt_var.get().strip()
        if not prompt:
            messagebox.showwarning("Warning", "Please enter an image prompt!")
            return

        # Disable button and start progress
        self.generate_btn.configure(state='disabled')
        self.progress.start(10)

        # Run generation in separate thread
        thread = threading.Thread(target=self._generate_thread, args=(prompt,))
        thread.daemon = True
        thread.start()

    def _generate_thread(self, prompt):
        try:
            self.log_message(f"🎨 Generating image: '{prompt}'")

            # Prepare parameters
            image_path = self.image_path_var.get().strip() if self.image_path_var.get().strip() else None

            if image_path and not os.path.exists(image_path):
                self.log_message(f"⚠️ Warning: Input image not found: {image_path}")
                image_path = None
            else:
                try:
                    Image.open(image_path)  # Verify image
                    self.log_message(f"📁 Valid input image: {os.path.basename(image_path)}")
                except Exception as e:
                    self.log_message(f"❌ Invalid input image: {e}")
                    image_path = None

            # Standardize prompt for image generation
            formatted_prompt = f"Create an image of {prompt}"
            self.log_message(f"📝 Formatted prompt: '{formatted_prompt}'")

            start_time = time.time()

            # Make the API call
            if image_path:
                result = self.client.ask(message=formatted_prompt, images=image_path)
                self.log_message(f"📁 Used input image: {os.path.basename(image_path)}")
            else:
                result = self.client.ask(message=formatted_prompt)

            duration = time.time() - start_time
            self.log_message(f"⏱️ Request completed in {duration:.1f} seconds")
            self.log_message(f"📄 Raw response: {str(result)[:100]}{'...' if len(str(result)) > 100 else ''}")

            # Process results
            if hasattr(result, 'modelResponse') and result.modelResponse:
                if hasattr(result.modelResponse, 'generatedImages') and result.modelResponse.generatedImages:
                    self.log_message(f"🖼️ Found {len(result.modelResponse.generatedImages)} generated image(s)!")

                    for i, image in enumerate(result.modelResponse.generatedImages):
                        try:
                            # Generate filename
                            timestamp = int(time.time())
                            safe_prompt = "".join(c for c in prompt if c.isalnum() or c in (' ', '-', '_')).rstrip()
                            safe_prompt = safe_prompt.replace(' ', '_')[:30]
                            filename = f"grok_{safe_prompt}_{timestamp}_{i}.jpg"

                            # Save image
                            if hasattr(image, 'save_to'):
                                image.save_to(filename)
                            elif hasattr(image, 'save'):
                                image.save(filename)
                            else:
                                self.log_message(f"⚠️ Image object found but no save method available: {type(image)}")
                                continue

                            self.log_message(f"💾 Saved: {filename}")
                            self.root.after(0, self._add_image_to_gui, filename)

                        except Exception as save_error:
                            self.log_message(f"❌ Error saving image {i}: {save_error}")
                else:
                    self.log_message("📝 No images were generated in the response")
            else:
                self.log_message("❌ No valid response received")

        except Exception as e:
            self.log_message(f"❌ Error: {str(e)}")

        finally:
            self.root.after(0, self._generation_complete)

    def _add_image_to_gui(self, filename):
        """Add generated image to the GUI display"""
        try:
            if not os.path.exists(filename):
                self.log_message(f"❌ Image file not found: {filename}")
                return
            img = Image.open(filename)
            img.thumbnail((150, 150), Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(img)

            img_frame = ttk.Frame(self.images_inner_frame)
            img_frame.pack(side=tk.LEFT, padx=5, pady=5)

            img_label = ttk.Label(img_frame, image=photo)
            img_label.image = photo
            img_label.pack()

            name_label = ttk.Label(img_frame, text=os.path.basename(filename),
                                   font=('Arial', 8))
            name_label.pack()

            open_btn = ttk.Button(img_frame, text="Open",
                                  command=lambda f=filename: os.startfile(f))
            open_btn.pack(pady=(2, 0))

            self.images_inner_frame.update_idletasks()
            self.images_canvas.configure(scrollregion=self.images_canvas.bbox("all"))

            self.generated_images.append(filename)

        except Exception as e:
            self.log_message(f"❌ Error displaying image: {e}")

    def _generation_complete(self):
        """Called when generation is complete"""
        self.progress.stop()
        self.generate_btn.configure(state='normal')
        self.log_message("✅ Generation complete!\n" + "─" * 50)

def main():
    root = tk.Tk()

    style = ttk.Style()
    try:
        style.theme_use('clam')
    except:
        pass

    app = GrokImageGenerator(root)
    root.mainloop()

if __name__ == "__main__":
    main()