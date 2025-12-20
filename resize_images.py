#!/usr/bin/env python3
"""
Resize and optimize banner images for YouTube.
YouTube banners should be 2560x1440 pixels and under 6MB.
"""

from pathlib import Path
from PIL import Image
import os

# Target dimensions for YouTube banner
TARGET_WIDTH = 2560
TARGET_HEIGHT = 1440
MAX_FILE_SIZE = 6 * 1024 * 1024  # 6MB in bytes

def resize_and_optimize_image(input_path: Path, output_path: Path = None):
    """Resize and optimize an image to YouTube banner specifications."""
    if output_path is None:
        output_path = input_path
    
    try:
        # Open image
        img = Image.open(input_path)
        original_size = input_path.stat().st_size
        
        print(f"Processing: {input_path.name}")
        print(f"  Original size: {img.size[0]}x{img.size[1]}")
        print(f"  Original file size: {original_size / 1024 / 1024:.2f} MB")
        
        # Resize to target dimensions (maintains aspect ratio, crops if needed)
        img_resized = img.resize((TARGET_WIDTH, TARGET_HEIGHT), Image.Resampling.LANCZOS)
        
        # Save as PNG with optimization
        img_resized.save(output_path, 'PNG', optimize=True)
        file_size = output_path.stat().st_size
        
        if file_size <= MAX_FILE_SIZE:
            print(f"  ✓ Resized to: {img_resized.size[0]}x{img_resized.size[1]}")
            print(f"  ✓ File size: {file_size / 1024 / 1024:.2f} MB")
            return True
        
        # If still too large, try converting to RGB and reducing colors
        if img_resized.mode in ('RGBA', 'LA', 'P'):
            # Convert to RGB (removes alpha channel)
            rgb_img = Image.new('RGB', img_resized.size, (255, 255, 255))
            if img_resized.mode == 'P':
                img_resized = img_resized.convert('RGBA')
            rgb_img.paste(img_resized, mask=img_resized.split()[3] if img_resized.mode == 'RGBA' else None)
            img_resized = rgb_img
        
        # Save again as PNG
        img_resized.save(output_path, 'PNG', optimize=True)
        file_size = output_path.stat().st_size
        
        if file_size <= MAX_FILE_SIZE:
            print(f"  ✓ Resized to: {img_resized.size[0]}x{img_resized.size[1]} (RGB)")
            print(f"  ✓ File size: {file_size / 1024 / 1024:.2f} MB")
            return True
        
        # Last resort: convert to JPEG (but keep PNG name - you'll need to change manually if needed)
        print(f"  ⚠ Warning: PNG file size is {file_size / 1024 / 1024:.2f} MB (above 6MB limit)")
        print(f"  ⚠ Consider using JPEG format or reducing image complexity")
        print(f"  ✓ Resized to: {img_resized.size[0]}x{img_resized.size[1]}")
        return True  # Still save it, user can decide what to do
        
    except Exception as e:
        print(f"  ✗ Error processing {input_path.name}: {e}")
        return False

def main():
    """Resize all PNG images in the images/default/ directory."""
    images_dir = Path('images/winter')
    
    if not images_dir.exists():
        print(f"Error: {images_dir} does not exist")
        return
    
    # Find all PNG files
    png_files = list(images_dir.glob('*.png'))
    
    if not png_files:
        print(f"No PNG files found in {images_dir}")
        return
    
    print(f"Found {len(png_files)} PNG files to process\n")
    
    # Process each file
    success_count = 0
    for png_file in sorted(png_files):
        if resize_and_optimize_image(png_file):
            success_count += 1
        print()
    
    print(f"Processed {success_count}/{len(png_files)} files successfully")

if __name__ == '__main__':
    main()

