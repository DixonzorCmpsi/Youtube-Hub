import os
from pathlib import Path
from typing import Tuple
import sys

from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageFilter, ImageOps
from rembg import remove

class DeeTalkThumbnailGenerator:
    def __init__(self, output_dir: str = "./output"):
        self.canvas_size = (1920, 1080)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # --- CONFIGURATION (TWEAKED FOR PRO LOOK) ---
        self.split_start_ratio = 0.50  # Split starts at 50% width (Top) - MIDDLE
        self.split_end_ratio = 0.40    # Split ends at 40% width (Bottom)
        self.brand_cyan = "#00FFCC"
        
        # Font - Ensure this file is in your folder!
        self.font_path = "Montserrat-Black.ttf"
        self._default_font_size = 220

    def _load_image(self, path: str) -> Image.Image:
        """Safely loads an image and converts to RGBA."""
        if not os.path.exists(path):
            raise FileNotFoundError(f"Image not found: {path}")
        return Image.open(path).convert("RGBA")

    def create_split_masks(self) -> Tuple[Image.Image, Image.Image, Image.Image]:
        """Creates a cleaner, steeper diagonal split with a stroked separator line."""
        w, h = self.canvas_size
        
        # Calculate coordinates for a subtle slice
        top_x = int(w * self.split_start_ratio)
        bottom_x = int(w * self.split_end_ratio)
        
        # 1. Right Side Mask (White on Right)
        mask_right = Image.new('L', (w, h), 0)
        draw = ImageDraw.Draw(mask_right)
        # Draw polygon filling the right side
        draw.polygon([(top_x, 0), (w, 0), (w, h), (bottom_x, h)], fill=255)
        
        # 2. Left Side Mask (Inverse)
        mask_left = ImageOps.invert(mask_right)
        
        # 3. Diagonal Line with Stroke
        line_layer = Image.new('RGBA', (w, h), (0,0,0,0))
        draw_line = ImageDraw.Draw(line_layer)
        # Draw a thicker black line underneath for stroke
        stroke_width = 37  # 25 (main) + 12 (stroke on each side)
        draw_line.line([(top_x, 0), (bottom_x, h)], fill="black", width=stroke_width)
        # Draw the main white line on top
        draw_line.line([(top_x, 0), (bottom_x, h)], fill="white", width=25)
        
        return mask_left, mask_right, line_layer


    def create_composite_background(self, host_path: str, topic_path: str, mask_left: Image.Image, mask_right: Image.Image) -> Image.Image:
        """Combines Host image (Left, with cutout stroke) and Topic image (Right) - centered in their panels."""
        w, h = self.canvas_size

        # --- 1. Prepare Left (Host Image - with cutout stroke, keep background) ---
        raw_host = self._load_image(host_path)
        # Scale to cover canvas height, maintain aspect ratio
        host_ratio = raw_host.width / raw_host.height
        host_h = h
        host_w = int(host_h * host_ratio)
        # Slightly larger for cropped look
        scale_factor = 1.0
        host_w_large = int(host_w * scale_factor)
        host_h_large = int(host_h * scale_factor)
        host_scaled = raw_host.resize((host_w_large, host_h_large), Image.Resampling.LANCZOS)

        # Create host layer with background
        host_layer = Image.new('RGBA', self.canvas_size, (0, 0, 0, 255))
        left_center_x = int(w * 0.25)
        host_x = left_center_x - (host_w_large // 2)
        host_y = 0
        host_layer.paste(host_scaled, (host_x, host_y))

        # Crop out host and add stroke, zoom cutout to match background
        host_cutout = remove(raw_host)
        host_cutout_zoomed = host_cutout.resize((host_w_large, host_h_large), Image.Resampling.LANCZOS)
        host_with_stroke = self.add_stroke_to_cutout(host_cutout_zoomed, stroke_color="white", stroke_width=8)
        host_layer.paste(host_with_stroke, (host_x, host_y), mask=host_with_stroke)

        # --- 2. Prepare Right (Topic - with background, cutout stroke on top) ---
        raw_topic = self._load_image(topic_path)
        print("🤖 Removing background from topic image...")
        topic_cutout = remove(raw_topic)
        # Scale both to fit nicely in right panel
        topic_ratio = raw_topic.width / raw_topic.height
        topic_h = int(h * 0.95)  # 95% of canvas height
        topic_w = int(topic_h * topic_ratio)
        topic_bg_scaled = raw_topic.resize((topic_w, topic_h), Image.Resampling.LANCZOS)
        topic_cutout_scaled = topic_cutout.resize((topic_w, topic_h), Image.Resampling.LANCZOS)
        # Add professional stroke around the cutout
        topic_with_stroke = self.add_stroke_to_cutout(topic_cutout_scaled, stroke_color="white", stroke_width=8)
        # Center the topic in the RIGHT half of the canvas, align to top
        right_center_x = int(w * 0.77)
        topic_x = right_center_x - (topic_with_stroke.width // 2)
        topic_y = 0  # Align to top
        # Create a dark background for right side
        right_bg = Image.new('RGBA', self.canvas_size, (25, 25, 35, 255))
        # Paste topic background first
        right_bg.paste(topic_bg_scaled, (topic_x, topic_y))
        # Paste cutout with stroke on top
        right_bg.paste(topic_with_stroke, (topic_x, topic_y), mask=topic_with_stroke)

        # --- 3. Merge using masks ---
        final_bg = host_layer.copy()
        final_bg.paste(right_bg, (0, 0), mask=mask_right)
        return final_bg
    
    def add_stroke_to_cutout(self, img: Image.Image, stroke_color: str = "white", stroke_width: int = 8) -> Image.Image:
        """Adds a stroke/outline around a cutout image."""
        # Get alpha channel
        alpha = img.getchannel('A')
        
        # Create dilated version for stroke
        from PIL import ImageFilter
        dilated = alpha.filter(ImageFilter.MaxFilter(stroke_width * 2 + 1))
        
        # Create stroke layer
        stroke_layer = Image.new('RGBA', img.size, (0, 0, 0, 0))
        stroke_img = Image.new('RGBA', img.size, stroke_color)
        stroke_layer.paste(stroke_img, (0, 0), mask=dilated)
        
        # Paste original on top
        stroke_layer.paste(img, (0, 0), mask=img)
        
        return stroke_layer

    def process_host(self, image_path: str) -> Image.Image:
        print("🤖 Segmenting Host & Applying 'TV Lighting'...")
        img = self._load_image(image_path)
        cutout = remove(img)
        
        # --- PRO FIX: LIGHTING BOOST ---
        # 1. Boost Contrast (Makes you look sharper)
        enhancer = ImageEnhance.Contrast(cutout)
        cutout = enhancer.enhance(1.2)
        # 2. Boost Brightness (Fixes dim webcam lighting)
        enhancer = ImageEnhance.Brightness(cutout)
        cutout = enhancer.enhance(1.1)
        # 3. Boost Color/Saturation (Makes skin tones healthy)
        enhancer = ImageEnhance.Color(cutout)
        cutout = enhancer.enhance(1.2)

        # --- SCALING ---
        # Scale host to fit LEFT panel (about 40% of canvas width)
        # Height should overflow slightly for cropped look
        target_h = int(self.canvas_size[1] * 1.15)
        ratio = cutout.width / cutout.height
        target_w = int(target_h * ratio)
        
        # Limit width so host doesn't cross into right panel
        max_width = int(self.canvas_size[0] * 0.45)
        if target_w > max_width:
            target_w = max_width
            target_h = int(target_w / ratio)
        
        cutout = cutout.resize((target_w, target_h), Image.Resampling.LANCZOS)
        return cutout

    def add_logo(self, canvas: Image.Image) -> Image.Image:
        """Adds 'DT!' logo in the top left corner."""
        draw = ImageDraw.Draw(canvas)
        
        try:
            logo_font = ImageFont.truetype(self.font_path, 100)
        except:
            logo_font = ImageFont.load_default()
        
        logo_text = "DT!"
        
        # Position in top left with padding
        x = 30
        y = 20
        
        # Draw black stroke for logo
        stroke_w = 6
        draw.text((x, y), logo_text, font=logo_font, fill="black", stroke_width=stroke_w, stroke_fill="black")
        # Draw cyan logo text
        draw.text((x, y), logo_text, font=logo_font, fill=self.brand_cyan)
        
        return canvas

    def add_text(self, canvas: Image.Image, text: str) -> Image.Image:
        draw = ImageDraw.Draw(canvas)
        w, h = self.canvas_size

        min_font = 90
        max_font = 260
        font_size = max_font
        margin = 60
        lines = []
        
        # --- MULTILINE LOGIC ---
        words = text.split()
        char_count = len(text)
        # If more than 2 words or >18 chars, split into multiple lines
        if len(words) > 2 or char_count > 18:
            # Try to balance lines: greedy, max 3 lines
            current = []
            for word in words:
                if not current:
                    current.append(word)
                elif len(' '.join(current + [word])) <= max(18, char_count // 2) and len(current) < 5:
                    current.append(word)
                else:
                    lines.append(' '.join(current))
                    current = [word]
            if current:
                lines.append(' '.join(current))
        else:
            lines = [' '.join(words)]

        # Dynamically reduce font size until all lines fit within width and block fits above margin
        while font_size >= min_font:
            try:
                font = ImageFont.truetype(self.font_path, font_size)
            except:
                font = ImageFont.load_default()
            line_widths = []
            line_heights = []
            for line in lines:
                bbox = draw.textbbox((0, 0), line, font=font)
                line_widths.append(bbox[2] - bbox[0])
                line_heights.append(bbox[3] - bbox[1])
            total_height = sum(line_heights) + (len(lines) - 1) * int(font_size * 0.18)
            if max(line_widths) <= w - 2 * margin and total_height <= h // 2:
                break
            font_size -= 8
            
        # Final font
        try:
            font = ImageFont.truetype(self.font_path, font_size)
        except:
            font = ImageFont.load_default()

        # Recompute for final font
        line_widths = []
        line_heights = []
        for line in lines:
            bbox = draw.textbbox((0, 0), line, font=font)
            line_widths.append(bbox[2] - bbox[0])
            line_heights.append(bbox[3] - bbox[1])
        total_height = sum(line_heights) + (len(lines) - 1) * int(font_size * 0.18)
        y_start = h - total_height - 80

        # --- UPDATED: HEAVY DROP SHADOW (NO TRANSPARENCY) ---
        
        stroke_w = 15
        shadow_offset = 15 # Increased distance for better pop
        y = y_start
        
        for idx, line in enumerate(lines):
            # Split line into first/second word and rest for coloring
            line_words = line.split()
            total_words = len(' '.join(lines).split())
            if total_words >= 5:
                # First two words white, rest neon green
                if len(line_words) > 2:
                    first_part = ' '.join(line_words[:2])
                    rest = ' '.join(line_words[2:])
                else:
                    first_part = ' '.join(line_words)
                    rest = None
            else:
                if len(line_words) > 1:
                    first_part = line_words[0]
                    rest = ' '.join(line_words[1:])
                else:
                    first_part = line
                    rest = None
                    
            # Measure for centering
            first_bbox = draw.textbbox((0, 0), first_part, font=font)
            first_w = first_bbox[2] - first_bbox[0]
            if rest:
                rest_bbox = draw.textbbox((0, 0), rest, font=font)
                rest_w = rest_bbox[2] - rest_bbox[0]
                text_w = first_w + draw.textlength(' ', font=font) + rest_w
            else:
                text_w = first_w
                
            x = (w - text_w) // 2

            # --- 1. DRAW DROP SHADOW (OFFSET BLACK TEXT WITH STROKE) ---
            # We add stroke_width to the shadow too, otherwise the main text hides it.
            if rest:
                draw.text((x + shadow_offset, y + shadow_offset), first_part, font=font, fill="black", stroke_width=stroke_w, stroke_fill="black")
                draw.text((x + first_w + draw.textlength(' ', font=font) + shadow_offset, y + shadow_offset), rest, font=font, fill="black", stroke_width=stroke_w, stroke_fill="black")
            else:
                draw.text((x + shadow_offset, y + shadow_offset), first_part, font=font, fill="black", stroke_width=stroke_w, stroke_fill="black")

            # --- 2. DRAW MAIN TEXT WITH STROKE ---
            if rest:
                # Stroke
                draw.text((x, y), first_part, font=font, fill="black", stroke_width=stroke_w, stroke_fill="black")
                draw.text((x + first_w + draw.textlength(' ', font=font), y), rest, font=font, fill="black", stroke_width=stroke_w, stroke_fill="black")
                # Fill
                draw.text((x, y), first_part, font=font, fill="white")
                draw.text((x + first_w + draw.textlength(' ', font=font), y), rest, font=font, fill=self.brand_cyan)
            else:
                # Stroke
                draw.text((x, y), first_part, font=font, fill="black", stroke_width=stroke_w, stroke_fill="black")
                # Fill
                draw.text((x, y), first_part, font=font, fill=self.brand_cyan)
                
            y += line_heights[idx] + int(font_size * 0.18)
            
        return canvas

    def generate(self, host_path: str, topic_path: str, title: str):
        print(f"🎨 Compiling Final DeeTalk Thumbnail for host: {os.path.basename(host_path)} ...")
        # 1. Setup Split
        mask_left, mask_right, line_layer = self.create_split_masks()
        # 2. Backgrounds - Host on left, Topic on right (with cutout)
        final_comp = self.create_composite_background(host_path, topic_path, mask_left, mask_right)
        # 3. Add diagonal line
        final_comp.alpha_composite(line_layer)
        # 4. Add Logo
        final_comp = self.add_logo(final_comp)
        # 5. Text
        final_comp = self.add_text(final_comp, title.upper())
        # Output file named after host image
        host_base = os.path.splitext(os.path.basename(host_path))[0]
        output_path = self.output_dir / f"deetalk_{host_base}.png"
        final_comp.save(output_path)
        print(f"✅ Saved Pro Thumbnail to: {output_path}")

# --- EXECUTION ---
if __name__ == "__main__":
    host_folder = "Host-image"
    topic_folder = "Topic-image"
    
    # Find first image in each folder
    def find_images(folder):
        exts = [".png", ".jpg", ".jpeg", ".webp"]
        if not os.path.exists(folder):
            os.makedirs(folder)
            return []
        return [os.path.join(folder, fname) for fname in os.listdir(folder) if any(fname.lower().endswith(e) for e in exts)]

    def find_first_image(folder):
        exts = [".png", ".jpg", ".jpeg", ".webp"]
        if not os.path.exists(folder):
            os.makedirs(folder)
            return None
        for fname in os.listdir(folder):
            if any(fname.lower().endswith(e) for e in exts):
                return os.path.join(folder, fname)
        return None

    HOST_IMAGES = find_images(host_folder)
    TOPIC_IMG = find_first_image(topic_folder)

    if not HOST_IMAGES or not TOPIC_IMG:
        print(f"⚠️ Missing files! Ensure at least one image in '{host_folder}' and '{topic_folder}'.")
        sys.exit(1)

    # Prompt for punch line
    TITLE = input("Enter punch line for thumbnail: ")

    gen = DeeTalkThumbnailGenerator()
    for host_img in HOST_IMAGES:
        gen.generate(host_img, TOPIC_IMG, TITLE)