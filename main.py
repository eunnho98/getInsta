from instagrapi import Client
from instagrapi.exceptions import LoginRequired
import logging


class Instagram(Client):
    def __init__(self, username, password):
        super().__init__()
        self.username = username
        self.password = password
        self.logger = logging.getLogger()
        self.delay_range = [3, 6]

    def login_user(self):
        """
        * Try to login with session, if failed then login with PW
        """
        try:
            session = self.load_settings("./session.json")

            login_via_session = False
            login_via_pw = False

            if session:
                try:
                    self.set_settings(session)

                    try:
                        self.get_timeline_feed()  # * 세션이 유효한지 검사
                        print("Session으로 로그인 성공")
                    except LoginRequired:
                        print("세션이 유효하지 않아 ID & PW로 로그인 필요")
                        old_session = self.get_settings()

                        self.set_settings({})
                        self.set_uuids(old_session["uuids"])
                        self.login(self.username, self.password)
                    login_via_session = True
                except Exception as e:
                    print("세션 정보로 로그인 불가: %s" % e)

            if not login_via_session:
                try:
                    print("ID와 PW로 로그인 시도, %s" % USERNAME)
                    if self.login(self.username, self.password):
                        login_via_pw = True
                        self.dump_settings("./session.json")
                        print("ID, PW로 로그인 성공")
                except Exception as e:
                    print("ID와 PW로 로그인 불가: %s" % e)

            if not login_via_pw and not login_via_session:
                raise Exception("PW or Session으로 로그인 불가")

        except FileNotFoundError as e:
            print("최초 로그인")
            self.login(self.username, self.password)
            self.dump_settings("./session.json")


class InstagramUser(Instagram):
    def __init__(self, username, password):
        super().__init__(username, password)

    def get_user_id_by_name(self, name: str) -> int:
        """
        * 유저의 인스타 이름으로 ID 반환
        """
        return self.user_id_from_username(name)

    def get_user_info_by_username(self, name: str) -> dict:
        """
        * 유저에 대한 정보 반환
        """
        data = self.user_info_by_username(name).dict()
        result = {
            "pk": data["pk"],
            "username": data["username"],
            "full_name": data["full_name"],
            "is_private": data["is_private"],
            "profile_url": data["profile_pic_url"],
            "media_count": data["media_count"],
            "follower_count": data["follower_count"],
            "following_count": data["following_count"],
            "bio": data["biography"],
            "category": data["category"],
            "category_name": data["category_name"],
        }
        return result

    def get_user_followers(self, user_id: str, amount: int, know=True) -> dict:
        """
        공개 유저인 경우 지정한 유저의 팔로워 목록 반환

        Args:
            * user_id: str, int에서 변환 필요
            * amount: 가져올 수, 0이면 모든 팔로워 가져옴
            * know: public 여부를 아는지

        Return:
            * Dict[user_id(int), UserShort]
        """
        if know == False:
            data = self.user_info(user_id).dict()
            is_private = data["is_private"]
            if is_private == True:  # 비공개
                raise Exception("사용자가 Private입니다.")

        return self.user_followers(user_id, amount)

    def get_user_followings(self, user_id: str, amount: int, know=True) -> dict:
        """
        공개 유저인 경우 지정한 유저의 팔로잉 목록 반환

        Args:
            * user_id: str, int에서 변환 필요
            * amount: 가져올 수, 0이면 모든 팔로잉 가져옴
            * know: public 여부를 아는지

        Return:
            * Dict[user_id(int), UserShort]
        """
        if know == False:
            data = self.user_info(user_id).dict()
            is_private = data["is_private"]
            if is_private == True:  # 비공개
                raise Exception("사용자가 Private입니다.")

        return self.user_following(user_id, amount)


class InstagramMedia(Instagram):
    """
    Media Types:
        * Photo: media_type=1
        * Video(feed): media_type=2
    """

    def __init__(self, username, password):
        super().__init__(username, password)

    def get_user_medias(self, user_id: str, amount: int, know=True) -> list:
        """
        유저의 미디어 리스트 반환

        Args:
            * user_id: str, int에서 변환 필요
            * amount: 가져올 미디어 수, 최대 20
            * know: public 여부를 아는지

        Return:
            * List[dict()]
        """
        if know == False:
            data = self.user_info(user_id).dict()
            is_private = data["is_private"]
            if is_private == True:  # 비공개
                raise Exception("사용자가 Private입니다.")

        medias = self.user_medias(user_id, amount)

        selected_key = [
            "media_pk",
            "media_id",
            "taken_at",
            "media_type",
            "product_type",
            "thumbnail_url",
            "video_url",
            "comment_count",
            "like_count",
            "caption_text",
            "view_count",
        ]

        result = [
            {key: media.dict().get(key) for key in selected_key} for media in medias
        ]
        return result

    def get_user_reels(self, user_id: str, amount: int, know=True) -> list:
        """
        유저의 릴스 리스트 반환

        Args:
            * user_id: str, int에서 변환 필요
            * amount: 가져올 릴스 수, 최대 20
            * know: public 여부를 아는지

        Return:
            * List[dict()]
        """
        if know == False:
            data = self.user_info(user_id).dict()
            is_private = data["is_private"]
            if is_private == True:  # 비공개
                raise Exception("사용자가 Private입니다.")

        reels = self.user_clips(user_id, amount)

        selected_key = [
            "reels_pk",
            "reels_id",
            "taken_at",
            "media_type",
            "product_type",
            "thumbnail_url",
            "video_url",
            "comment_count",
            "like_count",
            "play_count",
            "caption_text",
        ]

        result = [{key: reel.dict().get(key) for key in selected_key} for reel in reels]
        return result

    def get_media_comments(self, media_id: str, amount: int) -> list:
        """
        게시물의 댓글 목록 반환

        Args:
            * media_id: 미디어의 ID
            * amount: 가져올 댓글 수, 0이면 전부, 최대 99

        Return:
            * List[dict()]
        """
        comments = self.media_comments(media_id, amount)

        selected_key = ["comment_pk", "text", "user", "created_at_utc", "like_count"]
        result = [
            {key: comment.dict().get(key) for key in selected_key}
            for comment in comments
        ]
        return result

    def get_media_likers(self, media_id: str) -> list:
        return self.media_likers(media_id)
