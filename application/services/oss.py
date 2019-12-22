import oss2
from config.private_data import sms_service_info

__auth = oss2.Auth(sms_service_info['AccessKeyID'], sms_service_info['AccessKeySecret'])
__bucket = oss2.Bucket(__auth, 'http://oss-cn-shanghai.aliyuncs.com', 'yh0x13f-bucket')
