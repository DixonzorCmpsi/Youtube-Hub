import numpy as np
from manim import *
from scipy.io import wavfile
from scipy.fftpack import fft
from moviepy.editor import VideoFileClip
import os

# --- STEP 1: THE EXTRACTOR ---
def extract_audio(video_path, audio_path="audio.wav"):
    """
    Extracts audio from video and saves as standard WAV.
    """
    print(f"🔄 Extracting audio from {video_path}...")
    if not os.path.exists(video_path):
        raise FileNotFoundError(f"❌ Video not found: {video_path}")
        
    clip = VideoFileClip(video_path)
    # Write 44100Hz mono wav
    clip.audio.write_audiofile(
        audio_path, fps=44100, nbytes=2, codec='pcm_s16le', 
        verbose=False, logger=None
    )
    clip.close()
    print("✅ Audio extraction complete.")

class FinalSpectrum(Scene):
    def construct(self):
        # --- CONFIGURATION ---
        VIDEO_FILE = "The NFL Height VS Weight Debate.mp4" # <--- REPLACE THIS with your video file name
        AUDIO_FILE = "audio.wav"
        
        # 1. RUN EXTRACTION
        # This automatically creates the wav file you need
        extract_audio(VIDEO_FILE, AUDIO_FILE)
        
        # 2. LOAD DATA
        rate, data = wavfile.read(AUDIO_FILE)
        if len(data.shape) > 1: data = data.mean(axis=1) # Mono
        data = data / np.max(np.abs(data)) # Normalize
        
        # 3. PRE-BAKE ANIMATION DATA (The PhD Step)
        # We calculate the height of every bar for every frame NOW.
        # This ensures the animation cannot fail during render.
        print("🍞 Baking animation data...")
        
        fps = config.frame_rate
        total_frames = int(len(data) / rate * fps)
        num_bars = 30
        
        # This list will hold the heights for every single frame
        # Shape: [Frame 1: [h1, h2...], Frame 2: [h1, h2...], ...]
        baked_heights = []
        
        for f in range(total_frames):
            # Find the audio index for this frame
            time_sec = f / fps
            idx = int(time_sec * rate)
            
            # FFT Window
            fft_size = 2048
            if idx + fft_size < len(data):
                chunk = data[idx : idx + fft_size]
                fft_res = np.abs(fft(chunk)[:fft_size//2])
                
                # Bucketing
                frame_bars = []
                chunk_size = len(fft_res) // num_bars
                for b in range(num_bars):
                    section = fft_res[b*chunk_size : (b+1)*chunk_size]
                    vol = np.mean(section)
                    h = 0.1 + (vol * 0.2) # Sensitivity
                    frame_bars.append(min(h, 6.0))
                baked_heights.append(frame_bars)
            else:
                baked_heights.append([0.1] * num_bars)

        print(f"✅ Baked {len(baked_heights)} frames of data.")

        # 4. SETUP VISUALS
        bars = VGroup()
        for i in range(num_bars):
            color = interpolate_color(BLUE, PURPLE, i/num_bars)
            bar = Rectangle(width=0.2, height=0.1, fill_color=color, fill_opacity=1, stroke_width=0)
            bar.move_to(RIGHT * (i - num_bars/2) * 0.25)
            bar.align_to(DOWN * 2, DOWN)
            bars.add(bar)
        
        self.add(bars)
        
        # 5. ANIMATE USING BAKED DATA
        # We use a ValueTracker to track the frame number
        frame_tracker = ValueTracker(0)
        
        def update_bars(mob):
            # Get current frame index from tracker
            f = int(frame_tracker.get_value())
            
            # Retrieve the pre-calculated heights
            if f < len(baked_heights):
                current_heights = baked_heights[f]
                for i, bar in enumerate(mob):
                    target_h = current_heights[i]
                    # Direct geometry set (fast and robust)
                    bar.stretch_to_fit_height(target_h)
                    bar.align_to(DOWN * 2, DOWN)
                    
        bars.add_updater(update_bars)
        
        # 6. RENDER
        self.add_sound(AUDIO_FILE)
        
        # Animate the frame_tracker from 0 to total_frames
        duration = len(data) / rate
        self.play(
            frame_tracker.animate.set_value(total_frames),
            run_time=duration,
            rate_func=linear # Linear is crucial for audio sync
        )

# RUN COMMAND (Use --format=mp4 to help Windows):
# manim -pql video-animator.py FinalSpectrum