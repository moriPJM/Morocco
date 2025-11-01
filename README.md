# Morocco Travel App

A React TypeScript web application for Morocco travel with comprehensive features including AI-powered guidance, advanced translation with speech synthesis, and beautiful interactive guides.

## ✨ Latest Features (November 2024)

### 🎤 **Advanced Speech Features**
- **Multi-language Speech Synthesis**: Japanese, English, Arabic text-to-speech
- **Speech Recognition**: Voice input for translations
- **Arabic Speech Support**: Specialized Arabic pronunciation with fallback options
- **Interactive Phrase Cards**: Hover-activated speech buttons for common phrases

### 🗣️ **Enhanced Translation System**
- **Japanese Default**: Japanese as the primary language
- **Contextual Phrases**: Situation-based conversation helpers
- **6 Categories**: Greetings, gratitude, navigation, dining, shopping, emergencies
- **Real-time Audio**: Instant pronunciation for all supported languages

### 🎨 **Beautiful Guide Interface**
- **Modern Card Layout**: Elegant, responsive design with gradients
- **Quick Navigation**: Category-based browsing with smooth scrolling
- **AI Integration**: Prominent AI guide placement with premium styling
- **Visual Hierarchy**: Clear information structure with icons and colors

## Core Features

- 🤖 **AI-Powered Guide**: OpenAI GPT-3.5 integration for intelligent travel advice
- 🔤 **Real-time Translation**: Translate between Arabic, French, Berber, Japanese, and English
- 🎵 **Speech Technology**: Advanced text-to-speech and speech recognition
- 📖 **Comprehensive Guides**: Detailed information about Moroccan cities, culture, and cuisine  
- 🗺️ **Interactive Maps**: Navigate Morocco with detailed maps and points of interest
- ❤️ **Favorites**: Save your favorite places and information for quick access
- 🌍 **Internationalization**: Multi-language support with proper RTL text direction
- 📱 **Responsive Design**: Optimized for mobile and desktop devices

## Technology Stack

- **Frontend**: React 18 with TypeScript
- **Backend**: Python Flask with OpenAI API integration
- **Styling**: Tailwind CSS with custom Morocco-themed colors
- **Internationalization**: react-i18next
- **Maps**: React Leaflet
- **Build Tool**: Vite
- **AI**: OpenAI GPT-3.5 Turbo

## Prerequisites

Before running this project, you need to install:

1. **Python** (version 3.8 or higher)
   - Download from: https://python.org/
   - Verify installation: `python --version`

2. **Node.js** (version 16 or higher)
   - Download from: https://nodejs.org/
   - Verify installation: `node --version`

3. **OpenAI API Key**
   - Get your API key from: https://platform.openai.com/api-keys
   - Add to `.env` file: `VITE_OPENAI_API_KEY=your_api_key_here`

## Quick Start (Python)

### Option 1: Automatic Setup (Recommended)

**Windows:**
```bash
start.bat
```

**Cross-platform:**
```bash
python start.py
```

This will automatically:
- Install Python dependencies
- Install Node.js dependencies  
- Build the frontend
- Start the Flask server on http://localhost:5000

### Option 2: Manual Setup

1. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Install Node.js dependencies:**
   ```bash
   npm install
   ```

3. **Build the frontend:**
   ```bash
   npm run build
   ```

4. **Start the Python server:**
   ```bash
   python app.py
   ```

5. **Access the app at:** http://localhost:5000

## Development Mode

For development with hot reloading:

1. **Start the Python backend:**
   ```bash
   python app.py
   ```

2. **In another terminal, start the frontend dev server:**
   ```bash
   npm run dev
   ```

3. **Access frontend at:** http://localhost:3001
4. **Backend API at:** http://localhost:5000/api

## Project Structure

