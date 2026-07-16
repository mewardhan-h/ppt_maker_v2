from google import genai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def format_text_with_llm(raw_text):
    """
    Send raw unformatted text to Gemini LLM and get properly formatted output
    that can be converted to PowerPoint by text_to_ppt.py
    """
    
    # Get API key from .env
    API_KEY = os.getenv("GEMINI_API_KEY")
    
    if not API_KEY:
        print("Error: GEMINI_API_KEY not set in .env file")
        print("Please add your API key to the .env file")
        exit(1)
    
    # Create client with API key from .env (same as llm_call.py)
    client = genai.Client(api_key=API_KEY)
    
    # Strict formatting prompt
    prompt = f"""You are a PowerPoint content formatter. Convert the following raw text into a structured format suitable for PowerPoint slides.

STRICT FORMATTING RULES:
1. Use "# Title" for slide titles (one per slide)
2. Use "- Bullet point" for bullet points
3. Use "**text**" for bold text within bullets (e.g., "- **Important:** explanation")
4. For tables, use markdown pipe format:
   | Header 1 | Header 2 | Header 3 |
   |----------|----------|----------|
   | Cell A   | Cell B   | Cell C   |

SLIDE ORGANIZATION RULES:
- First slide: Use the main topic as the title
- Each major section/topic = ONE new slide
- Each slide should have 3-6 bullet points MAXIMUM (NOT MORE THAN 6)
- If a topic has too much content, split it into multiple slides (e.g., "Topic - Part 1", "Topic - Part 2")
- Keep bullet points concise (1-2 lines each)
- Group related information together

STRUCTURE GUIDELINES:
- Identify main topics/sections from the text
- Create a slide for each distinct topic
- Break down long paragraphs into bullet points
- Use bold (**text**) for key terms, names, or emphasis
- If there are comparisons or data, use tables

IMPORTANT:
- Do NOT add any explanations or comments outside the formatted content
- Do NOT add markdown code blocks (no ```)
- Output ONLY the formatted text
- Make sure every slide starts with "# "
- Minimum 5 slides, maximum 20 slides

Raw text to format:

{raw_text}

Now output the formatted text following ALL the rules above:"""

    print("Sending text to Gemini for formatting...")
    print("-" * 60)
    
    # Call Gemini (exactly like llm_call.py)
    interaction = client.interactions.create(
        model="lyria-3-clip-preview",
        input=prompt
    )
    
    # Get output text (exactly like llm_call.py)
    formatted_text = interaction.output_text
    
    print("✅ Formatting complete!")
    print("-" * 60)
    
    return formatted_text.strip()


if __name__ == "__main__":
    import sys
    
    print("\n" + "="*60)
    print("LLM TEXT FORMATTER")
    print("="*60 + "\n")
    
    # Check if input file provided
    if len(sys.argv) < 2:
        print("Usage: python llm_formatter.py <input_text_file.txt>")
        print("\nExample:")
        print("  python llm_formatter.py raw_input.txt")
        print("\nOutput: Will create basic_text_converted.txt")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = "basic_text_converted.txt"
    
    # Check if input file exists
    if not os.path.isfile(input_file):
        print(f"❌ Error: Input file '{input_file}' not found")
        sys.exit(1)
    
    # Read input file
    print(f"📄 Reading input file: {input_file}")
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            raw_text = f.read()
        print(f"✅ Read {len(raw_text)} characters\n")
    except Exception as e:
        print(f"❌ Error reading file: {e}")
        sys.exit(1)
    
    # Format with LLM
    print("🤖 Formatting text with Gemini LLM...")
    try:
        formatted_text = format_text_with_llm(raw_text)
    except Exception as e:
        print(f"\n❌ Error formatting text: {e}")
        sys.exit(1)
    
    # Save output
    print(f"\n💾 Saving formatted text to: {output_file}")
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(formatted_text)
        print(f"✅ Successfully saved {len(formatted_text)} characters")
    except Exception as e:
        print(f"❌ Error saving file: {e}")
        sys.exit(1)
    
    print("\n" + "="*60)
    print("✅ SUCCESS! Formatted text saved to basic_text_converted.txt")
    print("="*60)
    print("\nNext step: Run 'python text_to_ppt.py' to generate PowerPoint\n")
