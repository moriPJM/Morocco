# Morocco Travel App

A React TypeScript web application for Morocco travel with automatic translation features and guide information.

## Features

- 🔤 **Real-time Translation**: Translate between Arabic, French, Berber, and English
- 📖 **Comprehensive Guides**: Detailed information about Moroccan cities, culture, and cuisine  
- 🗺️ **Interactive Maps**: Navigate Morocco with detailed maps and points of interest
- ❤️ **Favorites**: Save your favorite places and information for quick access
- 🌍 **Internationalization**: Multi-language support with proper RTL text direction
- 📱 **Responsive Design**: Optimized for mobile and desktop devices

## Technology Stack

- **Frontend**: React 18 with TypeScript
- **Styling**: Tailwind CSS with custom Morocco-themed colors
- **Internationalization**: react-i18next
- **Maps**: React Leaflet
- **Build Tool**: Vite
- **State Management**: Zustand

## Project Structure

```
src/
├── components/         # Reusable UI components
│   └── Navigation.tsx  # Main navigation component
├── pages/             # Page components
│   ├── Home.tsx       # Landing page
│   ├── Translator.tsx # Translation interface
│   ├── Guides.tsx     # Travel guides
│   ├── Map.tsx        # Interactive map
│   └── Favorites.tsx  # User favorites
├── i18n/              # Internationalization
│   └── i18n.ts        # i18n configuration
├── App.tsx            # Main app component
├── main.tsx           # App entry point
└── index.css          # Global styles
```

## Prerequisites

Before running this project, you need to install:

1. **Node.js** (version 16 or higher)
   - Download from: https://nodejs.org/
   - Verify installation: `node --version`

2. **npm** (comes with Node.js)
   - Verify installation: `npm --version`

## Installation

1. **Install dependencies**:
   ```bash
   npm install
   ```

2. **Start development server**:
   ```bash
   npm run dev
   ```

3. **Build for production**:
   ```bash
   npm run build
   ```

## Development

- **Development server**: `npm run dev` (runs on http://localhost:3000)
- **Type checking**: `npm run lint`
- **Production build**: `npm run build`
- **Preview production build**: `npm run preview`

## Morocco Travel Features

### Translation Component
- Support for Arabic, French, Berber (Tamazight), and English
- Real-time text translation
- Common phrases library
- Right-to-left (RTL) text support for Arabic

### Travel Guides
- **Cities**: Marrakech, Casablanca, Fez, Rabat, Chefchaouen, Essaouira
- **Culture**: Berber heritage, Islamic art, traditional crafts
- **Cuisine**: Tagine, mint tea, traditional recipes
- **Practical Tips**: Currency, language, etiquette, best travel times

### Interactive Map
- Major Moroccan cities with detailed information
- Points of interest and attractions
- Responsive map interface using Leaflet

### Favorites System
- Save favorite places, phrases, and guides
- Organized by categories
- Quick access to saved content

## Styling

The app uses Tailwind CSS with custom Morocco-themed colors:

- **Morocco Red**: `#C1272D` (flag red)
- **Morocco Green**: `#006233` (flag green)  
- **Morocco Gold**: `#FFD700` (accent color)
- **Morocco Sand**: `#F4A460` (desert theme)
- **Morocco Blue**: `#4682B4` (Atlantic coast)

## Translation API

Currently uses mock translations for demonstration. In production, integrate with:
- Google Translate API
- Azure Translator
- AWS Translate
- Custom translation service

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is open source and available under the [MIT License](LICENSE).

## Next Steps

To enhance the application, consider adding:

- Real translation API integration
- Offline functionality with service workers
- User authentication and personal favorites sync
- Weather information for cities
- Currency converter
- Local events and festivals
- Hotel and restaurant recommendations
- Photo gallery for attractions
- Audio pronunciation guides
- GPS navigation integration