```
├── app.py                    # Python Flask backend
├── start.py                  # Python startup script
├── start.bat                 # Windows batch startup
├── requirements.txt          # Python dependencies
├── .env                      # Environment variables (OpenAI API key)
├── src/
│   ├── components/           # React components
│   │   ├── AIGuide.tsx       # AI chatbot component
│   │   ├── SpeechControls.tsx # Speech synthesis/recognition
│   │   └── Navigation.tsx
│   ├── pages/               # Page components
│   │   ├── Home.tsx
│   │   ├── Translator.tsx    # Enhanced with speech features
│   │   ├── Guides.tsx        # Beautiful card-based layout
│   │   └── Map.tsx
│   ├── utils/               # Utility functions
│   │   └── speechUtils.ts    # Speech API utilities
│   └── i18n/                # Internationalization
├── public/                  # Static assets
│   └── images/              # Morocco-themed images
├── dist/                    # Built frontend (created after build)
└── package.json             # Node.js dependencies
```

## API Endpoints

The Flask backend provides the following endpoints:

- `GET /` - Serve React app
- `POST /api/chat` - AI chat with OpenAI GPT-3.5
- `GET /api/health` - Health check
- `GET /<path>` - Static file serving

## Environment Variables

Create a `.env` file in the root directory:

```env
VITE_OPENAI_API_KEY=your_openai_api_key_here
FLASK_ENV=development
PORT=5000
```

## AI Guide Features

The AI guide uses OpenAI GPT-3.5 Turbo to provide:

- Expert advice on Moroccan tourism
- Cultural insights and etiquette tips
- Restaurant and accommodation recommendations
- Safety and travel tips
- Weather and seasonal advice
- Language assistance

## 🎤 Speech Features

### Supported Languages
- **Japanese** (ja-JP): Default language with natural pronunciation
- **English** (en-US): Clear American English pronunciation  
- **Arabic** (ar-SA): Standard Arabic with fallback options
- **Moroccan Arabic** (ar-MA): Dialect-specific pronunciation when available
- **French** (fr-FR): Standard French pronunciation

### Speech Controls
- **🔊 Text-to-Speech**: Click speaker icons to hear pronunciations
- **🎤 Speech Recognition**: Voice input for translation text
- **🕌 Arabic Audio**: Specialized buttons for Arabic phrases
- **🎌 Japanese Audio**: Native Japanese pronunciation
- **📱 Mobile Optimized**: Touch-friendly speech controls

### How to Use Speech Features
1. Navigate to the **Translation** page
2. Hover over phrase cards to reveal speech buttons
3. Click language-specific icons for pronunciation:
   - 🔊 English pronunciation
   - 🎌 Japanese pronunciation  
   - 🕌 Arabic pronunciation
4. Use microphone button for voice input
5. Check browser console for speech debugging information

## 🎨 UI/UX Improvements

### Modern Design Elements
- **Gradient Backgrounds**: Morocco-themed color schemes
- **Card-based Layout**: Clean, organized information display
- **Hover Animations**: Interactive elements with smooth transitions
- **Responsive Grid**: Adapts to all screen sizes
- **Visual Hierarchy**: Clear information prioritization

### Navigation Enhancements
- **Quick Links**: Jump to specific guide sections
- **Category Badges**: Visual indicators for content types
- **Smooth Scrolling**: Seamless page navigation
- **Mobile Menu**: Optimized mobile navigation

## Deployment

### Local Production

```bash
# Build frontend
npm run build

# Start production server
python app.py
```

### Docker (Optional)

```dockerfile
FROM python:3.11
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
RUN npm install && npm run build
EXPOSE 5000
CMD ["python", "app.py"]
```

## Troubleshooting

### Common Issues

1. **Port 5000 already in use:**
   - Change PORT in .env file
   - Or stop the conflicting process

2. **OpenAI API errors:**
   - Check your API key in .env
   - Verify API key has sufficient credits
   - Check internet connection

3. **Build failures:**
   - Delete `node_modules` and run `npm install`
   - Clear npm cache: `npm cache clean --force`

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is open source and available under the [MIT License](LICENSE).