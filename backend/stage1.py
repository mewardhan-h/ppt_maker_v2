"""
Stage 1: Content Generation with NVIDIA LLM
Receives user details and generates rich educational content
"""

from openai import OpenAI
import os
import sys
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Color codes for terminal output
USE_COLOR = sys.stdout.isatty() and os.getenv("NO_COLOR") is None
REASONING_COLOR = "\033[90m" if USE_COLOR else ""
RESET_COLOR = "\033[0m" if USE_COLOR else ""


def generate_content_with_nvidia(user_data):
    """
    Generate educational content using NVIDIA LLM based on user details
    
    Args:
        user_data (dict): Contains topic, name, degree, year, department, contentSuggestion, noOfSlides
    
    Returns:
        str: Generated content
    """
    
    # Get NVIDIA API key from environment
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
    
    # Extract user details
    topic = user_data.get("topic", "")
    name = user_data.get("name", "")
    degree = user_data.get("degree", "")
    year = user_data.get("year", "")
    department = user_data.get("department", "")
    content_suggestion = user_data.get("contentSuggestion", "")
    no_of_slides = user_data.get("noOfSlides", "10")
    
    # Create dynamic prompt based on user details
    prompt = f"""You are an expert medical educator creating presentation content for a {degree} student in year {year} studying {department} at Government Villupuram Medical College and Hospital (GVMCH).

STUDENT PROFILE:
- Name: {name}
- Degree: {degree}
- Year: {year}
- Department: {department}

PRESENTATION TOPIC: {topic}

CONTENT REQUIREMENTS:
- Create approximately {no_of_slides} slides worth of content
- Tailor the depth and complexity to a {degree} Year {year} level
- Focus on {department} perspective
- Include relevant clinical pearls, guidelines, and evidence-based information

{"SPECIFIC FOCUS AREAS:" if content_suggestion else ""}
{content_suggestion if content_suggestion else ""}

CRITICAL FORMATTING INSTRUCTIONS:
- DO NOT create a separate "Title Slide"
- Start directly with Slide 1 containing the introduction and key concepts
- The first slide title should be the main topic: {topic}
- Each subsequent section should become a new slide
- Keep content organized by topic sections
- Use clear headings that could become slide titles
- Include important facts, statistics, classifications, and guidelines
- Add relevant clinical pearls and practical tips
- **LAST SLIDE MUST BE: "Conclusion"** with key takeaways and summary points

STRUCTURE EXAMPLE:
Slide 1: {topic} - Introduction & Overview
Slide 2: Classification/Epidemiology
Slide 3: Clinical Features
... (middle slides)
Final Slide: Conclusion (with key summary points and takeaways)

Generate comprehensive, well-organized educational content. Focus on accuracy and practical clinical relevance. DO NOT include a separate title slide - start directly with content. END WITH A CONCLUSION SLIDE.

IMPORTANT: Generate rich, detailed educational content organized by clear topic sections. The first slide should contain substantial introductory content, and the LAST slide must be titled "Conclusion" with summary points."""

    print("\n" + "="*60)
    print("STAGE 1: CONTENT GENERATION")
    print("="*60)
    print(f"\n📚 Topic: {topic}")
    print(f"👤 Student: {name}")
    print(f"🎓 Level: {degree} Year {year}")
    print(f"🏥 Department: {department}")
    print(f"📊 Target slides: {no_of_slides}")
    if content_suggestion:
        print(f"💡 Focus areas: {content_suggestion[:100]}...")
    print("\n" + "="*60)
    print("🤖 CALLING NVIDIA LLM (z-ai/glm-5.2)")
    print("="*60)
    print("⏳ Sending request to NVIDIA API...")
    print("📡 Model: z-ai/glm-5.2")
    print("🎯 Max tokens: 16384")
    print("⏱️ Timeout: 10 minutes")
    print("-" * 60 + "\n")
    
    # Call NVIDIA LLM with timeout handling
    try:
        completion = client.chat.completions.create(
            model="z-ai/glm-5.2",
            messages=[{"role": "user", "content": prompt}],
            temperature=1,
            top_p=1,
            max_tokens=16384,
            seed=42,
            stream=True,
            timeout=600  # 10 minutes timeout
        )
    except Exception as api_error:
        print(f"\n❌ Error calling NVIDIA API: {api_error}")
        raise Exception(f"NVIDIA API call failed: {str(api_error)}")
    
    # Collect streamed response
    generated_content = ""
    print(f"{REASONING_COLOR}📥 Receiving response from NVIDIA LLM...")
    print("=" * 60)
    print("[STREAMING CONTENT - LLM OUTPUT]")
    print("=" * 60 + "\n")
    
    try:
        for chunk in completion:
            if not getattr(chunk, "choices", None):
                continue
            if len(chunk.choices) == 0 or getattr(chunk.choices[0], "delta", None) is None:
                continue
            
            delta = chunk.choices[0].delta
            if getattr(delta, "content", None) is not None:
                content_piece = delta.content
                generated_content += content_piece
                print(content_piece, end="", flush=True)
    
    except Exception as stream_error:
        print(f"\n\n⚠️ WARNING: Stream interrupted: {stream_error}")
        print(f"📊 Partial content received: {len(generated_content)} characters")
        
        if len(generated_content) < 500:
            raise Exception(f"Stream interrupted too early. Only {len(generated_content)} characters received. Please try again.")
        else:
            print("⚠️ Using partial content (stream interrupted mid-way)")
    
    print(f"{RESET_COLOR}\n")
    print("=" * 60)
    print("✅ RECEIVED COMPLETE RESPONSE FROM LLM")
    print("=" * 60)
    print(f"📊 Total characters received: {len(generated_content)}")
    print(f"📄 Approximate word count: {len(generated_content.split())}")
    
    # Get token usage if available
    try:
        if hasattr(completion, 'usage'):
            usage = completion.usage
            print("\n💰 TOKEN USAGE:")
            print(f"   Input tokens:  {usage.prompt_tokens if hasattr(usage, 'prompt_tokens') else 'N/A'}")
            print(f"   Output tokens: {usage.completion_tokens if hasattr(usage, 'completion_tokens') else 'N/A'}")
            print(f"   Total tokens:  {usage.total_tokens if hasattr(usage, 'total_tokens') else 'N/A'}")
        else:
            # Estimate tokens (rough approximation: 1 token ≈ 4 characters)
            estimated_input_tokens = len(prompt) // 4
            estimated_output_tokens = len(generated_content) // 4
            print("\n💰 ESTIMATED TOKEN USAGE:")
            print(f"   Input tokens:  ~{estimated_input_tokens}")
            print(f"   Output tokens: ~{estimated_output_tokens}")
            print(f"   Total tokens:  ~{estimated_input_tokens + estimated_output_tokens}")
    except Exception as e:
        print(f"\n⚠️ Could not retrieve token usage: {e}")
    
    print("=" * 60 + "\n")
    
    return generated_content


