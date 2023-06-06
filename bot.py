import json
import random

import requests

HOST = "http://127.0.0.1:8000"


def read_config_file():
    with open("var/bot_config.json") as json_file:
        data = json.load(json_file)
        return data


def generate_random_username_and_password():
    username = "user" + str(random.randint(1, 100000))
    password = "password" + str(random.randint(1, 100000))

    return username, password


def get_token_for_user(username, password):
    response = requests.post(
        f"{HOST}/api/user/login/",
        json={
            "username": username,
            "password": password,
        },
    )

    if response.status_code == 200:
        return response.json().get("access")


def signup_users(number_of_users):
    created_users = []

    while len(created_users) < number_of_users:
        username, password = generate_random_username_and_password()

        response = requests.post(
            f"{HOST}/api/user/register/",
            json={
                "username": username,
                "password": password,
            },
        )

        if response.status_code == 201:
            print(f"User {username} created successfully")

            token = get_token_for_user(username, password)

            if token:
                created_users.append(
                    {
                        "username": username,
                        "password": password,
                        "token": token,
                    }
                )

    return created_users


def create_posts(created_users, max_posts_per_user):
    created_posts = []

    for user in created_users:
        number_of_posts = random.randint(1, max_posts_per_user)

        for i in range(number_of_posts):

            response = requests.post(
                f"{HOST}/api/posts/",
                headers={"Authorization": f"Bearer {user['token']}"},
                json={"title": f"test title {i}", "content": f"test content {i}"},
            )

            if response.status_code == 201:
                print(f"Post created successfully for user {user['username']}")
                created_posts.append(
                    {"username": user["username"], "post_id": response.json()["id"]}
                )

    return created_posts


def like_posts(created_users, created_posts, max_likes_per_user):
    for user in created_users:
        number_of_likes = random.randint(1, max_likes_per_user)

        for i in range(number_of_likes):
            post = random.choice(created_posts)

            response = requests.post(
                f"{HOST}/api/posts/{post['post_id']}/like-unlike/",
                headers={"Authorization": f"Bearer {user['token']}"},
            )

            if response.status_code == 200:
                print(
                    f"Post {post['post_id']} liked successfully by user {user['username']}"
                )


def main():
    config = read_config_file()
    print(config)
    number_of_users = config["number_of_users"]
    max_posts_per_user = config["max_posts_per_user"]
    max_likes_per_user = config["max_likes_per_user"]

    if not number_of_users:
        print("Number of users is not defined in config file")
        return

    created_users = signup_users(config["number_of_users"])
    created_posts = create_posts(created_users, max_posts_per_user)
    like_posts(created_users, created_posts, max_likes_per_user)


if __name__ == "__main__":
    main()
