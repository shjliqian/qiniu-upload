#coding=utf-8

from qiniu import Auth,put_file,put_data,BucketManager
from django.conf import settings
from os.path import basename,splitext
from datetime import datetime
from time import sleep

class QiniuStorage(object):
    def __init__(self,access_key,secret_key,bucket_name,bucket_domain):
        self.auth=Auth(access_key,secret_key)
        self.bucket_name = bucket_name
        self.bucket_domain = bucket_domain
        self.bucket_manager = BucketManager(self.auth)

    def upload_data(self,name,data):
        """文件流上传:
        1. 目标域名和空间在local_settings.py中设置
        2. 备案网站域名后，可提高上传速度和稳定性
        3、空间里的文件名不能重复，所以用_newname生成新文件名                                  
        Args:            
            name: 文件名   
            data: 上传二进制流                      
        Return:
            上传后的url路径
        """
        # 七牛put_data源码：
        # https://github.com/qiniu/python-sdk/blob/master/qiniu/services/storage/uploader.py
        
        key = self._newname(name)  #上传到七牛后保存的文件名
        token=self.auth.upload_token(self.bucket_name,key) #生成上传 Token，可以指定过期时间等
        ret, info = put_data(token, key, data)  #上传文件到七牛
        #self._parseRet(ret,info) #解析上传结果  
        return self.get_url(key)
        
    def _newname(self,name):
        '''加上6位日期和6位时间标识 PG.jpg --> PG_170211_044217.jpg '''
        root,ext=splitext(basename(name))
        time=datetime.now().strftime('_%y%m%d_%H%M%S')
        return '{}{}{}'.format(root,time,ext)

    def get_url(self,key):    
        url='http://{}/{}'.format(self.bucket_domain,key)
        return url 
            
    def upload(self,filePath):
        """本地文件上传:
        1. 目标域名和空间在local_settings.py中设置
        2. 备案网站域名后，可提高上传速度和稳定性
        3、空间里的文件名不能重复，所以用_newname生成新文件名  
        具体参考:
        https://developer.qiniu.com/kodo/sdk/python
        Args:            
            filePath: 待上传文件在磁盘中的绝对路径                             
        Return:
            上传后的url路径
        """        
        key = self._newname(filePath)  #上传到七牛后保存的文件名
        token=self.auth.upload_token(self.bucket_name,key) #生成上传 Token，可以指定过期时间等
        ret, info = put_file(token, key, filePath)  #上传文件到七牛
        #self._parseRet(ret,info) #解析上传结果  
        return self.get_url(key)
    
    def exists(self,key):        
        '''检测七牛云上是否有文件名为key的文件'''
        bucket=self.bucket_manager
        ret, info = bucket.stat(self.bucket_name, key.split('/')[-1])
        return ret is not None  

    def delete(self,key):  
        if not self.exists(key):
            return '{} not exist in qiniu_cloud'.format(key)           
        ret, info = self.bucket_manager.delete(self.bucket_name, key.split('/')[-1])
        if ret == {}:
            return 'success to delete {} in qiniu_cloud'.format(key)
        else:
            return info    

    def ls_files(self,prefix="", limit=100):
        """前缀查询(列出七牛云存储空间里的前缀为prefix的所有文件）:
        1. 无论 err 值如何，均应该先看 ret.get('items') 是否有内容
        2. 如果后续没有更多数据，err 返回 EOF（但不通过该特征来判断是否结束）        
        具体规格参考:
        http://developer.qiniu.com/docs/v6/api/reference/rs/list.html
        Args:            
            prefix:     列举前缀            
            limit:      单次列举个数限制            
        Returns:
            文件名列表
        """
        rlist=[]    
        bucket=self.bucket_manager
        marker = None
        eof = False
        while eof is False:
            ret, eof, info = bucket.list(self.bucket_name, 
                prefix=prefix, marker=marker, limit=limit)
            marker = ret.get('marker', None)
            for item in ret['items']:
                rlist.append(item["key"])
        if eof is not True:
            # 错误处理
            #print "error"
            pass
        return rlist
                 
def main():
    sevencow=QiniuStorage(**settings.QINIU_SET)
    for i,f in enumerate(sevencow.ls_files(),1):
        print i,'、',f
    filePath='/home/willie/Downloads/PG.jpg'
    url=sevencow.upload(filePath)
    print url    
    sleep(3)    
    assert sevencow.exists(url)
    print sevencow.ls_files()
    assert sevencow.delete(url)=='success to delete {} in qiniu_cloud'.format(url)    
    assert sevencow.exists(url)==False
    assert sevencow.delete(url)=='{} not exist in qiniu_cloud'.format(url)
    print sevencow.ls_files()

if __name__=='__main__':
    main()
    
'''不能直接python backends.py
需python manage.py shell
...
from qiniuyun import backends as ba
ba.main()
'''
