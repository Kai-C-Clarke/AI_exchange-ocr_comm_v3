import re
import logging
from difflib import SequenceMatcher

GARBAGE_PATTERNS = [
    r"tm arrect", r"Mmilgrnet", r"SBnvthing", r"VFpwer", r"KRek", r"MOwWw", r"eke",
    r"OG PWS By", r"Acknowledged", r"^\[\d{2}:\d{2}:\d{2}\]$"  # Added timestamp pattern
]

def similarity_ratio(a, b):
    """Calculate similarity between two strings."""
    return SequenceMatcher(None, a.lower().strip(), b.lower().strip()).ratio()

def extract_newest_content(text_blocks):
    """Extract the most recent, unique content from text blocks."""
    if not text_blocks:
        return ""
    
    # Look for the most recent timestamp pattern
    timestamp_pattern = r'\[(\d{2}:\d{2}:\d{2})\]'
    
    # Find all timestamped content
    timestamped_content = []
    for block in text_blocks:
        matches = re.finditer(timestamp_pattern, block)
        for match in matches:
            timestamp = match.group(1)
            # Extract content after this timestamp
            start_pos = match.end()
            # Find next timestamp or end of string
            next_match = re.search(timestamp_pattern, block[start_pos:])
            if next_match:
                content = block[start_pos:start_pos + next_match.start()].strip()
            else:
                content = block[start_pos:].strip()
            
            if content and not any(re.search(pat, content, re.IGNORECASE) for pat in GARBAGE_PATTERNS):
                timestamped_content.append((timestamp, content))
    
    if timestamped_content:
        # Sort by timestamp and get most recent
        timestamped_content.sort(key=lambda x: x[0])
        latest_content = timestamped_content[-1][1]
        logging.info(f"🕐 Extracted latest timestamped content: '{latest_content[:50]}...'")
        return latest_content
    
    # Fallback: return the longest unique block
    unique_blocks = []
    for block in text_blocks:
        cleaned = clean_single_block(block)
        if cleaned and not any(similarity_ratio(cleaned, existing) > 0.8 for existing in unique_blocks):
            unique_blocks.append(cleaned)
    
    if unique_blocks:
        # Return the longest block (likely most complete)
        result = max(unique_blocks, key=len)
        logging.info(f"📝 Extracted longest unique block: '{result[:50]}...'")
        return result
    
    return ""

def clean_single_block(text: str) -> str:
    """Clean a single text block."""
    if not text:
        return ""
    
    # Remove obvious garbage patterns
    for pattern in GARBAGE_PATTERNS:
        text = re.sub(pattern, "", text, flags=re.IGNORECASE)
    
    # Remove repeated phrases (like "OG PWS By" repetitions)
    lines = text.split('\n')
    cleaned_lines = []
    seen_lines = set()
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        # Skip if we've seen this exact line before
        if line in seen_lines:
            continue
            
        # Skip if it's very similar to a line we've already seen
        if any(similarity_ratio(line, seen_line) > 0.9 for seen_line in seen_lines):
            continue
            
        seen_lines.add(line)
        cleaned_lines.append(line)
    
    result = ' '.join(cleaned_lines)
    
    # Remove timestamps from the final result (keep content only)
    result = re.sub(r'\[\d{2}:\d{2}:\d{2}\]\s*', '', result)
    
    return result.strip()

def clean_ocr_output(text: str) -> str:
    """Main cleaning function - now just cleans a single block."""
    return clean_single_block(text)

def process_multiple_frames(text_blocks: list) -> str:
    """Process multiple OCR frames and extract the best content."""
    if not text_blocks:
        return "[No readable text]"
    
    logging.info(f"🔍 Processing {len(text_blocks)} OCR frames...")
    
    # Log what we received for debugging
    for i, block in enumerate(text_blocks):
        logging.info(f"Frame {i}: '{block[:60]}...'")
    
    # First, try to extract newest timestamped content
    result = extract_newest_content(text_blocks)
    
    if not result:
        # Fallback: clean and deduplicate all blocks
        all_text = ' '.join(text_blocks)
        result = clean_single_block(all_text)
    
    if not result:
        return "[No readable text after filtering]"
    
    # Final cleanup
    result = result.strip()
    
    # Remove any remaining repetitive patterns
    words = result.split()
    if len(words) > 10:
        # Check for repetitive sequences
        unique_words = []
        for word in words:
            if len(unique_words) < 3 or word not in unique_words[-3:]:
                unique_words.append(word)
        result = ' '.join(unique_words)
    
    logging.info(f"✅ Final cleaned result: '{result}'")
    return result