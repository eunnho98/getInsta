from main import InstagramMedia, InstagramUser
from db import CRUD
from dotenv import load_dotenv
import argparse, os


def argparser():
    parser = argparse.ArgumentParser()
    parser.add_argument("--username", required=True)
    config = parser.parse_args()
    return config


if __name__ == "__main__":
    name_list = [
        "onemore._1",
        "breadroider",
        "hwwwan___",
        "woongkida",
        "105_minn",
        "ddang_jun",
        "beaugosse_hoon",
        "jaehun_allright",
        "physical_huun",
    ]
    hashtag = "보디빌딩대회"
    load_dotenv()
    account = InstagramUser("name", "password")
    account.login_user()
    db = CRUD()
    for name in name_list:
        user_id = account.get_user_id_by_name(name)
        print("userid", user_id)

        db.insertDB(
            schema="public",
            table="user",
            column="user_id, username",
            data=f"'{str(user_id)}', '{name}'",
        )

        result = account.get_user_info_by_username(name)

        if result["category"] == None:
            result["category"] = ""
        if result["category_name"] == None:
            result["category_name"] = ""

        mixed_data = [
            (
                str(user_id),
                result["full_name"],
                result["is_private"],
                result["profile_url"],
                result["media_count"],
                result["follower_count"],
                result["following_count"],
                result["bio"],
                hashtag,
                result["category"],
                result["category_name"],
            )
        ]
        db.insertDB(
            schema="public",
            table="userinfo",
            column="user_id, fullname, is_private, profile_url, media_count, follower_count, following_count, bio, hashtag, category, category_name",
            data=f"'{str(user_id)}', '{result['full_name']}', {result['is_private']}, '{result['profile_url']}', {result['media_count']}, {result['follower_count']}, {result['following_count']}, '{result['bio']}', '{hashtag}', '{result['category']}', '{result['category_name']}'",
        )
