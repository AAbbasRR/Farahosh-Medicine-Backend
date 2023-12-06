class RedisKeys:
    list_all_data = "list_all_data"
    verify_otp_code = "verify_otp_code"
    lock_wrong_try_otp_code_verify = "lock_wrong_try_otp_code_verify"

    lock_wrong_try_otp_code_verify_expire = 300  # 5min
