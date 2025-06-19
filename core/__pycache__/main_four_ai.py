import time
import logging
from utils import inject_prompt_clipboard, wait_for_ai_response
from ocr_engine import scroll_and_capture
from config import UI_CONFIGS, CONVERSATION_FLOW
from window_manager import safe_click_area, switch_to_desktop
from reflection_logger import save_reflection

logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(message)s')

def run_four_ai_loop():
    prompt = "Hello. Let's begin the discourse loop. Reflect briefly and pass it on."
    loop_count = 0

    while True:
        loop_count += 1
        logging.info(f"🌐 Starting loop #{loop_count}")

        for speaker, receiver in CONVERSATION_FLOW["four_ai"]:
            logging.info(f"🎙️ {speaker} → {receiver}")

            # Focus on speaker's UI
            safe_click_area(speaker)
            time.sleep(1)

            # Inject prompt into speaker
            success = inject_prompt_clipboard(prompt, speaker)
            if not success:
                logging.warning(f"❌ Failed to inject prompt into {speaker}. Skipping...")
                continue

            wait_for_ai_response(speaker)

            # Read speaker's response
            response, frames, reason = scroll_and_capture(speaker)
            if not response:
                logging.warning(f"⚠️ No response from {speaker}. Skipping...")
                continue

            # Save reflection
            save_reflection(response, prompt, frames, reason, speaker)

            # Prepare response as next prompt
            prompt = response
            time.sleep(1)

        # Optional: break loop after one full circuit for testing
        # break

if __name__ == "__main__":
    logging.info("🚀 Four-AI loop initializing...")
    run_four_ai_loop()
