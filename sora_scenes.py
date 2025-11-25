import os
import time
import sys
from pathlib import Path
import json

import requests
from openai import OpenAI

# Directory to save all generated clips
OUTPUT_DIR = Path("sora_gladych_psyops_scenes")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# All the Sora prompts we defined for the short
SCENES = [
    {
        "model": "sora-2",
        "seconds": '8',
        "size": "720x1280",
        "prompt": (
            "Dynamic animated title card: ‘PsyOps’ in bold stencil lettering, "
            "glitch effects, cold-war aesthetic, subtle static noise, dark blue and "
            "black color palette, documentary style, 9:16."
        ),
    },
    {
        "model": "sora-2",
        "seconds": '8',
        "size": "720x1280",
        "prompt": (
            "Archival-style recreation of 1950s CIA research room, dim lighting, "
            "mid-century files and typewriters, blurred silhouettes of agents, a folder "
            "labeled ‘ARTICHOKE’ sliding across a desk, 16mm film look, no identifiable faces."
        ),
    },
    {
        "model": "sora-2",
        "seconds": '8',
        "size": "720x1280",
        "prompt": (
            "1950s Okinawa military airbase, wide establishing shot, drafting tables with "
            "blueprints, two architects reviewing plans, humid tropical light, U.S. signage, "
            "realistic but non-identifiable faces."
        ),
    },
    {
        "model": "sora-2",
        "seconds": '8',
        "size": "720x1280",
        "prompt": (
            "1960s U.S. military PsyOps radio room, reel-to-reel players, headphones, "
            "operators preparing leaflets and broadcast scripts, green fluorescent lighting, "
            "handheld documentary feel."
        ),
    },
    {
        "model": "sora-2",
        "seconds": '8',
        "size": "720x1280",
        "prompt": (
            "Cinematic slow zoom on the J. Edgar Hoover FBI Building in Washington D.C., "
            "golden-hour lighting, dramatic angle from street level, crisp realism, high detail, "
            "4K look, 24fps."
        ),
    },
    {
        "model": "sora-2",
        "seconds": '8',
        "size": "720x1280",
        "prompt": (
            "Hoover Building at night, moody blue lighting, faint fog, a single window glowing, "
            "subtle lens flare, paranormal ambience, camera slowly tilts upward, rain-soaked "
            "pavement reflections."
        ),
    },
    {
        "model": "sora-2",
        "seconds": '8',
        "size": "720x1280",
        "prompt": (
            "Silhouettes of two FBI agents walking into a modernist federal building at dusk, "
            "no faces visible, long shadows, trench coat outlines, cinematic noir style, slight grain."
        ),
    },
    {
        "model": "sora-2",
        "seconds": '8',
        "size": "720x1280",
        "prompt": (
            "Animated conspiracy-board graphic connecting nodes: CIA, PsyOps, Okinawa, FBI Building, "
            "X-Files, antigravity articles, red string links, parchment background, smooth camera drift."
        ),
    },
    {
        "model": "sora-2",
        "seconds": '8',
        "size": "720x1280",
        "prompt": (
            "Animated title card: ‘THE GLADYCH FILES’ appears in glowing serif lettering, soft paranormal "
            "light rays, dark void background, subtle static and glitch."
        ),
    },
]


NAMES=["01_whyfiles_psyops_title",
        "02_project_artichoke_room",
        "03_okinawa_1955_base_design",
        "04_vietnam_era_psyops_room",
        "05_hoover_building_hero_shot",
        "06_hoover_building_night_paranormal",
        "07_mulder_scully_silhouettes",
        "08_conspiracy_board_gladych_web",
        "09_gladych_files_outro_card"]


# Make sure you have OPENAI_API_KEY set in your environment.
openai = OpenAI()

def generate_scene(scene, name_index):
    """Generate one Sora video scene and save it locally."""
    print(f"\n=== Generating scene: {NAMES[name_index]} ===")

    # Submit the job
    video = openai.videos.create(**scene)
    print("Video generation started:", video)

    # Progress bar setup
    bar_length = 30

    # Poll until done
    while video.status in ("in_progress", "queued"):
        # Fetch updated status
        video = openai.videos.retrieve(video.id)
        progress = getattr(video, "progress", 0)

        filled_length = int((progress / 100) * bar_length)
        bar = "=" * filled_length + "-" * (bar_length - filled_length)

        status_text = "Queued" if video.status == "queued" else "Processing"
        sys.stdout.write(f"{status_text}: [{bar}] {progress:.1f}%   \r")
        sys.stdout.flush()

        time.sleep(2)

    # Finish progress output
    sys.stdout.write("\n")

    # Check failure
    if video.status == "failed":
        message = getattr(getattr(video, "error", None), "message", "Video generation failed")
        print(message)
        return

    print("Video generation completed:", video)
    print("Downloading video content...")

    # Custom filename using scene name
    filename = f"{NAMES[name_index]}.mp4"

    # Download the final video
    content = openai.videos.download_content(video.id, variant="video")
    content.write_to_file(filename)

    print(f"Wrote {filename}")


def main():
    print("Starting batch generation for all scenes...")
    name_index = 0
    for scene in SCENES:
        generate_scene(scene, name_index)
        name_index = name_index + 1

    print("\nAll scenes complete.")
    print("Generated video files:")
    for name in NAMES:
        print(" -", name + ".mp4")

if __name__ == "__main__":
    main()
