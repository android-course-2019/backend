import base64
import collections
import hmac
import random
import requests
import uuid
from datetime import datetime
from hashlib import sha1
from urllib.parse import urlencode, quote_plus

from application.config.private_data import sms_service_info


def send_sms(phone):
    random.seed()
    code = '{:06d}'.format(random.randrange(0, 1000000))

    params = {
        "AccessKeyId": sms_service_info['AccessKeyID'],
        "Timestamp": datetime.utcnow().isoformat(timespec='seconds') + 'Z',
        "Format": "JSON",
        "SignatureMethod": "HMAC-SHA1",
        "SignatureVersion": "1.0",
        "SignatureNonce": str(uuid.uuid4()),
        "Action": "SendSms",

        "Version": "2017-05-25",
        "RegionId": "cn-hangzhou",
        "PhoneNumbers": phone,
        "SignName": "yh0x13f",
        "TemplateCode": "SMS_175541886",
        "TemplateParam": "{{\"code\":\"{}\"}}".format(code)
    }

    params = collections.OrderedDict(sorted(params.items(), key=lambda item: item[0]))

    query_string = "&" \
        .join(["{}={}"
              .format(__special_url_string_encoder(item[0]),
                      __special_url_string_encoder(item[1]))
               for item in params.items()])

    string_to_sign = "GET&%2F&{}".format(__special_url_string_encoder(query_string))
    params['Signature'] = __sign(string_to_sign)

    response = requests.get("https://dysmsapi.aliyuncs.com?{}".format(__special_url_encoder(params)))
    res_data = response.json()
    if res_data['Code'] == "OK":
        return True, code
    else:
        return False, res_data['Message']


def __special_url_encoder(data):
    return urlencode(data, quote_via=__special_url_string_encoder)


def __special_url_string_encoder(string, safe='', encoding=None, errors=None):
    return quote_plus(string, safe, encoding, errors).replace("+", "%20").replace("*", "%2A").replace("%7E", "~")


def __sign(string_to_sign):
    return base64.encodebytes(
        hmac.new(
            (sms_service_info['AccessKeySecret'] + "&").encode(),
            string_to_sign.encode(),
            sha1
        ).digest()).decode().replace("\n", "")
