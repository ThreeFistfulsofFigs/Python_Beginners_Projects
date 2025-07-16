"""
╔══════════════════════════════════════════════════════════════════════════════════════╗
║                              MILES TO KILOMETERS CONVERTER                           ║
║                                                                                      ║
║  A simple GUI application that converts miles to kilometers using tkinter.          ║
║                                                                                      ║
║  Features:                                                                          ║
║    • Input field for miles value                                                   ║
║    • Click "Calculate" button or press Enter to convert                            ║
║    • Real-time conversion display                                                  ║
║    • Error handling for invalid inputs                                             ║
║                                                                                      ║
║  Layout:                                                                           ║
║    Row 0: [Input Field] [Miles]                                                   ║
║    Row 1: [is equal to] [Result] [Km]                                            ║
║    Row 2:               [Calculate]                                                ║
║                                                                                      ║
║  Usage: Enter a number in miles and press Enter or click Calculate                 ║
╚══════════════════════════════════════════════════════════════════════════════════════╝
"""

import tkinter
from tkinter import Entry

# ═══════════════════════════════════════════════════════════════════════════════════════
#                                   WINDOW SETUP
# ═══════════════════════════════════════════════════════════════════════════════════════

# Create the main window
window = tkinter.Tk()
window.title("Miles to Km Converter")
window.minsize(width=300, height=100)
window.config(padx=50, pady=100)

# ═══════════════════════════════════════════════════════════════════════════════════════
#                                   GUI ELEMENTS
# ═══════════════════════════════════════════════════════════════════════════════════════

# Entry widget for miles input (Row 0, Column 0)
input_int = Entry(width=10)
input_int.grid(row=0, column=1, padx=10, pady=10)
input_int.bind('<Return>', lambda event: Converter())  # Enable Enter key conversion

# "Miles" label (Row 0, Column 1)
miles_label = tkinter.Label(text="Miles")
miles_label.grid(row=0, column=2, padx=10, pady=10)

# "is equal to" label (Row 1, Column 0)
equal_label = tkinter.Label(text="is equal to")
equal_label.grid(row=1, column=0, padx=10, pady=10)

# Result label for kilometers (Row 1, Column 1)
result_label = tkinter.Label(text="0")
result_label.grid(row=1, column=1, padx=10, pady=10)

# "Km" label (Row 1, Column 2)
km_label = tkinter.Label(text="Km")
km_label.grid(row=1, column=2, padx=10, pady=10)


# ═══════════════════════════════════════════════════════════════════════════════════════
#                                   FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════════════════

def Converter():
    """
    Converts miles to kilometers and updates the result display.

    Uses the precise conversion factor: 1 mile = 1.609344 kilometers
    Handles invalid input by displaying "0" in the result field.
    """
    try:
        miles_value = float(input_int.get())
        km_value = miles_value * 1.609344  # Precise conversion factor
        result_label.config(text=f"{km_value:.2f}")
    except ValueError:
        result_label.config(text="0")


# ═══════════════════════════════════════════════════════════════════════════════════════
#                                   BUTTONS
# ═══════════════════════════════════════════════════════════════════════════════════════

# Calculate button (Row 2, Column 1)
button = tkinter.Button(text="Calculate", command=Converter)
button.grid(row=2, column=1, padx=10, pady=10)

window.mainloop()