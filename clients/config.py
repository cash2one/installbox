#!/usr/bin/python
#coding=utf8

'''配置文件'''

settings = {
    'api_url' : 'http://api.ucenter.playcrab.com/',
    'api_key' : '3158308647',
    'api_secret_key' : '454fceaa64e202256b295a7184272af4'
}

# settings = {
#     'api_url' : 'http://119.254.111.26:8086/',
#     'api_key' : '4190854055',
#     'api_secret_key' : 'b08be6a42e7d86a7a57557dfc3afdd7b'
# }


class Url_some(object):
    def __init__(self):
        self.root=os.getcwd()
        self.DataSome=self.root+"/static/FileSome/DataSome.yaml"
        self.fileDatasome=self.root+"/static/FileSome/fileDatasome.yaml"
        self.game_category=self.root+"/static/FileSome/game_category.txt"
        self.korea=self.root+"/static/FileSome/korea.yaml"
        self.platform_category=self.root+"/static/FileSome/platform_category.txt"
        self.testshell=self.root+"/static/FileSome/testshell.sh"
