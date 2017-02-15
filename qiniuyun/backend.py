#coding=utf-8
from django.conf import settings
from .qiniustorage import QiniuStorage
from time import sleep

def get_qiniu_config(cnf):
    return getattr(settings,cnf) 
       
QINIU_ACCESS_KEY = get_qiniu_config('QINIU_ACCESS_KEY')
QINIU_SECRET_KEY = get_qiniu_config('QINIU_SECRET_KEY')
QINIU_BUCKET_NAME = get_qiniu_config('QINIU_BUCKET_NAME')
QINIU_BUCKET_DOMAIN = get_qiniu_config('QINIU_BUCKET_DOMAIN')
    
class QiniuPush(QiniuStorage):
    def __init__(self):
        super(QiniuPush,self).__init__(**settings.QINIU_CONF)
            
    @classmethod
    def put_data(cls,name,data):
        '''上传内存中的文件流到七牛并返回上传后的url地址'''
        qn=cls()
        return super(QiniuPush,qn).put_data(name,data)

    @classmethod            
    def put_file(cls,filePath):
        '''上传本地文件到七牛并返回上传后的url地址'''
        qn=cls()
        return super(QiniuPush,qn).put_file(filePath)
        
    @classmethod
    def exists(cls,key):        
        '''检测七牛云上是否有文件名为key的文件'''
        qn=cls()
        return super(QiniuPush,qn).exists(key)  
        
    @classmethod
    def delete(cls,key):  
        '''删除七牛云上文件名为key的文件'''
        qn=cls()
        return super(QiniuPush,qn).delete(key) 
          
    @classmethod
    def ls_files(cls,prefix="", limit=100):
        '''列出七牛云上的所有文件(前100个)'''
        qn=cls()
        return super(QiniuPush,qn).ls_files()
                 
def main():    
    for i,f in enumerate(QiniuPush.ls_files(),1):
        print i,'、',f
    filePath='/home/willie/Downloads/PG.jpg'
    url=QiniuPush.put_file(filePath) 
    with open(filePath,'rb') as f:
        url2=QiniuPush.put_data(filePath,f.read())
        #or: url2=QiniuPush.put_data(filePath.split('/')[-1],f.read())
    print url,'\n',url2    
    sleep(3)    
    assert QiniuPush.exists(url)
    for i,f in enumerate(QiniuPush.ls_files(),1):
        print i,'、',f
    print QiniuPush.delete(url)    
    assert QiniuPush.exists(url)==False
    assert QiniuPush.delete(url)=='{} not exist in qiniu_cloud'.format(url)
    for i,f in enumerate(QiniuPush.ls_files(),1):
        print i,'、',f

if __name__=='__main__':
    main()
    
'''不能直接python backend.py
需在上一级目录python manage.py shell
...
from qiniuyun import backend as ba
ba.main()
'''
