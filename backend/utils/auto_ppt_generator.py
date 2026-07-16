import os
import sys
import subprocess
from llm_formatter import format_text_with_llm

def read_input_file(file_path):
    """Read the raw input text file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found")
        sys.exit(1)
    except Exception as e:
        print(f"Error reading file: {e}")
        sys.exit(1)


def save_formatted_text(formatted_text, output_path="basic_text_converted.txt"):
    """Save the formatted text to the intermediate file"""
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(formatted_text)
        print(f"✅ Formatted text saved to: {output_path}")
        return True
    except Exception as e:
        print(f"Error saving formatted text: {e}")
        return False


def get_presentation_details():
    """Prompt user for presentation details"""
    print("\n" + "="*60)
    print("PRESENTATION DETAILS")
    print("="*60)
    topic = input("Topic          : ").strip()
    presenter = input("Presenter name : ").strip()
    department = input("Department     : ").strip()
    print("="*60 + "\n")
    
    return topic, presenter, department


def main():
    print("\n" + "="*60)
    print("AUTOMATED POWERPOINT GENERATOR (ORCHESTRATOR)")
    print("="*60 + "\n")
    
    # Check arguments
    if len(sys.argv) < 2:
        print("Usage: python auto_ppt_generator.py <input_text_file.txt>")
        print("\nExample:")
        print("  python auto_ppt_generator.py raw_input.txt")
        print("\nThis will:")
        print("  1. Format text with LLM")
        print("  2. Save to basic_text_converted.txt")
        print("  3. Generate PowerPoint automatically")
        sys.exit(1)
    
    input_file = sys.argv[1]
    
    # Check if input file exists
    if not os.path.isfile(input_file):
        print(f"❌ Error: Input file '{input_file}' not found")
        sys.exit(1)
    
    # STEP 1: Read raw input file
    print(f"📄 Reading input file: {input_file}")
    raw_text = read_input_file(input_file)
    print(f"✅ Read {len(raw_text)} characters\n")
    
    # STEP 2: Format text using LLM
    print("🤖 Formatting text with Gemini LLM...")
    formatted_text = format_text_with_llm(raw_text)
    
    if not formatted_text:
        print("❌ Failed to format text")
        sys.exit(1)
    
    # STEP 3: Save formatted text
    print("\n💾 Saving formatted text...")
    if not save_formatted_text(formatted_text):
        sys.exit(1)
    
    # STEP 4: Call text_to_ppt.py to generate PowerPoint
    print("\n🎨 Generating PowerPoint presentation...")
    print("-" * 60)
    
    try:
        # Import and run text_to_ppt.py main function directly
        import text_to_ppt
        text_to_ppt.main()
        
        print("\n" + "="*60)
        print("🎉 ALL DONE! Presentation is ready.")
        print("="*60 + "\n")
        
    except Exception as e:
        print(f"\n❌ Error generating PowerPoint: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
