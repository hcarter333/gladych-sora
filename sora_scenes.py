import os
import time
import sys
from pathlib import Path
import json
from PIL import Image

import requests
from openai import OpenAI

# Directory to save all generated clips
OUTPUT_DIR = Path("sora_gladych_cwhaptics_scenes")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# All the Sora prompts we defined for the short

openai = OpenAI()

# Shared continuity context for all scenes
CONTEXT = """
[CONTEXT — SAME SHORT FILM]
This clip is part of the same unified sci-fi ham-radio promo short about
a phone-based Morse code key with haptic sidetone.

Keep the visual style, color palette, and character designs consistent
across all shots.

Pilot:
- mid-30s, short brown hair
- orange retro-futuristic flight suit
- same face, same proportions every time

Starfighter cockpit:
- retro-futuristic analog-meets-holographic design
- lots of physical switches and metal, plus a few floating HUD elements

Overall look:
- vertical smartphone video (6:19 / 9:16 style)
- cinematic, slightly stylized realism
- rich contrast, cool sci-fi blues with warm orange highlights
"""

CONTEXT = """
[CONTEXT — SAME SHORT FILM]
This clip is part of a single unified sci-fi ham-radio promo short
about a phone-based Morse code key with haptic sidetone.

Keep these elements CONSISTENT across scenes:
- Same pilot character:
  - mid-30s, short brown hair
  - orange retro-futuristic flight suit
  - same face, same proportions, same general expression style
- Same starfighter cockpit:
  - retro-futuristic analog-meets-holographic design
  - physical switches, metal panels, plus a few floating HUD elements
- Overall look:
  - vertical smartphone video (6:19 / 9:16 style)
  - cinematic, slightly stylized realism
  - rich contrast, cool sci-fi blues with warm orange highlights
"""

