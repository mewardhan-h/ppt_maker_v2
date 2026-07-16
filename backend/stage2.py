"""
Stage 2: Strict Formatting with NVIDIA LLM
Takes raw content from Stage 1 and formats it strictly for PPT conversion
"""

from openai import OpenAI
import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Color codes for terminal output
USE_COLOR = sys.stdout.isatty() and os.getenv("NO_COLOR") is None
REASONING_COLOR = "\033[90m" if USE_COLOR else ""
RESET_COLOR = "\033[0m" if USE_COLOR else ""


def format_with_strict_rules(raw_content):
    """
    Format raw content with strict PPT structure rules using NVIDIA LLM
    
    Args:
        raw_content (str): Raw educational content from Stage 1
    
    Returns:
        str: Strictly formatted content with # titles, - bullets, **bold**
    """
    
    # Get NVIDIA API key
    nvidia_api_key = os.getenv("NVIDIA_API_KEY")
    
    if not nvidia_api_key:
        raise Exception("NVIDIA_API_KEY not set in .env file")
    
    # Initialize OpenAI client with NVIDIA endpoint
    try:
        client = OpenAI(
            base_url="https://integrate.api.nvidia.com/v1",
            api_key=nvidia_api_key
        )
    except Exception as e:
        print(f"❌ Error initializing NVIDIA client: {e}")
        raise Exception(f"Failed to initialize NVIDIA API client: {str(e)}")
    
    # Strict formatting prompt
    prompt = f"""You are a PowerPoint content formatter. Convert the following raw educational content into a structured format suitable for PowerPoint slides.

STRICT FORMATTING RULES:
1. Use "# Title" for slide titles (one per slide)
2. Use "- Bullet point" for bullet points
3. Use "**text**" for bold text within bullets (e.g., "- **Important:** explanation")
4. For tables, use markdown pipe format:
   | Header 1 | Header 2 | Header 3 |
   |----------|----------|----------|
   | Cell A   | Cell B   | Cell C   |

SLIDE ORGANIZATION RULES:
- First slide: Use the main topic as the title with introductory content
- Each major section/topic = ONE new slide
- Each slide should have **MAXIMUM 5 bullet points** (NOT MORE THAN 5)
- If a topic has too much content, split it into multiple slides (e.g., "Topic - Part 1", "Topic - Part 2")
- Keep bullet points concise (1-2 lines each)
- Group related information together
- **LAST SLIDE MUST BE: "# Conclusion"** with summary bullet points

STRUCTURE GUIDELINES:
- Identify main topics/sections from the text
- Create a slide for each distinct topic
- Break down long paragraphs into bullet points
- Use bold (**text**) for key terms, names, or emphasis
- If there are comparisons or data, use tables
- Ensure the final slide is titled "Conclusion" with key takeaways

CRITICAL RULES:
- Do NOT add any explanations or comments outside the formatted content
- Do NOT add markdown code blocks (no ```)
- Output ONLY the formatted text
- Make sure every slide starts with "# "
- Do NOT create a separate title slide - first slide should have content
- END WITH "# Conclusion" slide

Raw content to format:

{raw_content}

Now output the formatted text following ALL the rules above:"""

    print("\n" + "="*60)
    print("STAGE 2: STRICT FORMATTING")
    print("="*60)
    print("🤖 Calling NVIDIA LLM for strict formatting...")
    print("📡 Model: z-ai/glm-5.2")
    print("⏱️ Timeout: 10 minutes")
    print("-" * 60 + "\n")
    
    try:
        # Call NVIDIA LLM
        completion = client.chat.completions.create(
            model="z-ai/glm-5.2",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,  # Lower temperature for consistent formatting
            top_p=1,
            max_tokens=16384,
            seed=42,
            stream=True,
            timeout=600  # 10 minutes timeout
        )
        
        # Collect streamed response
        formatted_text = ""
        print(f"{REASONING_COLOR}📥 Receiving formatted response...")
        print("=" * 60)
        print("[STREAMING FORMATTED CONTENT]")
        print("=" * 60 + "\n")
        
        for chunk in completion:
            if not getattr(chunk, "choices", None):
                continue
            if len(chunk.choices) == 0 or getattr(chunk.choices[0], "delta", None) is None:
                continue
            
            delta = chunk.choices[0].delta
            if getattr(delta, "content", None) is not None:
                content_piece = delta.content
                formatted_text += content_piece
                print(content_piece, end="", flush=True)
        
        print(f"{RESET_COLOR}\n")
        print("=" * 60)
        print("✅ FORMATTING COMPLETE")
        print("=" * 60)
        print(f"📊 Formatted content length: {len(formatted_text)} characters")
        print(f"📄 Approximate word count: {len(formatted_text.split())}")
        
        # Estimate token usage (rough approximation)
        try:
            estimated_input_tokens = len(prompt) // 4
            estimated_output_tokens = len(formatted_text) // 4
            print("\n💰 ESTIMATED TOKEN USAGE:")
            print(f"   Input tokens:  ~{estimated_input_tokens}")
            print(f"   Output tokens: ~{estimated_output_tokens}")
            print(f"   Total tokens:  ~{estimated_input_tokens + estimated_output_tokens}")
        except Exception as e:
            print(f"\n⚠️ Could not estimate token usage: {e}")
        
        print("=" * 60 + "\n")
        
        return formatted_text.strip()
        
    except Exception as e:
        print(f"❌ Error during formatting: {e}")
        raise Exception(f"Stage 2 formatting failed: {str(e)}")


def save_formatted_content(formatted_text, output_file="basic_text_converted.txt"):
    """Save the formatted content to file"""
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(formatted_text)
        print(f"💾 Formatted content saved to: {output_file}")
        return True
    except Exception as e:
        print(f"❌ Error saving formatted content: {e}")
        return False


def main():
    """Main function - can be called from API or command line"""
    
    print("\n" + "="*60)
    print("🏥 GVMCH AI PPT MAKER - STAGE 2")
    print("="*60 + "\n")
    
    # Check if raw content file exists
    input_file = "stage1_raw_content.txt"
    
    if not os.path.isfile(input_file):
        print(f"❌ Error: {input_file} not found")
        print("Please run Stage 1 first to generate raw content")
        sys.exit(1)
    
    # Read raw content from Stage 1
    print(f"📄 Reading raw content from: {input_file}")
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            raw_content = f.read()
        print(f"✅ Read {len(raw_content)} characters\n")
    except Exception as e:
        print(f"❌ Error reading file: {e}")
        sys.exit(1)
    
    # Format with strict rules
    print("🚀 Starting strict formatting...")
    try:
        formatted_content = format_with_strict_rules(raw_content)
    except Exception as e:
        print(f"\n❌ Error formatting content: {e}")
        sys.exit(1)
    
    # Save formatted content
    if save_formatted_content(formatted_content):
        print("\n✅ Stage 2 Complete!")
        print("📄 Output: basic_text_converted.txt")
        print("\n💡 Next: Run PPT generation to create PowerPoint")
    else:
        print("\n❌ Failed to save formatted content")
        sys.exit(1)


if __name__ == "__main__":
    main()
