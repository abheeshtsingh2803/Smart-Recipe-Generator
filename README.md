# Smart Recipe Generator

A modern web application that helps users generate creative recipes based on available ingredients using AI, find matching recipes from a database, and manage their culinary preferences.

## Features

- **AI-Powered Recipe Generation**: Generate new recipes using OpenAI's GPT-4 based on your available ingredients
- **Ingredient Recognition**: Upload images to automatically detect ingredients (planned feature)
- **Recipe Matching**: Find existing recipes that match your available ingredients
- **Dietary Preferences**: Filter recipes based on dietary restrictions and preferences
- **Cuisine Selection**: Generate recipes from specific cuisines
- **Difficulty Levels**: Choose recipes by preparation difficulty
- **Nutrition Information**: Get detailed nutritional breakdown for each recipe
- **Saved Recipes**: Save and manage your favorite recipes
- **Responsive Design**: Modern, mobile-friendly interface built with React and Tailwind CSS

## Tech Stack

### Backend
- **FastAPI**: High-performance web framework for building APIs
- **MongoDB**: NoSQL database for storing recipes and user data
- **Motor**: Async MongoDB driver for Python
- **OpenAI GPT-4**: AI-powered recipe generation
- **Pydantic**: Data validation and serialization
- **Uvicorn**: ASGI server for running the FastAPI app

### Frontend
- **React 19**: Modern JavaScript library for building user interfaces
- **React Router**: Declarative routing for React
- **Tailwind CSS**: Utility-first CSS framework
- **Radix UI**: Accessible UI components
- **Axios**: HTTP client for API requests
- **React Hook Form**: Performant forms with easy validation
- **Zod**: TypeScript-first schema validation

## Prerequisites

- Python 3.8+
- Node.js 16+
- Yarn package manager
- MongoDB (local or cloud instance)
- OpenAI API key (for recipe generation)

## Installation and Setup

### Backend Setup

1. **Navigate to the backend directory:**
   ```bash
   cd Smart-Recipe-Generator/backend
