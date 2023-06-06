import json
import random
import asyncio
import aiohttp

HOST = "http://127.0.0.1:8000"


async def read_config_file():
    with open("var/bot_config.json") as json_file:
        data = json.load(json_file)
        return data


def generate_random_username_and_password():
    username = "user" + str(random.randint(1, 100000))
    password = "password" + str(random.randint(1, 100000))
    return username, password


async def get_token_for_user(username, password):
    async with aiohttp.ClientSession() as session:
        response = await session.post(
            f"{HOST}/api/user/login/",
            json={
                "username": username,
                "password": password,
            },
        )

        if response.status == 200:
            return (await response.json()).get("access")


async def signup_user(username, password):
    async with aiohttp.ClientSession() as session:
        response = await session.post(
            f"{HOST}/api/user/register/",
            json={
                "username": username,
                "password": password,
                "first_name": "test",
                "last_name": "test",
            },
        )

        if response.status == 201:
            print(f"User {username} created successfully")

            token = await get_token_for_user(username, password)

            if token:
                return {
                    "username": username,
                    "password": password,
                    "token": token,
                }


async def signup_users(number_of_users):
    tasks = []

    for _ in range(number_of_users):
        username, password = generate_random_username_and_password()
        task = asyncio.create_task(signup_user(username, password))
        tasks.append(task)

    results = await asyncio.gather(*tasks)
    created_users = [user for user in results if user]

    return created_users


async def create_posts(created_users, max_posts_per_user):
    created_posts = []

    for user in created_users:
        number_of_posts = random.randint(1, max_posts_per_user)

        async with aiohttp.ClientSession() as session:
            for i in range(number_of_posts):
                response = await session.post(
                    f"{HOST}/api/posts/",
                    headers={"Authorization": f"Bearer {user['token']}"},
                    json={"title": f"test title {i}", "content": f"test content {i}"},
                )

                if response.status == 201:
                    print(f"Post created successfully for user {user['username']}")
                    created_posts.append(
                        {
                            "username": user["username"],
                            "post_id": (await response.json())["id"],
                        }
                    )

    return created_posts


async def like_posts(created_users, created_posts, max_likes_per_user):
    for user in created_users:
        number_of_likes = random.randint(1, max_likes_per_user)

        async with aiohttp.ClientSession() as session:
            for _ in range(number_of_likes):
                post = random.choice(created_posts)

                response = await session.post(
                    f"{HOST}/api/posts/{post['post_id']}/like-unlike/",
                    headers={"Authorization": f"Bearer {user['token']}"},
                )

                if response.status == 200:
                    print(
                        f"Post {post['post_id']} liked successfully by user {user['username']}"
                    )


async def main():
    config = await read_config_file()
    print(config)
    number_of_users = config["number_of_users"]
    max_posts_per_user = config["max_posts_per_user"]
    max_likes_per_user = config["max_likes_per_user"]

    if not number_of_users:
        print("Number of users is not defined in config file")
        return

    created_users = await signup_users(config["number_of_users"])
    created_posts = await create_posts(created_users, max_posts_per_user)
    await like_posts(created_users, created_posts, max_likes_per_user)


if __name__ == "__main__":
    asyncio.run(main())
