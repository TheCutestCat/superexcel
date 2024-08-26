from moviepy.editor import VideoFileClip

def video_to_gif(video_path, output_gif_path, start_time=None, end_time=None, fps=10):
    """
    Converts a video file into a GIF.

    :param video_path: The path to the video file.
    :param output_gif_path: The path where the output GIF will be saved.
    :param start_time: Optional; starting time in the video from where GIF will be made.
    :param end_time: Optional; end time in the video until where GIF will be made.
    :param fps: Frames per second for the GIF. Lower value means smaller GIF file size.
    """
    try:
        with VideoFileClip(video_path) as video_clip:
            # If start_time and end_time are defined, cut the video
            if start_time is not None or end_time is not None:
                video_clip = video_clip.subclip(start_time, end_time)
            
            # Write the video clip to a GIF file
            video_clip.write_gif(output_gif_path, fps=fps)
            print(f"GIF saved successfully at {output_gif_path}")
    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage:
# video_to_gif("path/to/video.mp4", "output.gif", start_time=5, end_time=15)
