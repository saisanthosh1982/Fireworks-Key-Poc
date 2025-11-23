import os
import json
from extract import extract_text
from parse import parse_fields

OUTPUT_DIR = "outputs"

os.makedirs(OUTPUT_DIR, exist_ok=True)

def process(file_path):
    print(f"📄 Processing image: {file_path}")
    
    raw_text = extract_text(file_path)
    print("\n🔍 OCR Result:\n", raw_text)

    structured = parse_fields(raw_text)
    print("\n📦 Structured Output:\n", structured)

    # Normalize output filename
    filename = os.path.basename(file_path).split('.')[0] + ".json"
    output_path = os.path.join(OUTPUT_DIR, filename)

    # Convert structured output to clean JSON (remove markdown fences if present)
    cleaned = structured.replace("```", "").strip()

    # Attempt to load JSON safely
    try:
        data = json.loads(cleaned)
    except json.JSONDecodeError:
        # If format isn't perfect, wrap as raw text
        data = {"raw_output": cleaned}

    # Write final output
    with open(output_path, "w") as f:
        json.dump(data, f, indent=2)

    print(f"💾 Saved output to: {output_path}")

if __name__ == "__main__":
    samples_folder = "samples"

    image_files = [f for f in os.listdir(samples_folder) if f.lower().endswith(("jpg", "jpeg", "png"))]

    print("📁 Files detected:", image_files)

    for file in image_files:
        file_path = os.path.join(samples_folder, file)
        print("\n==============================")
        print(f"➡️ Processing: {file}")
        process(file_path)
        print("==============================")

