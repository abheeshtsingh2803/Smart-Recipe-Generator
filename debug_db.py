import asyncio
import os
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables
ROOT_DIR = Path(__file__).parent / "backend"
load_dotenv(ROOT_DIR / '.env')

async def check_database():
    """Check database connection and recipe count"""
    try:
        # Connect to MongoDB
        mongo_url = os.environ.get('MONGO_URL', 'mongodb://localhost:27017')
        client = AsyncIOMotorClient(mongo_url)
        db = client[os.environ.get('DB_NAME', 'recipe_generator_db')]
        
        print(f"🔍 Connecting to: {mongo_url}")
        print(f"📊 Database: {db.name}")
        
        # Check connection
        await client.admin.command('ping')
        print("✅ Database connection successful")
        
        # Count recipes
        recipe_count = await db.recipes.count_documents({})
        print(f"📝 Recipes in database: {recipe_count}")
        
        # List collections
        collections = await db.list_collection_names()
        print(f"📂 Collections: {collections}")
        
        # If no recipes, try to seed manually
        if recipe_count == 0:
            print("🌱 No recipes found, attempting manual seeding...")
            await seed_recipes_manually(db)
        
        client.close()
        
    except Exception as e:
        print(f"❌ Database error: {str(e)}")

async def seed_recipes_manually(db):
    """Manually seed the database with a few test recipes"""
    try:
        from backend.models.recipe import Recipe, NutritionInfo
        from datetime import datetime, timezone
        
        test_recipes = [
            {
                "name": "Simple Pasta",
                "ingredients": ["pasta", "tomato sauce", "cheese"],
                "instructions": ["Boil pasta", "Add sauce", "Top with cheese"],
                "cuisine": "Italian",
                "difficulty": "easy",
                "cooking_time": 15,
                "serving_size": 2,
                "dietary_tags": ["vegetarian"],
                "nutrition": {"calories": 300, "protein": 12, "carbs": 45, "fat": 8, "fiber": 3}
            },
            {
                "name": "Chicken Salad",
                "ingredients": ["chicken breast", "lettuce", "tomatoes", "dressing"],
                "instructions": ["Cook chicken", "Chop vegetables", "Mix with dressing"],
                "cuisine": "American",
                "difficulty": "easy",
                "cooking_time": 20,
                "serving_size": 1,
                "dietary_tags": ["high-protein"],
                "nutrition": {"calories": 250, "protein": 25, "carbs": 10, "fat": 12, "fiber": 4}
            }
        ]
        
        recipes_to_insert = []
        for recipe_data in test_recipes:
            recipe = Recipe(**recipe_data)
            doc = recipe.model_dump()
            doc['created_at'] = doc['created_at'].isoformat()
            recipes_to_insert.append(doc)
        
        if recipes_to_insert:
            result = await db.recipes.insert_many(recipes_to_insert)
            print(f"✅ Inserted {len(result.inserted_ids)} test recipes")
        
    except Exception as e:
        print(f"❌ Seeding error: {str(e)}")

if __name__ == "__main__":
    asyncio.run(check_database())