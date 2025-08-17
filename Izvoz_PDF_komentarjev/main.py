#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PDF Komentarji Izvoz - GUI način
"""

import os
import tkinter as tk
from tkinter import filedialog, messagebox
from pdf_komentarji_izvoz import PDFKomentarjiIzvoz

def gui_nacin():
    """GUI način za enostavno uporabo"""
    def izberi_datoteko():
        pot = filedialog.askopenfilename(
            title="Izberi PDF datoteko",
            filetypes=[("PDF datoteke", "*.pdf")]
        )
        if pot:
            vhod_label.config(text=pot)
            obdelaj_pdf(pot)

    def obdelaj_pdf(pot):
        base_name = os.path.splitext(pot)[0]
        annotation_datoteka = f"{base_name}_komentarji_improved.annotation"
        porocilo_pdf = f"{base_name}_porocilo_improved.pdf"
        porocilo_excel = f"{base_name}_porocilo_improved.xlsx"

        izvoznik = PDFKomentarjiIzvoz()
        if not izvoznik.preberi_pdf_komentarje(pot):
            messagebox.showerror("Napaka", "Ni uspelo prebrati komentarjev iz PDF.")
            return

        uspesno = []
        if izvoznik.izvozi_v_annotation(annotation_datoteka):
            uspesno.append(annotation_datoteka)
        if izvoznik.ustvari_porocilo_pdf(porocilo_pdf):
            uspesno.append(porocilo_pdf)
        if izvoznik.ustvari_excel_porocilo(porocilo_excel):
            uspesno.append(porocilo_excel)

        if uspesno:
            messagebox.showinfo("Končano", "Ustvarjene datoteke:\n" + "\n".join(uspesno))

    okno = tk.Tk()
    okno.title("PDF Komentarji Izvoz")
    okno.geometry("400x200")

    navodilo = tk.Label(okno, text="Izberi PDF datoteko za izvoz komentarjev:")
    navodilo.pack(pady=10)

    gumb = tk.Button(okno, text="Odpri PDF", command=izberi_datoteko)
    gumb.pack(pady=5)

    vhod_label = tk.Label(okno, text="Nobena datoteka ni izbrana", wraplength=350)
    vhod_label.pack(pady=10)

    okno.mainloop()

if __name__ == "__main__":
    gui_nacin()