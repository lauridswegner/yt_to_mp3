import os
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from pytube import YouTube
from moviepy.editor import *
import threading


def download_youtube_video_as_mp3(video_url, output_path, on_progress):
    # Download the video using pytube
    yt = YouTube(video_url, on_progress_callback=on_progress)
    video = yt.streams.filter(only_audio=True).first()
    out_file = video.download(output_path='temp')

    # Convert video to mp3 using moviepy
    output_filename = os.path.join(output_path, f"{yt.title}.mp3")
    input_clip = AudioFileClip(out_file)
    input_clip.write_audiofile(output_filename)

    # Remove temporary video file
    os.remove(out_file)

    return output_filename


def browse_directory():
    download_directory = filedialog.askdirectory(initialdir=os.getcwd())
    save_path.set(download_directory)


def on_progress(stream, chunk, bytes_remaining):
    total_size = stream.filesize
    bytes_downloaded = total_size - bytes_remaining
    percentage = (bytes_downloaded / total_size) * 100
    progress_bar['value'] = percentage
    root.update_idletasks()


def download_and_convert():
    video_url = url.get()
    output_path = save_path.get()

    def thread_task():
        try:
            output_filename = download_youtube_video_as_mp3(video_url, output_path, on_progress)
            messagebox.showinfo("Success", f"Video downloaded and converted successfully as\n{output_filename}")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred:\n{e}")

        # Reset progress bar
        progress_bar['value'] = 0

    download_thread = threading.Thread(target=thread_task)
    download_thread.start()


# Create the tkinter GUI
root = tk.Tk()
root.title("YouTube to MP3 Downloader")

# Create input fields and labels
url_label = tk.Label(root, text="Enter YouTube Video URL:")
url = tk.StringVar()
url_entry = tk.Entry(root, textvariable=url, width=50)

save_path_label = tk.Label(root, text="Choose Output Directory:")
save_path = tk.StringVar()
save_path_entry = tk.Entry(root, textvariable=save_path, width=50)
browse_button = tk.Button(root, text="Browse", command=browse_directory)

download_button = tk.Button(root, text="Download and Convert", command=download_and_convert)

progress_bar = ttk.Progressbar(root, orient='horizontal', length=300, mode='determinate')

# Place elements on the GUI
url_label.grid(row=0, column=0, padx=5, pady=5, sticky='w')
url_entry.grid(row=0, column=1, padx=5, pady=5, columnspan=2)

save_path_label.grid(row=1, column=0, padx=5, pady=5, sticky='w')
save_path_entry.grid(row=1, column=1, padx=5, pady=5)
browse_button.grid(row=1, column=2, padx=5, pady=5)

download_button.grid(row=2, column=1, padx=5, pady=20)
progress_bar.grid(row=3, column=1, padx=5, pady=5)

# Run the tkinter main loop
root.mainloop()