SCENES = [
    # SCENE 1 — no reference image
    {
        "model": "sora-2",
        "seconds": "8",
        "size": "720x1280",
        "prompt": f"""
{CONTEXT}

[SCENE 1 — HOOK: SIDETONE MISERY, NO REFERENCE IMAGE]

Vertical 6:19 / 9:16 smartphone video.

We’re in a modern ham radio shack at a small desk.
A ham operator (this is the same person who will become the starfighter pilot later),
wearing over-ear wireless headphones, is trying to send Morse code
with a paddle or cootie key.

Close-up: their hand keying on the desk and their face reacting.
The sidetone in their headphones is obviously delayed: finger taps are in-time,
but the audible beeps come a fraction of a second late, creating an annoying echo.

Camera: handheld close-ups on the key and the operator’s frustrated face,
with subtle focus pulls.

On-screen text at top:
“Have problems with transmit sidetone delay in your wireless headphones?”

Voiceover narrator (clear, friendly):
“Have problems with transmit sidetone delay in your wireless headphones? Who doesn’t?”

At the end of the shot, the operator winces and grabs the headphones
in frustration as the echoing sidetone continues.
""".strip(),
        # no reference for scene 1
    },

    # SCENE 2 — uses refimg_1.png from Scene 1
    {
        "model": "sora-2",
        "seconds": "8",
        "size": "720x1280",
        "prompt": f"""
{CONTEXT}

[SCENE 2 — STARFIGHTER FREAKOUT, USE REFERENCE IMAGE FROM SCENE 1]

Vertical 6:19 / 9:16.

A retro-futuristic starfighter cockpit in space, inspired by classic space dogfight movies
but with no specific franchise logos.

This is the SAME character as in Scene 1, now as a sci-fi pilot.

A reference still image from Scene 1 is provided.
Use the reference image to MATCH:
- the pilot’s face and hair
- overall color palette and lighting mood
- the sense that this is the same person in a different environment

The pilot sits in a cramped cockpit. Outside the canopy we see stylized enemy ships
and starfields.

The pilot wears a sci-fi flight helmet with built-in wireless audio.
We hear delayed Morse sidetone echoing in their ears while they try to key
on an in-cockpit Morse control.

Camera: medium close-up on the pilot, cockpit shaking slightly from turbulence.

The pilot shouts in frustration:
“Damn it, I can’t transmit with this sidetone delay!”

They rip off their helmet dramatically, revealing the same face as the ham operator
from Scene 1, hair slightly mussed, clearly exasperated.
""".strip(),
        "reference_filename": "refimg_1.png",
        "reference_instructions": (
            "From Scene 1 (01_haptic_sidetone_hook_operator.mp4), capture a frame where the "
            "operator’s full face is clearly visible with the wireless headphones on. "
            "Good lighting on eyes and hair; a mid-close shot that establishes their look."
        ),
    },

    # SCENE 3 — uses refimg_2.png from Scene 2
    {
        "model": "sora-2",
        "seconds": "8",
        "size": "720x1280",
        "prompt": f"""
{CONTEXT}

[SCENE 3 — MENTOR VOICE: USE THE HAPTICS, USE REFERENCE IMAGE FROM SCENE 2]

Vertical 6:19 / 9:16. Same starfighter cockpit, same pilot.

A reference still image from Scene 2 is provided.
Use the reference image to MATCH:
- cockpit layout, materials, and color
- pilot’s flight suit and facial features
- lighting direction and palette

The chaotic battle noise ducks down slightly.
The pilot looks around, a bit desperate but now helmet-off.

A calm, distant mentor voice (Obi-Wan-like, but generic and unnamed) echoes gently:
“Close your ears… Open your fingers to the code… Use the haptics.”

As the voice says “Close your ears…”, a pair of soft, padded ear muffs
materialize over the pilot’s ears from thin air with a gentle magical glow.
All external sound becomes muffled, like real ear protection.

As the voice says “Open your fingers to the code… Use the haptics,”
we see a subtle glow tracing around the pilot’s fingers on the control stick,
as if a new sense is awakening in their fingertips.

Camera: slow push-in on the pilot’s face as they move from frustration
to calm focus and curiosity.
""".strip(),
        "reference_filename": "refimg_2.png",
        "reference_instructions": (
            "From Scene 2 (02_starfighter_pilot_sidetone_delay.mp4), grab a frame right after "
            "the helmet comes off where the pilot’s full face, suit, and cockpit background are "
            "clearly visible. Emphasize face, suit color, and the metal panels behind them."
        ),
    },

    # SCENE 4 — uses refimg_3.png from Scene 3
    {
        "model": "sora-2",
        "seconds": "8",
        "size": "720x1280",
        "prompt": f"""
{CONTEXT}

[SCENE 4 — PEEL TRANSITION TO PHONE COOTIE KEY, USE REFERENCE IMAGE FROM SCENE 3]

Vertical 6:19 / 9:16.

We start tight on the pilot’s glowing fingers in the cockpit.

A reference still image from Scene 3 is provided.
Use the reference image to MATCH:
- finger position and glow style
- general cockpit color tones
- the feel that we are continuing directly from the previous shot

As the glowing fingers move slightly, the entire sci-fi cockpit scene PEELS AWAY
like a translucent sticker, revealing a real-world desk underneath.

Underneath is a smartphone lying flat on a desk, running the
Project Toucans phone-based cootie key app.

Close-up macro shot: a finger floating just above a large horizontal “key bar”
UI on the screen, rocking gently side to side in cootie-key fashion.
Each tap triggers a subtle screen animation and an implied haptic vibration.

The phone screen shows a small, clear label:
“HAPTIC SIDETONE MODE: ON” near the top corner.

Show simple text “Project Toucans” near the bottom as branding,
but no existing copyrighted logos.

We hear soft, bassy, tactile “thunk” haptic sounds rather than loud beeps.

On-screen text at bottom:
“Just turn audio sidetone off… and FEEL the code.”

Voiceover narrator:
“Just turn your audio transmit sidetone off… and feel the code with the app’s haptic sidetone mode.”
""".strip(),
        "reference_filename": "refimg_3.png",
        "reference_instructions": (
            "From Scene 3 (03_mentor_voice_use_the_haptics.mp4), capture a close shot where the "
            "ear muffs and glowing fingers on the control stick are visible together. The glow, "
            "hand pose, and cockpit color are what matter most."
        ),
    },

    # SCENE 5 — uses refimg_4.png from Scene 4
    {
        "model": "sora-2",
        "seconds": "8",
        "size": "720x1280",
        "prompt": f"""
{CONTEXT}

[SCENE 5 — PILOT SENDING KD0FNR IN MORSE, USE REFERENCE IMAGE FROM SCENE 4]

Vertical 6:19 / 9:16. Back in the same starfighter cockpit.

A reference still image from Scene 4 is provided.
Use the reference image to MATCH:
- the look of the hand and finger position from the phone cootie key
- overall color palette and lighting vibe
- the sense that the pilot’s “haptic” sense is now integrated into the cockpit

The pilot now sits calmly, eyes closed, ear muffs still on.
No more echo or delay. Their hand rests on an invisible haptic key
in front of them, rocking gently side to side as they send Morse.

We hear clean, perfectly timed Morse beeps (no delay),
spelling the callsign KD0FNR.

As each character is sent, letters appear center-screen, one by one,
in a vintage typewriter font, as if typed across the cockpit view:
“K D 0 F N R”.

Camera: slow orbit around the pilot, showing starlight and HUD reflections
on the canopy, conveying control and confidence.

Mood: triumphant, nerdy, precise.
""".strip(),
        "reference_filename": "refimg_4.png",
        "reference_instructions": (
            "From Scene 4 (04_phone_cootie_key_transition.mp4), grab a macro shot where a single "
            "finger is clearly hovering over or touching the horizontal cootie key bar, with the "
            "phone edges and key bar shape visible. The haptic gesture and UI bar are key."
        ),
    },

    # SCENE 6 — uses refimg_5.png from Scene 5
    {
        "model": "sora-2",
        "seconds": "8",
        "size": "720x1280",
        "prompt": f"""
{CONTEXT}

[SCENE 6 — STARSHIP BOOST & APP CTA, USE REFERENCE IMAGE FROM SCENE 5]

Vertical 6:19 / 9:16.

A reference still image from Scene 5 is provided.
Use the reference image to MATCH:
- starfighter design
- pilot suit colors and overall color palette

Exterior shot in space of the same starfighter seen before.

The ship suddenly accelerates up and away past the camera
with a dramatic burst of light, leaving behind a short trail of glowing
dots and dashes, like stylized Morse code, to suggest speed and perfect timing.

Cut briefly to inside the cockpit: the pilot throws a fist in the air
and shouts joyfully:
“Whoooo, oh yeah!”

Match cut to a clean dark-blue or black background.

Centered on screen:
- A 3D smartphone mockup showing the Project Toucans phone-based cootie key UI
  with “Haptic Sidetone Mode: ON” clearly visible.
- App title text: “Project Toucans Haptic Sidetone”
- Tagline text underneath:
  “Send better code on wireless headphones. No sidetone delay. Just haptics.”
- At the very bottom, small CTA text:
  “Learn more at projecttoucans.com”

Subtle animation:
- A small haptic vibration icon near the phone pulses gently.
- Very faint, repeating KD0FNR in Morse (dots and dashes) as a background pattern.
""".strip(),
        "reference_filename": "refimg_5.png",
        "reference_instructions": (
            "From Scene 5 (05_pilot_kd0fnr_morse_typewriter.mp4), capture a frame where the pilot "
            "is calm in the cockpit with ear muffs visible and some stars / HUD elements reflected "
            "on the canopy. Suit color and cockpit metal should be clear."
        ),
    },
]

