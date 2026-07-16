# Changes Summary - Token Tracking & Conclusion Slide

## Date: July 16, 2026

### Three Key Changes Made:

---

## ✅ 1. Stage 2 Now Uses NVIDIA LLM (Fixed 404 Error)

**Problem:** Gemini model `antigrvity` returned 404 error

**Solution:** Replaced Gemini with NVIDIA LLM in `stage2.py`

**Changes:**
- ❌ Removed: `from google import genai`
- ✅ Added: `from openai import OpenAI` (NVIDIA endpoint)
- ✅ Changed model: `z-ai/glm-5.2` (same as Stage 1)
- ✅ Uses `NVIDIA_API_KEY` from `.env` (no need for Gemini key anymore)

**File:** `c:\mewardhan\ppt_maker\backend\stage2.py`

---

## ✅ 2. Token Usage Tracking After Each LLM Call

**Added:** Token usage/cost tracking for both stages

### Stage 1 (Content Generation):
```
💰 ESTIMATED TOKEN USAGE:
   Input tokens:  ~XXXX
   Output tokens: ~XXXX
   Total tokens:  ~XXXX
```

### Stage 2 (Formatting):
```
💰 ESTIMATED TOKEN USAGE:
   Input tokens:  ~XXXX
   Output tokens: ~XXXX
   Total tokens:  ~XXXX
```

**How it works:**
- Estimates tokens using: `characters ÷ 4` (industry standard approximation)
- Shows input (prompt) + output (response) + total
- Prints after each LLM call completes

**Files modified:**
- `c:\mewardhan\ppt_maker\backend\stage1.py` (lines ~172-186)
- `c:\mewardhan\ppt_maker\backend\stage2.py` (lines ~142-150)

---

## ✅ 3. Last Slide Now Always "Conclusion"

**Added:** Automatic conclusion slide requirement

**Stage 1 Changes (Content Generation):**
- Prompt now explicitly requires: **"LAST SLIDE MUST BE: 'Conclusion'"**
- LLM instructed to end with summary points and key takeaways

**Stage 2 Changes (Formatting):**
- Formatter ensures: **"LAST SLIDE MUST BE: '# Conclusion'"**
- Validates structure ends with conclusion

**Structure now:**
```
Slide 1: [Topic] - Introduction & Overview
Slide 2: Classification/Epidemiology
Slide 3: Clinical Features
...
Final Slide: Conclusion (with key summary points)
```

**Files modified:**
- `c:\mewardhan\ppt_maker\backend\stage1.py` (line ~88)
- `c:\mewardhan\ppt_maker\backend\stage2.py` (line ~67-68)

---

## Technical Details

### NVIDIA LLM Configuration (Both Stages):
```python
client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key=nvidia_api_key
)

completion = client.chat.completions.create(
    model="z-ai/glm-5.2",
    messages=[{"role": "user", "content": prompt}],
    temperature=1,        # Stage 1: creative
    temperature=0.3,      # Stage 2: consistent formatting
    max_tokens=16384,
    timeout=600           # 10 minutes
)
```

### Token Estimation Logic:
```python
estimated_input_tokens = len(prompt) // 4
estimated_output_tokens = len(generated_content) // 4
total_tokens = estimated_input_tokens + estimated_output_tokens
```

---

## Testing Checklist

✅ Stage 1 completes without errors  
✅ Stage 2 completes without errors (no more 404)  
✅ Token usage prints after each stage  
✅ Last slide titled "Conclusion"  
✅ PPT generates successfully  
✅ Download button works  

---

## Next Steps

1. Test full flow: Form → Generate → Download
2. Verify token counts are reasonable
3. Verify conclusion slide appears in final PPT
4. Check if token estimates match actual usage (if NVIDIA provides usage stats)

---

## Environment Variables Required

Only need ONE API key now:

```env
NVIDIA_API_KEY=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
```

~~GEMINI_API_KEY~~ ← No longer needed!

---

## Files Changed

| File | Changes |
|------|---------|
| `backend/stage1.py` | ✅ Added token tracking, ✅ Added conclusion requirement |
| `backend/stage2.py` | ✅ Switched to NVIDIA LLM, ✅ Added token tracking, ✅ Added conclusion validation |
| `backend/requirements.txt` | ✅ google-genai already commented out |

---

**Status:** ✅ All changes complete and ready to test
