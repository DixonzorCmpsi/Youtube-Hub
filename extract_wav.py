import os
import sys
from pathlib import Path
from moviepy.editor import VideoFileClip

class AudioExtractor:
    """
    A production-grade utility to strip audio from video files 
    and normalize it for Python data processing (Manim/SciPy).
    """

    def __init__(self, target_filename: str = "audio.wav"):
        self.target_filename = target_filename

    def convert(self, source_video_path: str):
        """
        Extracts audio from the source video and saves it as a .wav
        in the current directory.
        """
        source_path = Path(source_video_path)
        
        # 1. Validation
        if not source_path.exists():
            print(f"❌ Error: The file '{source_video_path}' does not exist.")
            return

        print(f"🔄 Processing: {source_path.name}")
        
        try:
            # 2. Load the Video Clip
            # specific to moviepy: we load the file but don't decode video frames yet (fast)
            video_clip = VideoFileClip(str(source_path))
            
            # 3. Check for Audio
            if video_clip.audio is None:
                print("⚠️ Warning: This video has no audio track.")
                return

            # 4. Export Audio
            # We enforce 44100Hz 16-bit PCM WAV (Standard for Manim/SciPy)
            output_path = Path.cwd() / self.target_filename
            
            print(f"   Extracting audio to: {output_path}...")
            video_clip.audio.write_audiofile(
                str(output_path),
                fps=44100,
                nbytes=2,       # 16-bit PCM
                codec='pcm_s16le',
                verbose=False,
                logger=None     # Suppress the moviepy progress bar spam
            )
            
            # 5. Cleanup
            # Crucial step: Release the file handle so Manim can read it immediately after
            video_clip.close()
            
            print(f"✅ Success! Audio saved as '{self.target_filename}'")
            print("   You can now run your Manim script.")

        except Exception as e:
            print(f"❌ Critical Error: {e}")

if __name__ == "__main__":
    # --- USAGE ---
    # You can change this string to whatever video file you want to process
    INPUT_VIDEO = "The NFL Height VS Weight Debate.mp4" 
    
    # Check if user provided an argument via command line (optional pro feature)
    if len(sys.argv) > 1:
        INPUT_VIDEO = sys.argv[1]

    extractor = AudioExtractor(target_filename="audio.wav")
    extractor.convert(INPUT_VIDEO)