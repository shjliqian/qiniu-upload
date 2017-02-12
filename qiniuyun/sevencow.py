#coding=utf-8

from qiniu import Auth,put_file,put_data,BucketManager
# from django.conf import settings
from yuntest.local_settings import qiniu_keys,qiniu_bucket
from os.path import basename,splitext
from datetime import datetime
from time import sleep

#解析结果
def parseRet(retData,respInfo):
    if retData!=None:
        print("Upload file to qiniu_cloud success!")
        print("Hash: {}".format(retData["hash"]))
        print('Kety: {}'.format(retData['key']))
        #检查扩展参数
        for k,v in retData.items():
            if k[:2]=='x:':
                print('{}:{}'.format(k,v))
        #检查其他参数        
        for k,v in retData.items():
            if k[:2]=='x:' or k=='hash' or k=='key':
                continue
            else:
                print('{}:{}'.format(k,v))

    else:
        print('Upload file to qiniu_cloud failed!')
        print('Error: {}'.format(respInfo))
        #print('Error: {}'.format(respInfo.text_body))

def upload_qiniu(filePath):
    """本地文件上传:
        1. 目标域名和空间在local_settings.py中设置
        2. 备案网站域名后，可提高上传速度和稳定性
        3、空间里的文件名不能重复，所以加上6位日期和6位时间标识
            'PG.jpg' --> 'PG_170211_044217.jpg'        
        具体参考:
        https://developer.qiniu.com/kodo/sdk/python
        Args:            
            filePath: 待上传文件在磁盘中的绝对路径                             
        Return:
            上传后的url路径
        """
    #构建鉴权对象
    q=Auth(**qiniu_keys)    
    #上传到七牛后保存的文件名
    root,ext=splitext(basename(filePath))
    time=datetime.now().strftime('%y%m%d_%H%M%S')
    key = '{}_{}{}'.format(root,time,ext)
    #生成上传 Token，可以指定过期时间等
    token=q.upload_token(qiniu_bucket['name'],key)
    #要上传文件的本地路径
    localfile = filePath
    #上传文件到七牛
    ret, info = put_file(token, key, localfile)    
#    parseRet(ret,info) #解析上传结果    
    return get_url_qiniu(key)

def upload_data_qiniu(name,data):
    """文件流上传:
        1. 目标域名和空间在local_settings.py中设置
        2. 备案网站域名后，可提高上传速度和稳定性
        3、空间里的文件名不能重复，所以加上6位日期和6位时间标识
            'PG.jpg' --> 'PG_170211_044217.jpg'        
        具体参考:
        https://developer.qiniu.com/kodo/sdk/python
        Args:            
            name: 文件名   
            data: 上传二进制流                      
        Return:
            上传后的url路径
        """
    #构建鉴权对象
    q=Auth(**qiniu_keys)    
    #上传到七牛后保存的文件名
    root,ext=splitext(basename(name))
    time=datetime.now().strftime('%y%m%d_%H%M%S')
    key = '{}_{}{}'.format(root,time,ext)
    #生成上传 Token，可以指定过期时间等
    token=q.upload_token(qiniu_bucket['name'],key)    
    #上传文件到七牛
    ret, info = put_data(token, key, data)    
#    parseRet(ret,info) #解析上传结果    
    return get_url_qiniu(key)
    
def get_url_qiniu(key):    
    url='http://{}/{}'.format(qiniu_bucket['domain'],key)
    return url

def exists_qiniu(key):
    q=Auth(**qiniu_keys)
    bucket=BucketManager(q)
    #获取文件的状态信息
    ret, info = bucket.stat(qiniu_bucket['name'], key.split('/')[-1])
    return ret is not None
    
def delete_qiniu(key):  
    if not exists_qiniu(key):
        return '{} not exist in qiniu_cloud'.format(key)  
    q=Auth(**qiniu_keys)
    bucket=BucketManager(q)    
    ret, info = bucket.delete(qiniu_bucket['name'], key.split('/')[-1])
    if ret == {}:
        return 'success to delete {} in qiniu_cloud'.format(key)
    else:
        return info

def list_qiniu(prefix="", limit=100):
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
    q=Auth(**qiniu_keys)
    bucket=BucketManager(q)
    marker = None
    eof = False
    while eof is False:
        ret, eof, info = bucket.list(qiniu_bucket['name'], 
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
    for i,f in enumerate(list_qiniu(),1):
        print i,'、',f
    filePath='/home/willie/Downloads/PG.jpg'
    url=upload_qiniu(filePath)
    print url    
    sleep(3)    
    assert exists_qiniu(url)
    print list_qiniu()
    assert delete_qiniu(url)=='success to delete {} in qiniu_cloud'.format(url)    
    assert exists_qiniu(url)==False
    assert delete_qiniu(url)=='{} not exist in qiniu_cloud'.format(url)
    print list_qiniu()

if __name__=='__main__':
    main()
