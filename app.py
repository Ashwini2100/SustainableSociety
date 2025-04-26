import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

import logging

from flask import Flask, render_template, request, jsonify
from utils.gemini_api import analyze_symptoms

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Create the Flask app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key")

@app.route("/")
def index():
    """Render the main page of the symptoms checker application."""
    return render_template("index.html")

@app.route("/analyze", methods=["POST"])
def analyze():
    """
    Process the symptoms provided by the user and return possible conditions.
    
    Expects a form with a 'symptoms' field containing the user's symptoms description.
    Returns a JSON response with analysis results or error information.
    """
    try:
        symptoms = request.form.get("symptoms", "")
        
        if not symptoms or len(symptoms.strip()) < 5:
            return jsonify({
                "success": False,
                "error": "Please provide a detailed description of your symptoms."
            })
        
        # Additional information that might be useful
        age = request.form.get("age", "")
        gender = request.form.get("gender", "")
        
        # Create context with all available information
        context = {
            "symptoms": symptoms,
            "age": age,
            "gender": gender
        }
        
        # Call the Gemini API to analyze symptoms
        analysis_result = analyze_symptoms(context)
        
        if analysis_result:
            return jsonify({
                "success": True,
                "result": analysis_result
            })
        else:
            return jsonify({
                "success": False,
                "error": "Unable to analyze symptoms. Please try again."
            })
    
    except Exception as e:
        logger.error(f"Error analyzing symptoms: {str(e)}")
        return jsonify({
            "success": False,
            "error": "An unexpected error occurred. Please try again later."
        })

# Error handling
@app.errorhandler(404)
def page_not_found(e):
    return render_template("index.html"), 404

@app.errorhandler(500)
def internal_server_error(e):
    return jsonify({
        "success": False,
        "error": "Internal server error. Please try again later."
    }), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
