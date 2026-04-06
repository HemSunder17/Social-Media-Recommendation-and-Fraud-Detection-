import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'socialmedia_project.settings')
django.setup()

from accounts.models import User, Interest, INTEREST_CHOICES
from posts.models import Post, Like, Comment

# ── CREATE INTERESTS ──────────────────────────────────────────
print("Creating interests...")
for value, label in INTEREST_CHOICES:
    Interest.objects.get_or_create(name=value)

# ── CREATE USERS ──────────────────────────────────────────────
print("Creating users...")

users_data = [
    {'username': 'alex_drives', 'email': 'alex@demo.com', 'password': 'demo1234', 'interests': ['cars', 'technology', 'fitness']},
    {'username': 'pet_lover_sara', 'email': 'sara@demo.com', 'password': 'demo1234', 'interests': ['dogs', 'cats', 'food']},
    {'username': 'wanderlust_jay', 'email': 'jay@demo.com', 'password': 'demo1234', 'interests': ['travel', 'food', 'music']},
    {'username': 'gym_freak_mike', 'email': 'mike@demo.com', 'password': 'demo1234', 'interests': ['fitness', 'motivation', 'food']},
    {'username': 'techie_priya', 'email': 'priya@demo.com', 'password': 'demo1234', 'interests': ['technology', 'art', 'music']},
]

created_users = []
for data in users_data:
    if not User.objects.filter(username=data['username']).exists():
        user = User.objects.create_user(
            username=data['username'],
            email=data['email'],
            password=data['password'],
        )
        for interest_name in data['interests']:
            interest = Interest.objects.get(name=interest_name)
            user.interests.add(interest)
        created_users.append(user)
        print(f"  Created user: {user.username}")
    else:
        created_users.append(User.objects.get(username=data['username']))
        print(f"  User already exists: {data['username']}")

# ── CREATE POSTS ──────────────────────────────────────────────
print("Creating posts...")

posts_data = [
    {'username': 'alex_drives', 'category': 'cars', 'content': 'Just took my new BMW M3 for a spin on the highway. The acceleration is absolutely insane! 0 to 100 in under 4 seconds. Nothing beats that feeling. 🚗💨'},
    {'username': 'alex_drives', 'category': 'cars', 'content': 'Top 5 cars I want to own before I turn 30: Ferrari 488, Lamborghini Huracan, Porsche 911, McLaren 720S, and the Ford GT. A man can dream! 🏎️'},
    {'username': 'alex_drives', 'category': 'technology', 'content': 'Tesla Full Self Driving V12 is genuinely impressive. Drove from Bangalore to Mysore with zero interventions. The future of driving is here!'},
    {'username': 'pet_lover_sara', 'category': 'dogs', 'content': 'My golden retriever Bruno learned how to open the fridge today. I am both impressed and terrified. Send help. 🐶😂'},
    {'username': 'pet_lover_sara', 'category': 'cats', 'content': 'Adopted a new kitten today! Meet Luna 🐱 She spent the first hour hiding under the bed but now she won\'t leave my lap. Best decision ever!'},
    {'username': 'pet_lover_sara', 'category': 'dogs', 'content': 'Morning walks with Bruno are genuinely the best part of my day. There\'s something so peaceful about watching your dog discover the world with pure joy.'},
    {'username': 'pet_lover_sara', 'category': 'food', 'content': 'Made homemade dog biscuits today — peanut butter and banana flavor. Bruno approved. Recipe in the comments! 🍪'},
    {'username': 'wanderlust_jay', 'category': 'travel', 'content': 'Just landed in Bali! The rice terraces at Tegalalang are even more beautiful in person. Already planning to stay an extra week. ✈️🌴'},
    {'username': 'wanderlust_jay', 'category': 'travel', 'content': 'Backpacking through South East Asia on a budget of $30 a day is 100% doable. Vietnam, Cambodia, Thailand — all incredible. Here\'s how I did it. 🗺️'},
    {'username': 'wanderlust_jay', 'category': 'food', 'content': 'Street food in Bangkok is on another level. Pad Thai for 50 baht, mango sticky rice, and the most amazing green curry I\'ve ever had. Food tourism is real! 🍜'},
    {'username': 'wanderlust_jay', 'category': 'music', 'content': 'Attended a live jazz performance in New Orleans last night. There is something magical about live music in the city that invented it. 🎷'},
    {'username': 'gym_freak_mike', 'category': 'fitness', 'content': 'Hit a new PR today — 180kg deadlift! Two years ago I could barely lift 80kg. Consistency is everything. Trust the process. 💪'},
    {'username': 'gym_freak_mike', 'category': 'motivation', 'content': 'Nobody is coming to save you. Wake up early. Work hard. Stay consistent. The only person responsible for your success is YOU. Get after it! 🔥'},
    {'username': 'gym_freak_mike', 'category': 'fitness', 'content': 'My full chest workout: Bench Press 4x8, Incline DB Press 3x10, Cable Flyes 3x12, Dips 3x failure. Takes 45 mins and delivers serious results.'},
    {'username': 'gym_freak_mike', 'category': 'food', 'content': 'Meal prep Sunday done! 5 days of chicken, rice and vegetables ready to go. Abs are made in the kitchen, not just the gym. 🥗'},
    {'username': 'techie_priya', 'category': 'technology', 'content': 'Just built my first Neural Network from scratch using only NumPy — no TensorFlow, no PyTorch. Understanding backpropagation at a deep level is a game changer! 🧠'},
    {'username': 'techie_priya', 'category': 'technology', 'content': 'Hot take: Every developer should learn how to use the terminal properly before touching any IDE. The command line is your best friend. 💻'},
    {'username': 'techie_priya', 'category': 'art', 'content': 'Spent the weekend learning digital illustration. It\'s so much harder than it looks! Huge respect for digital artists. Here\'s my first attempt. 🎨'},
    {'username': 'techie_priya', 'category': 'music', 'content': 'Lo-fi hip hop playlists are scientifically proven to boost focus while coding. Currently 3 hours deep into a bug fix and honestly vibing. 🎵'},
]