NAMES = [
    "01_haptic_sidetone_hook_operator",
    "02_starfighter_pilot_sidetone_delay",
    "03_mentor_voice_use_the_haptics",
    "04_phone_cootie_key_transition",
    "05_pilot_kd0fnr_morse_typewriter",
    "06_starship_boost_and_app_cta",
]


# Make sure you have OPENAI_API_KEY set in your environment.
openai = OpenAI()

def prepare_reference_file(reference_filename: str, size_str: str):
    """
    Load the reference image, resize it to match the requested video size
    (e.g. '720x1280'), and return a file-like object suitable for input_reference.
    Returns None if anything goes wrong.
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

    # Put into an in-memory buffer as PNG
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)

    # Return the buffer; OpenAI client can treat this as a file-like for upload
    return buf



def generate_scene(scene, name_index, reference_filename=None):
    """Generate one Sora video scene and save it locally.
       Optionally uses a reference image file for continuity.
    """
    print(f"\n=== Generating scene: {NAMES[name_index]} ===")

    # Make a shallow copy so we don't mutate global SCENES
    scene_args = dict(scene)

    # Remove metadata keys the Videos API doesn't understand
    scene_args.pop("reference_filename", None)
    scene_args.pop("reference_instructions", None)

    # Prepare input_reference if requested
    ref_buffer = None
    if reference_filename:
        size_str = scene_args.get("size", "720x1280")
        print(f"Using input_reference file: {reference_filename}")
        ref_buffer = prepare_reference_file(reference_filename, size_str)
        if ref_buffer is not None:
            scene_args["input_reference"] = ref_buffer
        else:
            print("Continuing without input_reference due to preparation failure.")

    # Submit the job
    video = openai.videos.create(**scene_args)
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

    for idx, scene in enumerate(SCENES):
        # If this scene requires a continuity reference image, wait for it
        reference_filename = scene.get("reference_filename")

        if reference_filename:
            print(f"\nWaiting for continuity reference image: {reference_filename}")
            print("This scene expects an image file to guide visual continuity.")

            # Print the instructions again for convenience
            instructions = scene.get("reference_instructions")
            if instructions:
                print("\nReference instructions for this scene:")
                print(instructions)

            # Poll until the file exists
            while not os.path.exists(reference_filename):
                sys.stdout.write(f"  ... still waiting for {reference_filename} (press Ctrl+C to abort)\r")
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
                print(f"NEXT STEP: Prepare continuity reference for the next scene.")
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
