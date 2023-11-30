from django.utils.translation import gettext as _


class RedisKeys:
    verify_otp_code = "verify_otp_code"
    lock_wrong_try_otp_code_verify = "lock_wrong_try_otp_code_verify"
    activate_account = "activate_account"
    forget_password = "forget_password"
    change_password = "change_password"
    login_register = "login_register"
    deposit = "deposit_to_wallet"
    cart = "cart_products"
    submit_order_with_online_gateway = "submit_order_with_online_gateway"
    user_registration = "user_registration_data"
    cart_product_inventory_saver = "cart_product_inventory_saver"

    lock_wrong_try_otp_code_verify_expire = 300  # 5min

    deposit_expire = 1200
    sms_login_expire = 120
    cart_product_expire = 43200
    registration_expire = 240