for data in posts_data:
    user = User.objects.get(username=data['username'])
    if not Post.objects.filter(author=user, content=data['content']).exists():
        Post.objects.create(
            author=user,
            category=data['category'],
            content=data['content'],
        )
        print(f"  Created post by {data['username']} [{data['category']}]")

# ── CREATE LIKES ──────────────────────────────────────────────
print("Creating likes...")

all_posts = Post.objects.all()
all_users = User.objects.filter(is_superuser=False)

import random
random.seed(42)

for post in all_posts:
    likers = random.sample(list(all_users), k=random.randint(1, min(3, all_users.count())))
    for user in likers:
        if user != post.author:
            Like.objects.get_or_create(user=user, post=post)

print(f"  Likes created!")

# ── CREATE COMMENTS ───────────────────────────────────────────
print("Creating comments...")

comments_data = [
    ('alex_drives', 'cars', 'That M3 is a beast! The sound alone gives me chills.'),
    ('pet_lover_sara', 'dogs', 'Bruno sounds absolutely hilarious 😂 my dog does the same thing!'),
    ('wanderlust_jay', 'travel', 'Bali is on my bucket list! Which area are you staying in?'),
    ('gym_freak_mike', 'fitness', 'Incredible PR! What does your nutrition look like?'),
    ('techie_priya', 'technology', 'Building from scratch is the best way to really understand it!'),
    ('alex_drives', 'technology', 'Tesla FSD is wild. Did you try it in the rain?'),
    ('wanderlust_jay', 'food', 'Bangkok street food is unreal. Did you try the pad kra pao?'),
    ('gym_freak_mike', 'motivation', 'This is exactly what I needed to read today. Thank you! 🙏'),
]

posts_list = list(Post.objects.all())
for username, category, content in comments_data:
    user = User.objects.get(username=username)
    matching_posts = [p for p in posts_list if p.category == category and p.author != user]
    if matching_posts:
        post = random.choice(matching_posts)
        Comment.objects.get_or_create(user=user, post=post, content=content)

print("  Comments created!")

print("\n✅ Seed complete! Here are your demo accounts:")
print("─" * 40)
for data in users_data:
    print(f"  Username: {data['username']}  |  Password: demo1234")
print("─" * 40)
print("  Superuser: whatever you set during createsuperuser")