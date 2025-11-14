from fastapi import FastAPI, APIRouter
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path

# Import route initializers
from routes.recipe_routes import init_recipe_routes
from routes.ingredient_routes import init_ingredient_routes
from routes.user_routes import init_user_routes

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ.get('MONGO_URL', 'mongodb://localhost:27017')
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ.get('DB_NAME', 'recipe_generator_db')]

# Create the main app
app = FastAPI(title="Smart Recipe Generator API")

# Create main API router
api_router = APIRouter(prefix="/api")

# Health check
@api_router.get("/")
async def root():
    return {"message": "Smart Recipe Generator API is running", "status": "healthy"}

# Include all route modules
api_router.include_router(init_recipe_routes(db))
api_router.include_router(init_ingredient_routes())
api_router.include_router(init_user_routes(db))

# Include the main router in the app
app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=os.environ.get('CORS_ORIGINS', '*').split(','),
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@app.on_event("startup")
async def startup_db_client():
    logger.info("Starting up Smart Recipe Generator API...")
    # Seed initial recipes if database is empty
    count = await db.recipes.count_documents({})
    if count == 0:
        logger.info("Seeding initial recipes...")
        await seed_recipes()

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()
    logger.info("Shutting down Smart Recipe Generator API...")


async def seed_recipes():
    """Seed the database with initial recipes"""
    from models.recipe import Recipe, NutritionInfo
    from datetime import datetime, timezone
    
    initial_recipes = [
        {
            "name": "Classic Margherita Pizza",
            "ingredients": ["pizza dough", "tomato sauce", "mozzarella cheese", "fresh basil", "olive oil", "salt"],
            "instructions": [
                "Preheat oven to 475°F (245°C)",
                "Roll out pizza dough into a circle",
                "Spread tomato sauce evenly",
                "Add mozzarella cheese",
                "Bake for 12-15 minutes until crust is golden",
                "Top with fresh basil and drizzle with olive oil"
            ],
            "cuisine": "Italian",
            "difficulty": "easy",
            "cooking_time": 25,
            "serving_size": 4,
            "dietary_tags": ["vegetarian"],
            "nutrition": {"calories": 285, "protein": 12, "carbs": 36, "fat": 10, "fiber": 2}
        },
        {
            "name": "Chicken Stir Fry",
            "ingredients": ["chicken breast", "soy sauce", "garlic", "ginger", "bell peppers", "broccoli", "carrots", "sesame oil", "rice"],
            "instructions": [
                "Cut chicken into bite-sized pieces",
                "Heat sesame oil in wok",
                "Stir fry chicken until cooked",
                "Add vegetables and stir fry for 5 minutes",
                "Add soy sauce, garlic, and ginger",
                "Serve over cooked rice"
            ],
            "cuisine": "Asian",
            "difficulty": "easy",
            "cooking_time": 20,
            "serving_size": 4,
            "dietary_tags": ["high-protein"],
            "nutrition": {"calories": 320, "protein": 28, "carbs": 38, "fat": 6, "fiber": 4}
        },
        {
            "name": "Vegetable Curry",
            "ingredients": ["coconut milk", "curry paste", "potatoes", "carrots", "peas", "onions", "garlic", "ginger", "cilantro"],
            "instructions": [
                "Sauté onions, garlic, and ginger",
                "Add curry paste and cook for 2 minutes",
                "Add chopped vegetables",
                "Pour in coconut milk",
                "Simmer for 20 minutes until vegetables are tender",
                "Garnish with cilantro"
            ],
            "cuisine": "Indian",
            "difficulty": "medium",
            "cooking_time": 35,
            "serving_size": 6,
            "dietary_tags": ["vegetarian", "vegan", "gluten-free"],
            "nutrition": {"calories": 245, "protein": 6, "carbs": 32, "fat": 12, "fiber": 6}
        },
        {
            "name": "Grilled Salmon with Asparagus",
            "ingredients": ["salmon fillets", "asparagus", "lemon", "olive oil", "garlic", "salt", "pepper", "dill"],
            "instructions": [
                "Preheat grill to medium-high",
                "Season salmon with salt, pepper, and dill",
                "Toss asparagus with olive oil and garlic",
                "Grill salmon for 4-5 minutes per side",
                "Grill asparagus for 6-8 minutes",
                "Serve with lemon wedges"
            ],
            "cuisine": "American",
            "difficulty": "easy",
            "cooking_time": 20,
            "serving_size": 2,
            "dietary_tags": ["high-protein", "low-carb", "gluten-free"],
            "nutrition": {"calories": 340, "protein": 35, "carbs": 8, "fat": 18, "fiber": 4}
        },
        {
            "name": "Spaghetti Carbonara",
            "ingredients": ["spaghetti", "eggs", "parmesan cheese", "bacon", "black pepper", "salt"],
            "instructions": [
                "Cook spaghetti according to package",
                "Fry bacon until crispy",
                "Beat eggs with parmesan cheese",
                "Drain pasta, reserving pasta water",
                "Mix hot pasta with egg mixture",
                "Add bacon and pasta water to create creamy sauce",
                "Season with black pepper"
            ],
            "cuisine": "Italian",
            "difficulty": "medium",
            "cooking_time": 25,
            "serving_size": 4,
            "dietary_tags": [],
            "nutrition": {"calories": 485, "protein": 22, "carbs": 52, "fat": 20, "fiber": 2}
        },
        {
            "name": "Greek Salad",
            "ingredients": ["cucumber", "tomatoes", "red onion", "feta cheese", "olives", "olive oil", "lemon juice", "oregano"],
            "instructions": [
                "Chop cucumber, tomatoes, and onion",
                "Combine in large bowl",
                "Add crumbled feta cheese and olives",
                "Drizzle with olive oil and lemon juice",
                "Sprinkle with oregano",
                "Toss gently and serve"
            ],
            "cuisine": "Greek",
            "difficulty": "easy",
            "cooking_time": 10,
            "serving_size": 4,
            "dietary_tags": ["vegetarian", "gluten-free", "low-carb"],
            "nutrition": {"calories": 180, "protein": 6, "carbs": 12, "fat": 14, "fiber": 3}
        },
        {
            "name": "Beef Tacos",
            "ingredients": ["ground beef", "taco shells", "lettuce", "tomatoes", "cheese", "sour cream", "taco seasoning", "onions"],
            "instructions": [
                "Brown ground beef in skillet",
                "Add taco seasoning and water",
                "Simmer for 10 minutes",
                "Warm taco shells",
                "Fill shells with beef",
                "Top with lettuce, tomatoes, cheese, and sour cream"
            ],
            "cuisine": "Mexican",
            "difficulty": "easy",
            "cooking_time": 20,
            "serving_size": 6,
            "dietary_tags": [],
            "nutrition": {"calories": 325, "protein": 18, "carbs": 28, "fat": 16, "fiber": 3}
        },
        {
            "name": "Mushroom Risotto",
            "ingredients": ["arborio rice", "mushrooms", "white wine", "vegetable broth", "parmesan cheese", "butter", "onions", "garlic"],
            "instructions": [
                "Sauté onions and garlic in butter",
                "Add mushrooms and cook until soft",
                "Add rice and toast for 2 minutes",
                "Add wine and stir until absorbed",
                "Add broth one ladle at a time, stirring constantly",
                "Cook for 20 minutes until creamy",
                "Stir in parmesan cheese"
            ],
            "cuisine": "Italian",
            "difficulty": "hard",
            "cooking_time": 45,
            "serving_size": 4,
            "dietary_tags": ["vegetarian"],
            "nutrition": {"calories": 380, "protein": 12, "carbs": 54, "fat": 12, "fiber": 2}
        },
        {
            "name": "Pad Thai",
            "ingredients": ["rice noodles", "shrimp", "eggs", "bean sprouts", "peanuts", "lime", "fish sauce", "tamarind paste", "garlic"],
            "instructions": [
                "Soak rice noodles in warm water",
                "Heat oil and scramble eggs",
                "Add shrimp and cook until pink",
                "Add drained noodles",
                "Add fish sauce and tamarind paste",
                "Toss with bean sprouts",
                "Serve with peanuts and lime wedges"
            ],
            "cuisine": "Thai",
            "difficulty": "medium",
            "cooking_time": 30,
            "serving_size": 4,
            "dietary_tags": ["high-protein"],
            "nutrition": {"calories": 420, "protein": 24, "carbs": 58, "fat": 12, "fiber": 3}
        },
        {
            "name": "Caprese Salad",
            "ingredients": ["tomatoes", "mozzarella cheese", "fresh basil", "olive oil", "balsamic vinegar", "salt", "pepper"],
            "instructions": [
                "Slice tomatoes and mozzarella",
                "Arrange alternating slices on plate",
                "Tuck basil leaves between slices",
                "Drizzle with olive oil and balsamic vinegar",
                "Season with salt and pepper"
            ],
            "cuisine": "Italian",
            "difficulty": "easy",
            "cooking_time": 5,
            "serving_size": 4,
            "dietary_tags": ["vegetarian", "gluten-free", "low-carb"],
            "nutrition": {"calories": 220, "protein": 12, "carbs": 8, "fat": 16, "fiber": 2}
        },
        {
            "name": "Chicken Caesar Salad",
            "ingredients": ["romaine lettuce", "grilled chicken", "parmesan cheese", "croutons", "caesar dressing"],
            "instructions": [
                "Grill and slice chicken breast",
                "Chop romaine lettuce",
                "Toss lettuce with caesar dressing",
                "Top with sliced chicken",
                "Add parmesan cheese and croutons"
            ],
            "cuisine": "American",
            "difficulty": "easy",
            "cooking_time": 15,
            "serving_size": 2,
            "dietary_tags": ["high-protein"],
            "nutrition": {"calories": 450, "protein": 38, "carbs": 22, "fat": 24, "fiber": 3}
        },
        {
            "name": "Vegetable Stir Fry",
            "ingredients": ["broccoli", "bell peppers", "carrots", "snap peas", "soy sauce", "garlic", "ginger", "sesame oil"],
            "instructions": [
                "Heat sesame oil in wok",
                "Add garlic and ginger",
                "Add hardest vegetables first (carrots, broccoli)",
                "Stir fry for 3 minutes",
                "Add softer vegetables (peppers, peas)",
                "Add soy sauce and toss",
                "Cook until vegetables are tender-crisp"
            ],
            "cuisine": "Asian",
            "difficulty": "easy",
            "cooking_time": 15,
            "serving_size": 4,
            "dietary_tags": ["vegan", "vegetarian", "gluten-free"],
            "nutrition": {"calories": 120, "protein": 4, "carbs": 18, "fat": 4, "fiber": 5}
        },
        {
            "name": "Beef Stroganoff",
            "ingredients": ["beef sirloin", "mushrooms", "onions", "sour cream", "beef broth", "egg noodles", "flour", "butter"],
            "instructions": [
                "Cut beef into strips",
                "Brown beef in butter",
                "Sauté mushrooms and onions",
                "Sprinkle flour and stir",
                "Add beef broth and simmer",
                "Stir in sour cream",
                "Serve over cooked egg noodles"
            ],
            "cuisine": "Russian",
            "difficulty": "medium",
            "cooking_time": 40,
            "serving_size": 6,
            "dietary_tags": [],
            "nutrition": {"calories": 520, "protein": 32, "carbs": 42, "fat": 24, "fiber": 2}
        },
        {
            "name": "Quinoa Buddha Bowl",
            "ingredients": ["quinoa", "chickpeas", "avocado", "kale", "sweet potato", "tahini", "lemon", "olive oil"],
            "instructions": [
                "Cook quinoa according to package",
                "Roast chickpeas and sweet potato cubes",
                "Massage kale with olive oil",
                "Assemble bowl with quinoa as base",
                "Add roasted vegetables and kale",
                "Top with sliced avocado",
                "Drizzle with tahini-lemon dressing"
            ],
            "cuisine": "American",
            "difficulty": "easy",
            "cooking_time": 35,
            "serving_size": 2,
            "dietary_tags": ["vegan", "vegetarian", "gluten-free"],
            "nutrition": {"calories": 485, "protein": 16, "carbs": 68, "fat": 18, "fiber": 14}
        },
        {
            "name": "French Onion Soup",
            "ingredients": ["onions", "beef broth", "white wine", "french bread", "gruyere cheese", "butter", "thyme"],
            "instructions": [
                "Slice onions thinly",
                "Caramelize onions in butter for 40 minutes",
                "Add wine and reduce",
                "Add beef broth and thyme",
                "Simmer for 30 minutes",
                "Toast bread slices",
                "Top soup with bread and cheese",
                "Broil until cheese melts"
            ],
            "cuisine": "French",
            "difficulty": "hard",
            "cooking_time": 90,
            "serving_size": 4,
            "dietary_tags": [],
            "nutrition": {"calories": 380, "protein": 18, "carbs": 42, "fat": 16, "fiber": 4}
        },
        {
            "name": "Shakshuka",
            "ingredients": ["eggs", "tomatoes", "bell peppers", "onions", "garlic", "cumin", "paprika", "feta cheese", "parsley"],
            "instructions": [
                "Sauté onions, peppers, and garlic",
                "Add tomatoes and spices",
                "Simmer until thickened",
                "Make wells in sauce",
                "Crack eggs into wells",
                "Cover and cook until eggs set",
                "Top with feta and parsley"
            ],
            "cuisine": "Middle Eastern",
            "difficulty": "medium",
            "cooking_time": 30,
            "serving_size": 4,
            "dietary_tags": ["vegetarian", "gluten-free"],
            "nutrition": {"calories": 240, "protein": 14, "carbs": 18, "fat": 14, "fiber": 4}
        },
        {
            "name": "Teriyaki Chicken Bowl",
            "ingredients": ["chicken thighs", "teriyaki sauce", "rice", "edamame", "carrots", "sesame seeds", "green onions"],
            "instructions": [
                "Marinate chicken in teriyaki sauce",
                "Grill or pan-fry chicken",
                "Cook rice",
                "Steam edamame",
                "Julienne carrots",
                "Assemble bowl with rice, chicken, and vegetables",
                "Garnish with sesame seeds and green onions"
            ],
            "cuisine": "Japanese",
            "difficulty": "easy",
            "cooking_time": 25,
            "serving_size": 4,
            "dietary_tags": ["high-protein"],
            "nutrition": {"calories": 420, "protein": 32, "carbs": 52, "fat": 8, "fiber": 4}
        },
        {
            "name": "Lentil Soup",
            "ingredients": ["red lentils", "carrots", "celery", "onions", "garlic", "vegetable broth", "cumin", "turmeric", "lemon"],
            "instructions": [
                "Sauté onions, carrots, and celery",
                "Add garlic and spices",
                "Add lentils and broth",
                "Simmer for 25 minutes",
                "Blend half the soup for creaminess",
                "Season with lemon juice"
            ],
            "cuisine": "Mediterranean",
            "difficulty": "easy",
            "cooking_time": 35,
            "serving_size": 6,
            "dietary_tags": ["vegan", "vegetarian", "gluten-free"],
            "nutrition": {"calories": 210, "protein": 12, "carbs": 38, "fat": 2, "fiber": 8}
        },
        {
            "name": "Chicken Fajitas",
            "ingredients": ["chicken breast", "bell peppers", "onions", "fajita seasoning", "tortillas", "lime", "sour cream", "cilantro"],
            "instructions": [
                "Slice chicken and vegetables",
                "Season chicken with fajita seasoning",
                "Sauté chicken until cooked",
                "Add peppers and onions",
                "Cook until vegetables are tender",
                "Warm tortillas",
                "Serve with lime, sour cream, and cilantro"
            ],
            "cuisine": "Mexican",
            "difficulty": "easy",
            "cooking_time": 20,
            "serving_size": 4,
            "dietary_tags": ["high-protein"],
            "nutrition": {"calories": 380, "protein": 32, "carbs": 42, "fat": 10, "fiber": 5}
        },
        {
            "name": "Coconut Curry Shrimp",
            "ingredients": ["shrimp", "coconut milk", "red curry paste", "bell peppers", "onions", "garlic", "ginger", "basil", "lime"],
            "instructions": [
                "Sauté onions, garlic, and ginger",
                "Add curry paste and cook",
                "Add coconut milk and bring to simmer",
                "Add shrimp and peppers",
                "Cook until shrimp are pink",
                "Garnish with basil and lime"
            ],
            "cuisine": "Thai",
            "difficulty": "medium",
            "cooking_time": 25,
            "serving_size": 4,
            "dietary_tags": ["gluten-free", "high-protein"],
            "nutrition": {"calories": 290, "protein": 28, "carbs": 14, "fat": 16, "fiber": 2}
        },
        {
            "name": "Eggplant Parmesan",
            "ingredients": ["eggplant", "marinara sauce", "mozzarella cheese", "parmesan cheese", "bread crumbs", "eggs", "basil"],
            "instructions": [
                "Slice eggplant and salt to remove moisture",
                "Dip in egg then bread crumbs",
                "Fry until golden",
                "Layer eggplant with marinara and cheese",
                "Bake at 375°F for 25 minutes",
                "Garnish with fresh basil"
            ],
            "cuisine": "Italian",
            "difficulty": "medium",
            "cooking_time": 50,
            "serving_size": 6,
            "dietary_tags": ["vegetarian"],
            "nutrition": {"calories": 320, "protein": 16, "carbs": 28, "fat": 18, "fiber": 6}
        }
    ]
    
    recipes_to_insert = []
    for recipe_data in initial_recipes:
        recipe = Recipe(**recipe_data)
        doc = recipe.model_dump()
        doc['created_at'] = doc['created_at'].isoformat()
        recipes_to_insert.append(doc)
    
    if recipes_to_insert:
        await db.recipes.insert_many(recipes_to_insert)
        logger.info(f"Successfully seeded {len(recipes_to_insert)} recipes")