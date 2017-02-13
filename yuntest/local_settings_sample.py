#coding=utf-8
email_conf={}
email_conf["EMAIL_BACKEND"] = 'django.core.mail.backends.smtp.EmailBackend' #email后端
 
email_conf["EMAIL_USE_TLS"] = False  #是否使用TLS安全传输协议
email_conf["EMAIL_USE_SSL"] = True    #是否使用SSL加密，qq企业邮箱要求使用，网易邮箱则不需要
email_conf["EMAIL_HOST"] = 'smtp.126.com'   #发送邮件的邮箱 的 SMTP服务器
email_conf["EMAIL_PORT"] = 25    #发件箱的SMTP服务器端口
email_conf["EMAIL_HOST_USER"] = 'jaket5219999@126.com'   #发送邮件的邮箱地址
email_conf["EMAIL_HOST_PASSWORD"] = '****'       #发送邮件的邮箱密码
email_conf["DEFAULT_FROM_EMAIL"] = 'jaket5219999@126.com'      #这项可要可不要

qiniu_keys={}
#七牛云存储的权限校验机制基于一对密钥，分别称为Access Key和Secret Key。其中Access Key是公钥，Secret Key是私钥。这一对密钥可以从七牛的后台获取。
qiniu_keys['access_key']="-2E2wJUzd-EXy7Yfimpv4OoCVJrWt2OBDzfUmiqb"
qiniu_keys['secret_key']="1idK013nXsDQEnyvhLxxKm0mKLGwZ4e9ZhBGu_BC"
qiniu_bucket={}
qiniu_bucket['bucket_name']='ziyituixun'   #要上传的空间  
qiniu_bucket['bucket_domain']='okw0cf8ob.bkt.clouddn.com'    #获取文件url路径时对应的私有域名
qiniu_set=dict(qiniu_keys,**qiniu_bucket)    #so pythonic to add two dict
