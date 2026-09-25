import json
import re
import base64

log_path = "/Users/admin/.gemini/antigravity-ide/brain/1c8288cf-b19c-4615-9cdf-99047682d019/.system_generated/logs/transcript.jsonl"

with open(log_path, 'r') as f:
    lines = f.readlines()

print(f"Total lines in log: {len(lines)}")

# Let's inspect all lines
for i in range(len(lines)):
    try:
        step = json.loads(lines[i])
        print(f"Line {i}: step_index={step.get('step_index')}, type={step.get('type')}, source={step.get('source')}")
        # Search for base64 pattern or data:image
        step_str = json.dumps(step)
        matches = re.findall(r'data:image/[a-zA-Z]+;base64,[a-zA-Z0-9+/=]+', step_str)
        if matches:
            print(f"Found {len(matches)} data:image URIs on line {i}")
            for idx, match in enumerate(matches):
                print(f"  Match {idx}: length={len(match)}")
                # Extract base64 part
                base64_data = match.split(',')[1]
                img_data = base64.b64decode(base64_data)
                out_path = f"assets/images/extracted_icon_{idx}.png"
                with open(out_path, 'wb') as img_f:
                    img_f.write(img_data)
                print(f"  Saved to {out_path}")
    except Exception as e:
        print(f"Error parsing line {i}: {e}")
