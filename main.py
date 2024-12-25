import os
from dotenv import load_dotenv
from tortoise import Tortoise, fields
from tortoise.models import Model

# Load environment variables from a .env file (if you're using one)
load_dotenv()

# Fetch username and password from environment variables
DB_USERNAME = os.getenv('DB_USERNAME')
DB_PASSWORD = os.getenv('DB_PASSWORD')

# Step 1: Define Database Configuration
DATABASE_CONFIG = {
    "connections": {
        "default": f"postgres://{DB_USERNAME}:{DB_PASSWORD}@localhost:5432/tortoise_demo"
    },
    "apps": {
        "models": {
            "models": ["__main__"],
            "default_connection": "default",
        }
    }
}

# Step 2: Initialize Database
async def init():
    await Tortoise.init(config=DATABASE_CONFIG)
    await Tortoise.generate_schemas()

# Step 3: Define Models
class User(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=50)
    email = fields.CharField(max_length=100, unique=True)
    created_at = fields.DatetimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
class Post(Model):
    id = fields.IntField(pk=True)
    title = fields.CharField(max_length=100)
    content = fields.TextField()
    author = fields.ForeignKeyField("models.User", related_name="posts")

    def __str__(self):
        return self.title

# Step 4: CRUD Operations and Queries
async def main():
    await init()

    # Create user
    user = await User.create(name="Alice", email="alice@example.com")
    print(f"User Created: {user}")

    # Create post
    post = await Post.create(title="My First Post", content="Hello World!", author=user)
    print(f"Post Created: {post}")

    # Read user
    retrieved_user = await User.get(id=user.id)
    print(f"Retrieved User: {retrieved_user}")

    # Update user
    retrieved_user.name = "Alice Wonderland"
    await retrieved_user.save()
    print(f"Updated User: {retrieved_user}")

    # Delete post
    # await post.delete()
    # print(f"Post Deleted: {post.id}")

    # Query all users
    users = await User.all()
    for user in users:
        print(f"User: {user.name}")

    # Query with filter
    filtered_users = await User.filter(name__icontains="Alice")
    for user in filtered_users:
        print(f"Filtered User: {user.name}")

    # Query with ordering
    ordered_users = await User.all().order_by("-created_at")
    for user in ordered_users:
        print(f"Ordered User: {user.name}")

    # Paginate query
    paginated_users = await User.all().offset(0).limit(10)
    for user in paginated_users:
        print(f"Paginated User: {user.name}")

    # Fetch related data
    related_user = await User.get(id=user.id).prefetch_related("posts")
    for post in related_user.posts:
        print(f"Related Post: {post.title}")

    # Clean up
    await Post.all().delete()
    await User.all().delete()
    print("Database Cleaned Up")

    # Step 5: Run the script
if __name__ == "__main__":
    import asyncio
    asyncio.run(main())