def save_raw_content(content, output_file="stage1_raw_content.txt"):
    """Save the raw generated content to a file"""
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"💾 Raw content saved to: {output_file}")
        return True
    except Exception as e:
        print(f"❌ Error saving content: {e}")
        return False


def main():
    """Main function - can be called from API or command line"""
    
    print("\n" + "="*60)
    print("🏥 GVMCH AI PPT MAKER - STAGE 1")
    print("="*60 + "\n")
    
    # Check if JSON data is provided as command line argument
    if len(sys.argv) > 1:
        # Read from command line argument (JSON string or file path)
        arg = sys.argv[1]
        print("📂 Reading input data...")
        try:
            # Try to parse as JSON string
            user_data = json.loads(arg)
            print("✅ JSON string parsed successfully\n")
        except json.JSONDecodeError:
            # Try to read as file path
            try:
                with open(arg, 'r', encoding='utf-8') as f:
                    user_data = json.load(f)
                print(f"✅ Loaded from file: {arg}\n")
            except Exception as e:
                print(f"❌ Error reading input: {e}")
                print("\nUsage:")
                print('  python stage1.py \'{"topic":"...", "name":"...", ...}\'')
                print("  python stage1.py input.json")
                sys.exit(1)
    else:
        # Interactive mode - prompt for details
        print("📝 Enter presentation details:\n")
        user_data = {
            "topic": input("Topic: ").strip(),
            "name": input("Your name: ").strip(),
            "degree": input("Degree (UG/PG): ").strip(),
            "year": input("Year: ").strip(),
            "department": input("Department: ").strip(),
            "contentSuggestion": input("Content suggestions (optional, press Enter to skip): ").strip(),
            "noOfSlides": input("Number of slides (default 10): ").strip() or "10"
        }
    
    # Generate content with first LLM
    print("🚀 Starting content generation...\n")
    generated_content = generate_content_with_nvidia(user_data)
    
    # Show preview and ask for confirmation
    print("\n" + "="*60)
    print("📋 CONTENT PREVIEW (First 500 characters)")
    print("="*60)
    print(generated_content[:500] + "...")
    print("="*60 + "\n")
    
    # Ask user if they want to proceed to formatting
    print("❓ Content generated successfully!")
    print("\nOptions:")
    print("  1. Save and proceed to Stage 2 (formatting)")
    print("  2. Save and exit")
    print("  3. Cancel (don't save)")
    
    choice = input("\nEnter your choice (1/2/3): ").strip()
    
    if choice == "3":
        print("\n❌ Cancelled. Content not saved.")
        sys.exit(0)
    
    # Save raw content
    print("\n💾 Saving raw content...")
    if save_raw_content(generated_content):
        print("✅ Stage 1 Complete!")
        print("📄 Output saved: stage1_raw_content.txt")
        
        if choice == "1":
            print("\n" + "="*60)
            print("🔄 READY FOR STAGE 2")
            print("="*60)
            print("Next step: Format this content into strict PPT structure")
            print("\nRun: python stage2.py")
        else:
            print("\n✅ Content saved. Exiting.")
    else:
        print("\n❌ Failed to save content")
        sys.exit(1)


if __name__ == "__main__":
    main()
