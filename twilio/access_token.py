import time
import jwt


class IpMessagingGrant(object):
    def __init__(self, service_sid=None, endpoint_id=None,
                 role_sid=None, credential_sid=None):
        self.service_sid = service_sid
        self.endpoint_id = endpoint_id
        self.role_sid = role_sid
        self.credential_sid = credential_sid

    @property
    def key(self):
        return "ip_messaging"

    def to_payload(self):
        grant = {}
        if self.service_sid:
            grant['service_sid'] = self.service_sid
        if self.endpoint_id:
            grant['endpoint_id'] = self.endpoint_id
        if self.role_sid:
            grant['deployment_role_sid'] = self.role_sid
        if self.credential_sid:
            grant['push_credential_sid'] = self.credential_sid

        return grant


class ConversationGrant(object):
    def __init__(self, configuration_profile_sid=None):
        self.configuration_profile_sid = configuration_profile_sid

    @property
    def key(self):
        return "rtc"

    def to_payload(self):
        grant = {}
        if self.configuration_profile_sid:
            grant['configuration_profile_sid'] = self.configuration_profile_sid

        return grant


class AccessToken(object):
    def __init__(self, signing_key_sid, account_sid, secret,
                 identity=None, ttl=3600):
        self.signing_key_sid = signing_key_sid
        self.account_sid = account_sid
        self.secret = secret

        self.identity = identity
        self.ttl = ttl
        self.grants = []

    def add_grant(self, grant):
        self.grants.append(grant)

    def to_jwt(self, algorithm='HS256'):
        now = int(time.time())
        headers = {
            "typ": "JWT",
            "cty": "twilio-fpa;v=1"
        }

        grants = {}
        if self.identity:
            grants["identity"] = self.identity

        for grant in self.grants:
            grants[grant.key] = grant.to_payload()

        payload = {
            "jti": '{0}-{1}'.format(self.signing_key_sid, now),
            "iss": self.signing_key_sid,
            "sub": self.account_sid,
            "nbf": now,
            "exp": now + self.ttl,
            "grants": grants
        }

        return jwt.encode(payload, self.secret, headers=headers)

    def __str__(self):
        return self.to_jwt().decode('utf-8')
