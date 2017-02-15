#coding=utf-8
from __future__ import absolute_import, unicode_literals
# https://github.com/qiniu/python-sdk/blob/master/qiniu/services/storage/uploader.py
from qiniu import Auth,put_file,put_data,BucketManager
from .utils import QiniuError, bucket_lister
from os.path import basename,splitext
from datetime import datetime
   
class QiniuStorage(object):
    def __init__(self,access_key,secret_key,bucket_name,bucket_domain):
        self.auth=Auth(access_key,secret_key)
        self.bucket_name = bucket_name
        self.bucket_domain = bucket_domain
        self.bucket_manager = BucketManager(self.auth)
    
    def put_data(self,name,data):
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
        #上传到七牛后保存的文件名
        key = self._newname(name)  
        #生成上传 Token，可以指定过期时间等
        token=self.auth.upload_token(self.bucket_name,key) 
        if hasattr(data,'chunks'):
            data = b''.join(c for c in data.chunks())
        ret, info = put_data(token, key, data)  #上传文件流到七牛
        if ret is None or ret['key'] != key:
            raise QiniuError(info)
        return self.get_url(key)
        
    def _newname(self,name):
        '''加上6位日期和6位时间标识 PG.jpg --> PG_170211_044217.jpg '''
        root,ext=splitext(basename(name))
        time=datetime.now().strftime('_%y%m%d_%H%M%S')
        return '{}{}{}'.format(root,time,ext)

    def get_url(self,key):    
        url='http://{}/{}'.format(self.bucket_domain,key)
        return url 
            
    def put_file(self,filePath):
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
        key = self._newname(filePath)  
        token=self.auth.upload_token(self.bucket_name,key) 
        ret, info = put_file(token, key, filePath)  
        if ret is None or ret['key'] != key:
            raise QiniuError(info)
        return self.get_url(key)
    
    def exists(self,key):        
        '''检测七牛云上是否有文件名为key的文件'''
        bucket=self.bucket_manager
        ret, info = bucket.stat(self.bucket_name, key.split('/')[-1])
        return ret is not None  

    def delete(self,key):  
        if not self.exists(key):
            return '{} not exist in qiniu_cloud'.format(key)  
        bm=self.bucket_manager
        ret, info = bm.delete(self.bucket_name, key.split('/')[-1])
        if ret == {}:
            return 'success to delete {} in qiniu_cloud'.format(key)
        else:
            return info    

    def ls_files(self,prefix="", limit=None):
        """前缀查询(列出七牛云存储空间里的前缀为prefix的所有文件）:            
        具体规格参考:
        http://developer.qiniu.com/docs/v6/api/reference/rs/list.html
        Args:            
            prefix:     列举前缀            
            limit:      单次列举个数限制            
        Returns:
            文件名列表
        """
        files=set() 
        dirlist = bucket_lister(self.bucket_manager, self.bucket_name,
                                prefix,limit) 
        for item in dirlist:
            files.add(item['key'])        
        return files
                 

