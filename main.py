import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
import os
import soundfile as sf
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
import webbrowser

class SpectrogramDialog(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Spectrogram Parameters")

        self.lower_freq = tk.DoubleVar()
        self.upper_freq = tk.DoubleVar()

        tk.Label(self, text="Lower Frequency:").pack()
        tk.Entry(self, textvariable=self.lower_freq).pack()
        tk.Label(self, text="Upper Frequency:").pack()
        tk.Entry(self, textvariable=self.upper_freq).pack()

        tk.Button(self, text="Create Spectrogram", command=self.create_spectrogram).pack()

    def create_spectrogram(self):
        lower_freq = self.lower_freq.get()
        upper_freq = self.upper_freq.get()
        self.master.create_spectrogram(lower_freq, upper_freq)
        self.destroy()

class AudioAnalysisGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Audio Analysis")

        self.loaded_file_path = None
        self.window_size = tk.IntVar()

        self.create_widgets()

    def create_widgets(self):
        frame = tk.Frame(self)
        frame.pack(padx=10, pady=10)

        btn_load = tk.Button(frame, text="Load Audio", command=self.load_audio)
        btn_load.pack(side=tk.LEFT, padx=5)

        btn_dialog = tk.Button(frame, text="Set Spectrogram Parameters", command=self.open_dialog)
        btn_dialog.pack(side=tk.LEFT, padx=5)

        btn_analyze = tk.Button(frame, text="Analyze Audio", command=self.analyze_audio)
        btn_analyze.pack(side=tk.LEFT, padx=5)

        btn_save = tk.Button(frame, text="Save Results", command=self.save_results)
        btn_save.pack(side=tk.LEFT, padx=5)

        btn_help = tk.Button(frame, text="Help and Manual", command=self.open_manual)
        btn_help.pack(side=tk.LEFT, padx=5)

    def load_audio(self):
        self.loaded_file_path = filedialog.askopenfilename()
        if self.loaded_file_path:
            data, samplerate = sf.read(self.loaded_file_path)
            length = len(data) / samplerate
            messagebox.showinfo("Audio Info", f"Length: {length} seconds\nSample Rate: {samplerate} Hz")

    def open_dialog(self):
        dialog = SpectrogramDialog(self)

    def create_spectrogram(self, lower_freq, upper_freq):
        if not self.loaded_file_path:
            messagebox.showwarning("No Audio File", "Please load an audio file first.")
            return

        data, samplerate = sf.read(self.loaded_file_path)
        f, t, Sxx = signal.spectrogram(data, samplerate, nperseg=8192)  # Set nperseg to 8192
        plt.pcolormesh(t, f, 10 * np.log10(Sxx))
        plt.ylabel('Frequency [Hz]')
        plt.xlabel('Time [sec]')
        plt.colorbar(label='Intensity [dB]')
        plt.title(os.path.basename(self.loaded_file_path))  # Add the file name as title
        plt.ylim(lower_freq, upper_freq)  # Set frequency range

        # Save the spectrogram as a picture
        save_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
        if save_path:
            plt.savefig(save_path)
            messagebox.showinfo("Spectrogram Saved", f"Spectrogram saved as {save_path}")

        # Show the spectrogram
        plt.show()

        # Close the figure window to release resources
        plt.close()

    def analyze_audio(self):
        if not self.loaded_file_path:
            messagebox.showwarning("No Audio File", "Please load an audio file first.")
            return
        # Your code to analyze audio using AI model goes here
        # For demonstration, just showing a message
        messagebox.showinfo("Model Output", "AI model output will appear here")

    def save_results(self):
        if not self.loaded_file_path:
            messagebox.showwarning("No Audio File", "Please load an audio file first.")
            return
        file_path = filedialog.asksaveasfilename(defaultextension=".txt")
        if file_path:
            # Your code to save results goes here
            # For demonstration, just showing a message
            messagebox.showinfo("Save Results", f"Results saved to {file_path}")

    def open_manual(self):
        manual_path = "documentation.pdf"
        webbrowser.open(manual_path)

if __name__ == "__main__":
    app = AudioAnalysisGUI()
    app.mainloop()
