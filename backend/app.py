# ============================================
# SIMPLE PYTHON BACKEND WITH FILE STORAGE
# ============================================

from flask import Flask, request, jsonify, send_file 
from flask_cors import CORS
from datetime import datetime
import json
import os
import sys

# Create Flask app
app = Flask(__name__)
CORS(app)  # Allow React to connect

# File to store data
DATA_FILE = 'students_data.json'

# Track if processing is in progress
is_processing = False

# ============================================
# HELPER FUNCTIONS - Save/Load from file
# ============================================

def load_from_file():
    """Load data from JSON file"""
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return []

def save_to_file(data):
    """Save data to JSON file"""
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=2)

# ============================================
# API ENDPOINT - SUBMIT STUDENT FORM
# ============================================

@app.route('/api/submit-student', methods=['POST'])
def submit_student():
    global is_processing
    
    # Prevent multiple simultaneous submissions
    if is_processing:
        print('⚠️  Already processing a request. Please wait...')
        return jsonify({
            'success': False,
            'message': 'Another request is already being processed. Please wait.'
        }), 429  # 429 = Too Many Requests
    
    try:
        is_processing = True  # Lock
        
        # STEP 1: Get JSON data from React
        form_data = request.get_json()
        print(f'📤 Received from React: {form_data}')
        
        # STEP 2: Add ID and timestamp
        student_data = {
            'id': int(datetime.now().timestamp() * 1000),
            'timestamp': datetime.now().strftime('%m/%d/%Y, %I:%M:%S %p'),
            **form_data
        }
        
        # STEP 3: Save to file for record keeping
        submitted_data = [student_data]
        save_to_file(submitted_data)
        
        print('\n═══════════════════════════════════════════')
        print('✅ STORED IN FILE (REPLACED PREVIOUS):')
        print(student_data)
        print(f'Total submissions: {len(submitted_data)} (only keeps latest)')
        print(f'📁 Saved to: {DATA_FILE}')
        print('═══════════════════════════════════════════\n')
        
        # STEP 4: Call all 3 stages to generate PPT
        print('🚀 Starting 3-Stage PPT Generation Process...\n')
        
        try:
            # Import modules
            import stage1
            import stage2
            import text_to_ppt
            
            # STAGE 1: Generate content using NVIDIA LLM
            print("="*60)
            print("STAGE 1: CONTENT GENERATION")
            print("="*60)
            generated_content = stage1.generate_content_with_nvidia(form_data)
            stage1.save_raw_content(generated_content)
            print('\n✅ Stage 1 Complete! Raw content generated.')
            
            # STAGE 2: Format strictly with Gemini
            print("\n" + "="*60)
            print("STAGE 2: STRICT FORMATTING")
            print("="*60)
            formatted_content = stage2.format_with_strict_rules(generated_content)
            stage2.save_formatted_content(formatted_content)
            print('\n✅ Stage 2 Complete! Content formatted.')
            
            # STAGE 3: Generate PowerPoint (no terminal prompts!)
            print("\n" + "="*60)
            print("STAGE 3: POWERPOINT GENERATION")
            print("="*60)
            
            import text_to_ppt
            
            ppt_file = text_to_ppt.generate_ppt_with_data(
                topic=form_data.get('topic', ''),
                presenter=form_data.get('name', ''),
                department=form_data.get('department', '')
            )
            print(f'\n✅ Stage 3 Complete! PowerPoint: {ppt_file}')
            
            # STEP 5: Send response back to React
            return jsonify({
                'success': True,
                'message': 'PPT generated successfully!',
                'receivedData': student_data,
                'totalSubmissions': len(submitted_data),
                'pptFile': ppt_file,
                'stages': {
                    'stage1': 'Content generation complete',
                    'stage2': 'Formatting complete',
                    'stage3': 'PowerPoint generated'
                }
            })
            
        except Exception as e:
            print(f'\n❌ Error: {e}')
            import traceback
            traceback.print_exc()
            return jsonify({
                'success': False,
                'message': f'Error: {str(e)}',
                'receivedData': student_data
            }), 500
    
    finally:
        is_processing = False  # Unlock after completion or error

# ============================================
# OPTIONAL: View all stored data
# ============================================

@app.route('/api/students', methods=['GET'])
def get_students():
    submitted_data = load_from_file()
    return jsonify({
        'success': True,
        'count': len(submitted_data),
        'data': submitted_data
    })

# ============================================
# API ENDPOINT - DOWNLOAD PPT
# ============================================

@app.route('/api/download-ppt', methods=['GET'])
def download_ppt():
    """Send the generated PPT file to frontend for download"""
    ppt_file = 'presentation.pptx'

    if not os.path.exists(ppt_file):
        return jsonify({
            'success': False,
            'message': 'PPT file not found. Please generate first.'
        }), 404

    return send_file(
        ppt_file,
        as_attachment=True,
        download_name='GVMCH_Presentation.pptx',
        mimetype='application/vnd.openxmlformats-officedocument.presentationml.presentation'
    )


# ============================================
# START SERVER
# ============================================

if __name__ == '__main__':
    print('\n╔═══════════════════════════════════════════════╗')
    print('║   🐍 PYTHON FLASK SERVER WITH FILE STORAGE   ║')
    print('╚═══════════════════════════════════════════════╝')
    print('📡 Server running at: http://localhost:3000')
    print(f'📁 Data file: {DATA_FILE}')
    print('\n📌 Available APIs:')
    print('   POST   /api/submit-student  (Submit form data)')
    print('   GET    /api/students        (View all data)')
    print('\n💾 Data stored in: students_data.json')
    print('Press Ctrl+C to stop\n')
    
    app.run(host='localhost', port=3000, debug=True)
