// ============================================
// SIMPLE STUDENT FORM - SENDS JSON TO BACKEND
// ============================================

import { useState } from 'react';
import './App.css';

function App() {
  // Get backend URL from environment variable
  const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:3000';

  // State to store form data
  const [formData, setFormData] = useState({
    topic: '',
    name: '',
    degree: '',
    year: '',
    department: '',
    contentSuggestion: '',
    noOfSlides: '10'
  });

  // State to show success message
  const [submitted, setSubmitted] = useState(false);

  // State to track loading (prevents multiple clicks)
  const [isGenerating, setIsGenerating] = useState(false);

  // Update form data when user types
  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({
      ...formData,
      [name]: value
    });
  };

  // Send data to backend when form is submitted
  const handleSubmit = async (e) => {
    e.preventDefault(); // Prevent page reload

    // Prevent multiple submissions
    if (isGenerating) {
      console.log('⚠️ Already generating. Please wait...');
      return;
    }

    setIsGenerating(true); // Lock the button

    try {
      // Print what we're sending
      console.log('📤 Sending to backend:', formData);

      // Send JSON to backend
      const response = await fetch(`${API_URL}/api/submit-student`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json', // Tell backend we're sending JSON
        },
        body: JSON.stringify(formData) // Convert object to JSON string
      });

      // Get response from backend
      const result = await response.json();

      // Print backend response
      console.log('✅ Backend says:', result);

      if (result.success) {
        // Show success message
        setSubmitted(true);
      } else {
        alert(`Error: ${result.message}`);
      }

    } catch (error) {
      // If backend is not running
      console.error('❌ Error:', error);
      alert('Cannot connect to backend! Make sure server is running on port 3000');
    } finally {
      setIsGenerating(false); // Unlock the button
    }
  };

  // Reset form for another submission
  const handleReset = () => {
    setFormData({
      topic: '',
      name: '',
      degree: '',
      year: '',
      department: '',
      contentSuggestion: '',
      noOfSlides: '10'
    });
    setSubmitted(false);
    setIsGenerating(false);
  };

  // ============================================
  // SUCCESS PAGE (after generation)
  // ============================================
  if (submitted) {
    return (
      <div className="container">
        <div className="success-message">
          <h2>✅ PPT Generated Successfully!</h2>
          <div className="submitted-data">
            <h3>Your Details:</h3>
            <p><strong>Topic:</strong> {formData.topic}</p>
            <p><strong>Name:</strong> {formData.name}</p>
            <p><strong>Degree:</strong> {formData.degree}</p>
            <p><strong>Year:</strong> {formData.year}</p>
            <p><strong>Department:</strong> {formData.department}</p>
            <p><strong>Number of Slides:</strong> {formData.noOfSlides}</p>
            {formData.contentSuggestion && (
              <p><strong>Content Suggestion:</strong> {formData.contentSuggestion}</p>
            )}
          </div>


          <div style={{ display: 'flex', gap: '10px', justifyContent: 'center', flexWrap: 'wrap', marginTop: '20px' }}>
            <button
              onClick={() => window.open(`${API_URL}/api/download-ppt`, '_blank')}
              className="btn-primary"
              style={{
                width: 'auto',
                padding: '12px 30px',
                background: 'linear-gradient(135deg, #27ae60 0%, #229954 100%)'
              }}
            >
              📥 Download PPT
            </button>
            <button onClick={handleReset} className="btn-secondary">
              Try a New PPT
            </button>
          </div>

        </div>
      </div>
    );
  }

  // ============================================
  // MAIN FORM
  // ============================================
  return (
    <div className="container">
      <div className="form-wrapper">
        <h1>🏥 GVMCH AI PPT MAKER</h1>

        <form onSubmit={handleSubmit}>
          {/* Topic */}
          <div className="form-group">
            <label htmlFor="topic">Topic:</label>
            <input
              type="text"
              id="topic"
              name="topic"
              value={formData.topic}
              onChange={handleChange}
              required
              placeholder="Enter your topic"
            />
          </div>

          {/* Name */}
          <div className="form-group">
            <label htmlFor="name">Name:</label>
            <input
              type="text"
              id="name"
              name="name"
              value={formData.name}
              onChange={handleChange}
              required
              placeholder="Enter your full name"
            />
          </div>

          {/* UG/PG */}
          <div className="form-group">
            <label htmlFor="degree">UG/PG:</label>
            <select
              id="degree"
              name="degree"
              value={formData.degree}
              onChange={handleChange}
              required
            >
              <option value="">Select degree type</option>
              <option value="UG">UG (Undergraduate)</option>
              <option value="PG">PG (Postgraduate)</option>
            </select>
          </div>

          {/* Year */}
          <div className="form-group">
            <label htmlFor="year">Year of Studying:</label>
            <select
              id="year"
              name="year"
              value={formData.year}
              onChange={handleChange}
              required
            >
              <option value="">Select year</option>
              <option value="1">1st Year</option>
              <option value="2">2nd Year</option>
              <option value="3">3rd Year</option>
              <option value="4">4th Year</option>
              <option value="5">5th Year</option>
            </select>
          </div>

          {/* Department */}
          <div className="form-group">
            <label htmlFor="department">Department:</label>
            <input
              type="text"
              id="department"
              name="department"
              value={formData.department}
              onChange={handleChange}
              required
              placeholder="Enter your department"
            />
          </div>

          {/* Content Suggestion */}
          <div className="form-group">
            <label htmlFor="contentSuggestion">Content Suggestion (Optional):</label>
            <textarea
              id="contentSuggestion"
              name="contentSuggestion"
              value={formData.contentSuggestion}
              onChange={handleChange}
              placeholder="Enter specific focus areas or key points (optional)"
              rows="4"
            />
          </div>

          {/* Number of Slides */}
          <div className="form-group">
            <label htmlFor="noOfSlides">Number of Slides:</label>
            <input
              type="number"
              id="noOfSlides"
              name="noOfSlides"
              value={formData.noOfSlides}
              onChange={handleChange}
              required
              min="5"
              max="30"
              placeholder="10"
            />
          </div>

          {/* Generate Button */}
          <button
            type="submit"
            className="btn-primary"
            disabled={isGenerating}
          >
            {isGenerating ? '🔄 Generating PPT...' : '🎨 Generate PPT'}
          </button>

          {isGenerating && (
            <p className="loading-text">
              ⏳ Please wait... This may take 30-60 seconds
            </p>
          )}
        </form>
      </div>
    </div>
  );
}

export default App;
