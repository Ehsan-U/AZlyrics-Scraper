from rotating_proxies.policy import BanDetectionPolicy

class AZ_policy(BanDetectionPolicy):

    def response_is_ban(self, request, response):
        default_ban_checks = super(AZ_policy, self).response_is_ban(request, response)
        ban = (default_ban_checks) or ("verify" in response.text.lower() and "human" in response.text.lower())
        # True > ban detected
        # False > not detected
        return ban

    def exception_is_ban(self, request, exception):
        return None