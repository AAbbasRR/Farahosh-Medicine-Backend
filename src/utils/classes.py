from django.core.management import settings

from .functions import create_otp_code
from .data_list import RedisKeys

import redis
import json
import requests


class Redis:
    """
    manage public keys on redis
    """

    cache = redis.StrictRedis(
        decode_responses=True,
        host=settings.REDIS_HOST,
        port=settings.REDIS_PORT,
        db=settings.REDIS_DB,
    )  # config redis system cache
    expire_times = {
        "otp_code": 300,  # 5Min
        "forget_password": 900,  # 15Min
        "change_password": 900,  # 15Min
    }

    def __init__(
        self, mobile, key
    ):  # For the key to be unique, we use the public's email to access the key and a string for the key to be unique and clear.
        self.key = mobile + key

    def set_value(self, value):  # Set a value on the key in Redis
        self.cache.set(self.key, value)

    def set_json_value(
        self, value
    ):  # Set a value on the key in Redis when data is dict or json
        self.set_value(json.dumps(value))

    def set_status_value(self, value):  # Set a bool value on the key in redis
        self.set_value(str(value))

    def create_and_set_otp_key(self, length=5, otp_code=None):
        if otp_code is None:
            otp_code = create_otp_code(length)
        self.set_value(otp_code)
        self.set_expire(self.expire_times["otp_code"])
        return otp_code

    def get_value(self):  # Returns the internal value of the key
        if self.cache.exists(self.key):
            return self.cache.get(self.key)
        else:
            return None

    def get_json_value(self):  # Returns the json value of the key
        try:
            return json.loads(self.get_value())
        except TypeError:
            return None

    def get_status_value(self):  # Returns the True or False status value of the key
        the_value = self.get_value()
        if the_value is not None and str(the_value).upper() == "TRUE":
            return True
        else:
            return False

    def set_expire(
        self, time=300
    ):  # Set a time for the key to expire (time is in seconds)
        self.cache.expire(self.key, time)

    def get_expire(
        self,
    ):  # Returns the number of seconds remaining before the key expires
        return self.cache.ttl(self.key)

    def validate(
        self, user_value
    ):  # Takes an input value and checks to see if it is the same as the value inside the key
        user_value = str(user_value)
        if self.cache.exists(self.key):
            redis_value = self.cache.get(self.key)
            if redis_value == user_value:
                return True
            else:
                return False
        else:
            return None

    def exists(self):  # Checks if the key is there or not
        return self.cache.exists(self.key) == 1

    def delete(self):  # Remove the key from Redis
        return self.cache.delete(self.key)


class ManageSMSPortal:
    def __init__(self, user_mobile, user_type=""):
        self.user_mobile = user_mobile
        self.user_redis_key = f"{user_type}_{user_mobile}"
        self.title_types = {
            "register": "کد تایید حساب کاربری شما",
            "login": "کد ورود به حساب شما",
            "forget_password": "کد تایید فراموشی رمز عبور شما",
            "change_password": "کد تایید تغییر رمز عبور شما",
            "active": "تایید تغییر شماره تلفن شما",
        }

    def send_message(self, message):
        data = {
            "UserName": settings.SMS_PORTAL["username"],
            "Password": settings.SMS_PORTAL["pass"],
            "Mobile": self.user_mobile,
            "Message": message,
        }
        if settings.DEPENDENT_SMS_ON_DEBUG is True and settings.DEBUG is True:
            print(data)
            return True
        else:
            request_response = requests.post(
                "https://raygansms.com/SendMessageWithCode.ashx",
                data=data,
            )
            if request_response.status_code == 200:
                return True
            else:
                return False

    def send_otp_code(self, title_type):
        manage_redis = Redis(self.user_redis_key, RedisKeys.verify_otp_code)
        otp_code = manage_redis.create_and_set_otp_key()
        data = {
            "UserName": settings.SMS_PORTAL["username"],
            "Password": settings.SMS_PORTAL["pass"],
            "Mobile": self.user_mobile,
            "Message": f"بیولایف، {self.title_types[title_type]} {otp_code} میباشد.",
        }
        if settings.DEPENDENT_SMS_ON_DEBUG is True and settings.DEBUG is True:
            print(data)
            return True
        else:
            request_response = requests.post(
                "https://raygansms.com/SendMessageWithCode.ashx",
                data=data,
            )
            if request_response.status_code == 200:
                return True
            else:
                return False

    def check_otp_code_existed(self, title_type):
        manage_redis = Redis(self.user_redis_key, RedisKeys.verify_otp_code)
        return manage_redis.exists()

    def send_auto_otp_code(self):
        request_response = requests.post(
            "https://raygansms.com/AutoSendCode.ashx",
            data={
                "UserName": settings.SMS_PORTAL["username"],
                "Password": settings.SMS_PORTAL["pass"],
                "Mobile": self.user_mobile,
                "Footer": "پلتفرم بیولایف",
            },
        )
        if request_response.status_code == 200:
            return True
        else:
            return False

    def check_auto_otp_code(self, otp_code):
        request_response = requests.post(
            "https://raygansms.com/CheckSendCode.ashx",
            data={
                "UserName": settings.SMS_PORTAL["username"],
                "Password": settings.SMS_PORTAL["pass"],
                "Mobile": self.user_mobile,
                "Code": str(otp_code),
            },
        )
        if request_response.status_code == 200:
            return True
        else:
            return False
