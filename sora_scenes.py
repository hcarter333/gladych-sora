import os
import time
import sys
from pathlib import Path
import json
import io
from PIL import Image

import requests
from openai import OpenAI

# Directory to save all generated clips
OUTPUT_DIR = Path("sora_gladych_cwhaptics_scenes")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
INITIAL_REFERENCE_FILENAME = "refimg_0.png"

# All the Sora prompts we defined for the short

openai = OpenAI()

# Shared continuity context for all scenes

CONTEXT = """
[CONTEXT — SAME SHORT CARTOON FILM]
This is a single, unified, lighthearted 1950s-style cartoon short about
a ham-radio haptic sidetone app.

Visual style:
- Two cheerful cartoon kids in a vintage kids' comic style:
  * Red-haired kid: round face, red bowl-cut hair, green-and-white striped shirt,
    bright yellow shorts with suspenders, round shoes.
  * Blonde kid: long ponytail tied with a big ribbon,
    blue dress and tiny academic cap, white socks and shoes.
- A small brown puppy sidekick that behaves like a friendly little robot:
  wagging tail, cheerful face, sometimes beeping or flashing tiny lights.
- Thick black outlines, soft shading, warm retro-paper texture.
- The tone is upbeat, curious, friendly, and imaginative.
- IMPORTANT: Do NOT draw any readable on-screen text or captions.
"""

SCENES = [
    # SCENE 1 – no reference needed, though optional refimg_0 is supported

    # SCENE 4 – requires refimg_3.png (frame from scene 3)
    {
        "model": "sora-2",
        "seconds": "8",
        "size": "720x1280",
        "prompt": f"""
{CONTEXT}

[SCENE 4 — PEEL TRANSITION TO REAL PHONE COOTIE KEY]

Vertical 6:19 / 9:16.

We start tight on the glowing fingertip of the cartoon red-haired kid touching the
cartoon Morse key.

A reference still image from Scene 3 is provided. Match:
- the glowing finger style,
- cockpit lighting,
- character proportions.

The entire cartoon cockpit gently peels away like a sticker to reveal a real-world desk.

A real human finger hovers over a Project TouCans–style haptic cootie key UI on a phone.
The UI is abstract and icon-based (no text). Each tap produces a soft ripple animation,
suggesting haptic feedback.

Bright, friendly lighting keeps the tone connected to the cartoon world.
""".strip(),
        "reference_filename": "refimg_0.png",
        "reference_instructions": (
            "From Scene 3 (03_mentor_voice_use_the_haptics.mp4), capture a frame showing "
            "the glowing fingertip and cockpit background together. Avoid any visible text. "
            "Save as refimg_0.png."
        ),
    },

    # SCENE 5 – requires refimg_4.png (frame from scene 4)
    {
        "model": "sora-2",
        "seconds": "8",
        "size": "720x1280",
        "prompt": f"""
{CONTEXT}

[SCENE 5 — HAPPY HAPTIC MORSE IN STAR CRUISER]

Vertical 6:19 / 9:16.

Back in the cartoon star cruiser.

A reference image from Scene 4 is provided. Match:
- the glowing fingertip vibe,
- soft lighting,
- general proportions of the kid.

The red-haired kid now has the glowing ear-muffs and glowing fingertips.
They happily tap an invisible Morse key on the console. The rhythm corresponds
to KD0FNR but NOTHING should be written onscreen.

The blonde kid smiles proudly from the mission-control screen.
The robo-puppy bounces in place, beeping cheerfully in rhythm.

The camera gently orbits to show the warm glow and colorful cockpit.
""".strip(),
        "reference_filename": "refimg_4.png",
        "reference_instructions": (
            "From Scene 4 (04_phone_cootie_key_transition.mp4), capture a macro-style frame "
            "of the real finger over the haptic phone UI showing the horizontal key bar clearly. "
            "Save as refimg_4.png."
        ),
    },

    # SCENE 6 – requires refimg_5.png (frame from scene 5)
    {
        "model": "sora-2",
        "seconds": "8",
        "size": "720x1280",
        "prompt": f"""
{CONTEXT}

[SCENE 6 — CARTOON BOOST & PHONE HERO SHOT]

Vertical 6:19 / 9:16.

A reference image from Scene 5 is provided. Match:
- the cockpit color palette,
- the red-haired kid’s appearance,
- soft glowy lighting.

The friendly cartoon star cruiser gently swooshes upward in space with a trail
of sparkly Morse-like dots and dashes (no readable letters).

Inside, the two kids cheer with joy. The robo-puppy beeps and wiggles excitedly.

Match-cut to a clean hero shot: a real smartphone centered in frame against a
soft dark-blue background. On the screen is the haptic cootie key UI (icons only,
NO readable text).

Soft floating vibration icons or waves appear around the phone.
The feeling is warm, modern, and fun.
""".strip(),
        "reference_filename": "refimg_5.png",
        "reference_instructions": (
            "From Scene 5 (05_pilot_kd0fnr_morse_typewriter.mp4), capture a frame showing "
            "the cartoon cockpit with the red-haired kid, ear-muffs, and glowing fingertips "
            "clearly visible. Save as refimg_5.png."
        ),
    },
]

