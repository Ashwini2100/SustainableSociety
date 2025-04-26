# Medical Symptoms Checker

An AI-powered web application that analyzes user-provided symptoms and suggests possible medical conditions using Google's Gemini AI.

## Overview

This application allows users to input their symptoms along with optional information like age and gender. The system then uses Google's Gemini AI to analyze the symptoms and provide a list of potential medical conditions, along with descriptions, common symptoms, and recommended actions.

![Medical Symptoms Checker Screenshot](screenshot.png)

## Features

- **Symptom Analysis**: Enter your symptoms and get AI-powered analysis
- **Condition Details**: View possible conditions with descriptions and common symptoms
- **Urgency Assessment**: Each condition is tagged with an urgency level (immediate attention, doctor visit, or self-care)
- **Responsive Design**: Works on desktop and mobile devices
- **Medical Disclaimers**: Clear disclaimers about the non-diagnostic nature of the results

## Technologies Used

- **Backend**: Python, Flask
- **Frontend**: HTML, CSS, JavaScript, Bootstrap
- **AI Integration**: Google Gemini AI API
- **Styling**: Bootstrap with a custom dark theme

## Requirements

- Python 3.x
- Flask
- Google Generative AI Python SDK
- API key for Google Gemini AI

## Setup and Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/medical-symptoms-checker.git
   cd medical-symptoms-checker
   ```

2. Install the required dependencies:
   ```
   pip install flask google-generativeai gunicorn
   ```

3. Set up your environment variables:
   - Create a `.env` file in the root directory
   - Add your Gemini API key: `GEMINI_API_KEY=your_api_key_here`

4. Run the application:
   ```
   python main.py
   ```

5. Open your browser and navigate to `http://localhost:5000`

## Usage

1. Enter your symptoms in the text area (be as detailed as possible)
2. Optionally provide your age and gender for more targeted results
3. Click "Analyze Symptoms"
4. Review the list of potential conditions
5. Note the urgency level for each condition

## Important Disclaimer

This tool does not provide medical advice. It is intended for informational purposes only and is not a substitute for professional medical consultation, diagnosis, or treatment. Always seek the advice of your physician or other qualified health provider with any questions you may have regarding a medical condition.

## How It Works

1. User inputs symptoms and optional information
2. The Flask backend sends this data to Google's Gemini AI
3. A specially crafted prompt instructs the AI to analyze the symptoms
4. The AI returns structured data with possible conditions
5. The application presents the results with urgency indicators

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgements

- Google Gemini AI for powering the symptom analysis
- Bootstrap for the responsive UI components
- Flask for the easy-to-use web framework
