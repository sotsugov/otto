import os
import base64
import hashlib
import hmac
import urllib
import time
import requests


class OttoApi:
    def __init__(
        self,
        api_key: str = "",
        api_secret: str = "",
        api_password: str = "",
        api_url: str = "",
    ) -> None:

        self.api_key = api_key
        self.api_secret = api_secret
        self.api_password = api_password
        self.api_url = api_url
        self.api_version = 0

    def read_keys(self) -> None:
        self.api_url = os.environ.get("OTTO_URL", "")
        self.api_key = os.environ.get("OTTO_KEY", "")
        self.api_secret = os.environ.get("OTTO_SECRET", "")
        self.api_password = os.environ.get("OTTO_OTP", "")
        if not self.api_key or not self.api_secret:
            raise Exception("Missing api key or secret")

    def _sign_request(self, api_path: str, data: dict) -> str:
        post_data = urllib.parse.urlencode(data)
        encoded = (str(data["nonce"]) + post_data).encode()
        message = api_path.encode() + hashlib.sha256(encoded).digest()
        signature = hmac.new(base64.b64decode(self.api_secret), message, hashlib.sha512)
        sig_digest = base64.b64encode(signature.digest())
        return sig_digest.decode()

    def _request(self, url: str, headers: dict = None, data: dict = None) -> dict:
        if not data:
            data = {}
        if not headers:
            headers = {}

        uri = f"{self.api_url}/{url}"

        response = requests.post(uri, headers=headers, data=data)
        if response.status_code not in (200, 201, 202):
            response.raise_for_status()

        if len(response.json()["error"]) > 0:
            raise Exception(response.json()["error"])

        return response.json()["result"]

    def public_request(self, method: str, data: dict = None) -> dict:
        if not data:
            data = {}
        url = f"/{self.api_version}/public/{method}"
        return self._request(url, data)

    def private_request(self, method: str, data: dict = None) -> dict:
        if not data:
            data = {}

        data["nonce"] = int(1000 * time.time())

        if self.api_password:
            data["otp"] = self.api_password

        url = f"/{self.api_version}/private/{method}"
        headers = {
            "API-Key": self.api_key,
            "API-Sign": self._sign_request(url, data),
        }

        return self._request(url, headers, data)


if __name__ == "__main__":
    otto = OttoApi()
    otto.read_keys()

    print(otto.public_request("Time"))
    print(otto.private_request("Balance"))