NAMES = [
    "04_phone_cootie_key_transition",
    "05_pilot_kd0fnr_morse_typewriter",
    "06_starship_boost_and_app_cta",
]


# Make sure you have OPENAI_API_KEY set in your environment.
openai = OpenAI()

def prepare_reference_file(reference_filename: str, size_str: str):
    """
    Load the reference image, resize it to match the requested video size
    (e.g. '720x1280'), save as a PNG temp file, and return an open file handle.

    Returning a real file handle with a .png extension ensures the OpenAI client
    sets the correct mimetype (image/png) instead of application/octet-stream.
    """
    if not os.path.exists(reference_filename):
        print(f"WARNING: reference file {reference_filename} not found.")
        return None

    try:
        # Parse size like "720x1280"
        width_str, height_str = size_str.lower().split("x")
        target_width = int(width_str.strip())
        target_height = int(height_str.strip())
    except Exception as e:
        print(f"WARNING: Could not parse size '{size_str}': {e}")
        return None

    try:
        img = Image.open(reference_filename).convert("RGB")
    except Exception as e:
        print(f"WARNING: Could not open reference image {reference_filename}: {e}")
        return None

    # Resize if needed
    if img.size != (target_width, target_height):
        print(
            f"Resizing reference image {reference_filename} "
            f"from {img.size} to {(target_width, target_height)}"
        )
        img = img.resize((target_width, target_height), Image.LANCZOS)

    # Save to a temporary PNG file on disk so the client sees a proper filename
    ref_path = Path(reference_filename)
    temp_path = ref_path.with_name(ref_path.stem + "_sora_ref.png")

    try:
        img.save(temp_path, format="PNG")
    except Exception as e:
        print(f"WARNING: Could not save resized reference image to {temp_path}: {e}")
        return None

    # Return an open file handle; caller is responsible for closing
    try:
        f = open(temp_path, "rb")
    except Exception as e:
        print(f"WARNING: Could not reopen temp reference image {temp_path}: {e}")
        return None

    return f


