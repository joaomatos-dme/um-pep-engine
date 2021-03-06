#!/usr/bin/env python3

from base64 import b64encode
from WellKnownHandler import TYPE_OIDC, KEY_OIDC_TOKEN_ENDPOINT, KEY_OIDC_USERINFO_ENDPOINT, KEY_OIDC_CLIENTINFO_ENDPOINT

import requests

class OIDCHandler:

    def __init__(self, wkh, client_id: str, client_secret: str, redirect_uri: str, scopes, verify_ssl: bool = False):
        self.client_id = client_id
        self.client_secret = client_secret
        self.verify_ssl = verify_ssl
        self.redirect_uri = redirect_uri
        self.scopes = scopes
        self.wkh = wkh

    def get_new_pat(self):
        """
        Returns a new PAT
        """
        token_endpoint = self.wkh.get(TYPE_OIDC, KEY_OIDC_TOKEN_ENDPOINT)
        headers = {"content-type": "application/x-www-form-urlencoded", 'cache-control': "no-cache"}
        payload = "grant_type=client_credentials&client_id="+self.client_id+"&client_secret="+self.client_secret+"&scope="+" ".join(self.scopes).replace(" ","%20")+"&redirect_uri="+self.redirect_uri
        response = requests.post(token_endpoint, data=payload, headers=headers, verify = self.verify_ssl)
        
        try:
            access_token = response.json()["access_token"]
        except Exception as e:
            print("Error while getting access_token: "+str(response.text))
            exit(-1)
        
        return access_token

    def is_pat_valid(self, pat_token):
        """
        Verifies if the given pat token is valid
        """
        userinfo_endpoint = self.wkh.get(TYPE_OIDC, KEY_OIDC_USERINFO_ENDPOINT)
        clientinfo_endpoint = self.wkh.get(TYPE_OIDC, KEY_OIDC_CLIENTINFO_ENDPOINT)
        headers = {"content-type": "application/x-www-form-urlencoded", 'cache-control': "no-cache"}
        payload = {"access_token": pat_token}
        r = requests.get(clientinfo_endpoint, params=payload, headers=headers, verify=self.verify_ssl)
        if (r.status_code == 200):
            return True
        r = requests.get(userinfo_endpoint, params=payload, headers=headers, verify=self.verify_ssl)
        if (r.status_code == 200):
            return True
        return False
            
