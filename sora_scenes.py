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
import os
import time
import sys
from pathlib import Path
import json

from openai import OpenAI

# Directory to save all generated clips
OUTPUT_DIR = Path("sora_haptic_sidetone_scenes")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

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

SCENES = [
    # 1) Hook: narrator + frustrated headphone operator
    {
        "model": "sora-2",
        "seconds": "8",
        "size": "720x1280",
        "prompt": f"""
{CONTEXT}

[SCENE 1 — HOOK: SIDETONE MISERY]

Vertical 6:19 / 9:16 smartphone video.

We’re in a modern ham radio shack at a small desk.
A ham operator, wearing over-ear wireless headphones, is trying to send Morse code
with a paddle or cootie key. We see a close-up of the hand keying on the desk,
and the operator’s face reacting.

The sidetone in their headphones is obviously delayed: their finger taps are in-time,
but the audible beeps come a fraction of a second late, creating an annoying echo.

Camera: handheld close-up on the key and the operator’s frustrated face,
subtle focus pulls.

On-screen text at top:
“Have problems with transmit sidetone delay in your wireless headphones?”

Voiceover narrator (clear, friendly tone):
“Have problems with transmit sidetone delay in your wireless headphones? Who doesn’t?”

At the end of the shot, the operator winces and clutches the headphones in frustration
as the echoing sidetone continues.
""".strip(),
        "referenced_video_ids": []
    },

    # 2) Starfighter pilot freaking out about sidetone delay
    {
        "model": "sora-2",
        "seconds": "8",
        "size": "720x1280",
        "prompt": f"""
{CONTEXT}

[SCENE 2 — STARFIGHTER FREAKOUT]

Vertical 6:19 / 9:16. Inside a small, cramped retro-futuristic starfighter cockpit,
clearly inspired by classic space dogfight movies but with no specific franchise logos.

The same pilot character is now flying a sci-fi fighter. Outside the canopy,
we see stylized enemy ships and stars streaking by.

The pilot wears a sci-fi flight helmet with built-in wireless audio.
We hear delayed Morse sidetone echoing in their ears as they try to key
on an in-cockpit Morse control.

Camera: medium close-up on the pilot, cockpit shaking slightly from turbulence.

The pilot shouts in frustration:
“Damn it, I can’t transmit with this sidetone delay!”

They rip off their helmet dramatically, revealing the same face as in the other scenes,
hair slightly mussed, clearly exasperated.
""".strip(),
        "referenced_video_ids": []  # optionally fill with [id_of_scene_1]
    },

    # 3) Mentor voice + ear muffs + glowing fingers “Use the haptics”
    {
        "model": "sora-2",
        "seconds": "8",
        "size": "720x1280",
        "prompt": f"""
{CONTEXT}

[SCENE 3 — MENTOR VOICE: USE THE HAPTICS]

Vertical 6:19 / 9:16. Same cockpit, same pilot, helmet now off.

The chaotic battle noise ducks down slightly. The pilot looks around, a bit desperate.

A calm, distant mentor voice (Obi-Wan-like, but generic and unnamed) echoes gently:
“Close your ears… Open your fingers to the code… Use the haptics.”

As the voice says “Close your ears…”, a pair of soft, padded ear muffs
materialize over the pilot’s ears from thin air, with a gentle magical glow.
All external sound becomes muffled, like real ear protection.

As the voice says “Open your fingers to the code… Use the haptics,”
we see a subtle glow tracing around the pilot’s fingers on the control stick,
as if a new sense is awakening in their fingertips.

Camera: slow push-in on the pilot’s face as they go from frustrated
to focused and curious.
""".strip(),
        "referenced_video_ids": []  # optionally [id_of_scene_2]
    },

    # 4) Peel to phone-based Project Toucans cootie key & haptic sidetone mode
    {
        "model": "sora-2",
        "seconds": "8",
        "size": "720x1280",
        "prompt": f"""
{CONTEXT}

[SCENE 4 — PEEL TRANSITION TO PHONE COOTIE KEY]

Vertical 6:19 / 9:16.

We start tight on the pilot’s glowing fingers in the cockpit.
As they move slightly, the entire sci-fi cockpit scene peels away
like a translucent sticker, revealing a real-world desk underneath.

Underneath is a smartphone lying flat on a desk, running the
Project Toucans phone-based cootie key app.

Close-up macro shot: a finger floating just above a large horizontal “key bar”
UI on the screen, rocking gently side to side in cootie-key fashion.
Each tap triggers a subtle screen animation and a sense of haptic feedback.

The phone screen shows a small, clear label:
“HAPTIC SIDETONE MODE: ON” near the top corner.

We do NOT show any trademarked logos, just clean, simple branding
with the text “Project Toucans” subtly near the bottom.

We hear soft, bassy, tactile “thunk” haptic sounds rather than beeping sidetone.

On-screen text at bottom:
“Just turn audio sidetone off… and FEEL the code.”

Voiceover narrator:
“Just turn your audio transmit sidetone off… and feel the code with the app’s haptic sidetone mode.”
""".strip(),
        "referenced_video_ids": []  # optionally [id_of_previous_scene]
    },

    # 5) Back to cockpit, KD0FNR in Morse, typewriter font
    {
        "model": "sora-2",
        "seconds": "8",
        "size": "720x1280",
        "prompt": f"""
{CONTEXT}

[SCENE 5 — PILOT SENDING KD0FNR IN MORSE]

Vertical 6:19 / 9:16. Back in the same starfighter cockpit.

The pilot now sits calmly, eyes closed, ear muffs still on.
No more echo or delay. Their hand rests on an invisible haptic key
in front of them, rocking gently side to side as they send Morse.

We now hear clean, perfectly timed Morse beeps (no delay),
spelling the ham callsign KD0FNR.

As each character is sent, the letters appear center-screen, one by one,
in a vintage typewriter font, as if typed across the cockpit view:
“K D 0 F N R”.

Camera: slow orbit around the pilot, showing starlight and HUD reflections
on the canopy, conveying control and confidence.

Mood: triumphant, nerdy, precise.
""".strip(),
        "referenced_video_ids": []  # optionally [id_of_scene_4]
    },

    # 6) Boost away + app CTA
    {
        "model": "sora-2",
        "seconds": "8",
        "size": "720x1280",
        "prompt": f"""
{CONTEXT}

[SCENE 6 — STARSHIP BOOST & APP CTA]

Vertical 6:19 / 9:16.

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
        "referenced_video_ids": []  # optionally [id_of_scene_5]
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

def generate_scene(scene, name_index):
    """Generate one Sora video scene and save it locally.
       Returns the video.id so you *could* track continuity, even though
       we can't pass it back into videos.create() right now.
    """
    print(f"\n=== Generating scene: {NAMES[name_index]} ===")

    # Make a shallow copy so we don't mutate the original scene
    scene_args = dict(scene)

    # SAFETY: remove any keys that the Videos API doesn't understand
    # (like 'referenced_video_ids' which is NOT currently supported)
    scene_args.pop("referenced_video_ids", None)

    # Submit the job
    video = openai.videos.create(**scene_args)
    print("Video generation started:", video)

    # Progress bar setup
    bar_length = 30

    # Poll until done
    while video.status in ("in_progress", "queued"):
        # Fetch updated status
        video = openai.videos.retrieve(video.id)
        progress = getattr(video, "progress", 0) or 0

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
        return None

    print("Video generation completed:", video)
    print("Downloading video content...")

    filename = f"{NAMES[name_index]}.mp4"

    # Download the final video
    content = openai.videos.download_content(video.id, variant="video")
    content.write_to_file(filename)

    print(f"Wrote {filename}")

    # Return the video id (for your own tracking, logging, etc.)
    return video.id


def main():
    print("Starting batch generation for all scenes...")

    prev_video_id = None  # you can still log this for yourself
    name_index = 0

    for scene in SCENES:
        # If you *want* to keep track of continuity yourself, you can store
        # prev_video_id somewhere or print it, but we won't send it to the API.
        video_id = generate_scene(scene, name_index)

        if video_id is not None:
            prev_video_id = video_id
            print(f"Scene {NAMES[name_index]} completed as video id: {video_id}")

        name_index += 1

    print("\nAll scenes complete.")
    print("Generated video files:")
    for name in NAMES:
        print(" -", name + ".mp4")


if __name__ == "__main__":
    main()