def generate_scene(scene, name_index, reference_filename=None):
    """
    Generate one Sora video scene and save it locally.
    Optionally uses a reference image file for continuity via input_reference.
    """
    print(f"\n=== Generating scene: {NAMES[name_index]} ===")

    # Make a shallow copy so we don't mutate the global SCENES entry
    scene_args = dict(scene)

    # Remove metadata keys the Videos API doesn't understand
    scene_args.pop("reference_filename", None)
    scene_args.pop("reference_instructions", None)

    # Optional continuity reference file
    ref_file = None
    if reference_filename:
        size_str = scene_args.get("size", "720x1280")
        print(f"Using input_reference file: {reference_filename}")
        ref_file = prepare_reference_file(reference_filename, size_str)
        if ref_file is not None:
            # Pass the opened PNG/JPEG handle to Sora as input_reference
            scene_args["input_reference"] = ref_file
        else:
            print("Continuing without input_reference due to preparation failure.")

    # Submit the job to Sora-2
    video = openai.videos.create(**scene_args)

    # Close the reference file handle if we opened one
    if ref_file is not None:
        ref_file.close()

    print("Video generation started:", video)

    # Progress bar setup
    bar_length = 30

    # Poll until done
    while video.status in ("in_progress", "queued"):
        video = openai.videos.retrieve(video.id)
        progress = getattr(video, "progress", 0) or 0

        filled_length = int((progress / 100) * bar_length)
        bar = "=" * filled_length + "-" * (bar_length - filled_length)

        status_text = "Queued" if video.status == "queued" else "Processing"
        sys.stdout.write(f"{status_text}: [{bar}] {progress:.1f}%   \r")
        sys.stdout.flush()

        time.sleep(2)

    sys.stdout.write("\n")

    # Handle failure
    if video.status == "failed":
        message = getattr(getattr(video, "error", None), "message", "Video generation failed")
        print(message)
        return None

    print("Video generation completed:", video)
    print("Downloading video content...")

    filename = f"{NAMES[name_index]}.mp4"
    content = openai.videos.download_content(video.id, variant="video")
    content.write_to_file(filename)

    print(f"Wrote {filename}")
    return video.id



def main():
    print("Starting batch generation for all scenes...")

    name_index = 0
    total_scenes = len(SCENES)

    # Check once at startup if we have an optional initial reference for Scene 1
    initial_reference = None
    if os.path.exists(INITIAL_REFERENCE_FILENAME):
        initial_reference = INITIAL_REFERENCE_FILENAME
        print(f"Optional initial reference found: {INITIAL_REFERENCE_FILENAME}")
    else:
        print("No initial reference image found for Scene 1 (refimg_0.png). Proceeding without it.")

    for idx, scene in enumerate(SCENES):
        # Decide which reference file (if any) to use for this scene
        if idx == 0:
            # Scene 1: optional initial reference, no polling
            reference_filename = initial_reference
        else:
            # Scenes 2..N: use the scene's configured continuity reference, with waiting
            reference_filename = scene.get("reference_filename")

            if reference_filename:
                print(f"\nWaiting for continuity reference image: {reference_filename}")
                print("This scene expects an image file to guide visual continuity.")

                instructions = scene.get("reference_instructions")
                if instructions:
                    print("\nReference instructions for this scene:")
                    print(instructions)

                # Poll until the file exists
                while not os.path.exists(reference_filename):
                    sys.stdout.write(
                        f"  ... still waiting for {reference_filename} (press Ctrl+C to abort)\r"
                    )
                    sys.stdout.flush()
                    time.sleep(3)

                print(f"\nFound reference file {reference_filename}. Proceeding with generation.")

        # Generate the current scene
        video_id = generate_scene(scene, name_index, reference_filename=reference_filename)

        if video_id is not None:
            print(f"Scene {idx+1}/{total_scenes} ({NAMES[name_index]}) completed as video id: {video_id}")

        # AFTER generating this scene, tell user what still to grab for the NEXT scene
        if idx < total_scenes - 1:
            next_scene = SCENES[idx + 1]
            next_ref = next_scene.get("reference_filename")
            if next_ref:
                print("\n----------------------------------------")
                print("NEXT STEP: Prepare continuity reference for the next scene.")
                print(f"Please grab a still from {NAMES[idx]}.mp4 and save it as: {next_ref}")
                next_instructions = next_scene.get("reference_instructions")
                if next_instructions:
                    print("\nRecommended frame to grab:")
                    print(next_instructions)
                print("----------------------------------------\n")

        name_index += 1

    print("\nAll scenes complete.")
    print("Generated video files:")
    for name in NAMES:
        print(" -", name + ".mp4")


if __name__ == "__main__":
    main()
