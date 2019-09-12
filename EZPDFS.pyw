# EZPDFS v1 by Christopher Vergilio
# Website: christopherv.dev

import os
import shutil
import fnmatch
import sys
import time
from tkinter import *
from tkinter.filedialog import askopenfilename
from tkinter.messagebox import showerror, showinfo
from PyPDF2 import PdfFileReader, PdfFileWriter


class MyFrame(Frame):
    def __init__(self):
        Frame.__init__(self)
        self.master.title("EZPDFS")
        self.master.resizable(False, False)
        self.master.rowconfigure(5, weight=1)
        self.master.columnconfigure(5, weight=1)
        self.grid(sticky=W+E+N+S, padx=5, pady=7)

        self.var1 = BooleanVar()
        self.delete_original = False
        self.rename_files = False
        self.pdf_file = ""
        self.num_of_pages = 0
        self.title = Label(self, text="EZ PDF Splitter").grid(row=1, sticky=W)
        self.button1 = Button(self, text="Browse",
                              command=self.load_file, width=10)
        self.button1.grid(row=2, column=0, sticky=E)
        self.button2 = Button(self, text="Split", command=self.do_everything,
                              width=10, state=DISABLED)
        self.button2.grid(row=2, column=1, sticky=W)
        self.delete = Checkbutton(self, text="Delete original?",
                                  variable=self.var1).grid(
                                                      row=3,
                                                      sticky=W)
        self.credits = Label(self, text="christopherv.dev").grid(
                                                            row=4,
                                                            column=1,
                                                            sticky=E)

    def load_file(self):
        fname = askopenfilename(
            filetypes=(("PDF files", "*.pdf"), ("All files", "*.*"))
            )

        self.pdf_file = fname.replace('/', "\\")
        if self.pdf_file != "":
            self.button2.config(state=NORMAL)

    def do_everything(self):
        try:
            self.delete_original = format(self.var1.get())
            self.splitter(self.pdf_file)
            self.pdf_file == ""
            self.button2.config(state=DISABLED)
            showinfo("Complete", "PDF successfully split!\nNumber of pages: "
                     + str(self.num_of_pages))

        except (FileNotFoundError):
            showerror("Error", "File could not be found.")
            self.button2.config(state=DISABLED)

    def splitter(self, i):
        self.pdf_splitter(i)
        if str(self.delete_original) == "True":
            os.remove(i)

    def pdf_splitter(self, path):
        fileuse = open(path, "rb")
        inputpdf = PdfFileReader(fileuse)
        num_of_pages = 0

        for i in range(inputpdf.numPages):
            num_of_pages += 1
            output = PdfFileWriter()
            output.addPage(inputpdf.getPage(i))
            with open("Document-page%s.pdf" % i, "wb") as outputStream:
                output.write(outputStream)

        fileuse.close()
        self.num_of_pages = num_of_pages


if __name__ == "__main__":
    MyFrame().mainloop()
