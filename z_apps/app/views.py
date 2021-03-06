#!/usr/bin/python
#coding=utf8

#show
import re
import json
import yaml
import re
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import os
from django.http import HttpResponse
from django.views.generic import TemplateView, FormView
import subprocess
from z_apps.base.views import JSONResponseMixin
from z_apps.zapp_tools.views import Api
from clients.config import Url_some
Url=Url_some()


class JsonRes(HttpResponse):
    def __init__(self,
            content={},
            status=None,
            content_type='application/json'):

        super(JsonRes, self).__init__(
            json.dumps(content),
            status=status,
            content_type=content_type)

class FileDetach(object):
    '''文件操作'''
    def __init__(self):
        self.ip_inner=[]
        self.ip_public=[]
        self.Node=[]
        self.FiDataSome={}
        self.FDList={}


    def ReadYaml(self,FileName):
        '''读取yaml文件'''
        YamlMsg = yaml.load(file(FileName))
        self.ip_public=YamlMsg.get("ip_public")
        self.ip_inner=YamlMsg.get("ip_inner")
        return self.ip_public,self.ip_inner


    def ReadFile(self,FileName):
        '''读取普通文件'''
        Fn=open(FileName,'r+')
        Fn_some=Fn.read()
        return Fn_some


    def RsWriteYaml(self,FileName,DataSome):
        '''写yaml文件'''
        FileSome=open(FileName,'r')
        YamlMsg = yaml.load(FileSome)

        if YamlMsg is None:
            YamlMsg={}
            self.FDList.setdefault("%s"%DataSome.get("Node"),DataSome.get("strategy"))
            YamlMsg.setdefault("%s"%(DataSome.get("PintList")),self.FDList)
        else:
            Tf=YamlMsg.get(DataSome.get("PintList"),None)
            if Tf is None:
                self.FDList.setdefault("%s" % DataSome.get("Node"), DataSome.get("strategy"))

                YamlMsg.setdefault("%s" % (DataSome.get("PintList")), self.FDList)
            else:
                self.FDList.setdefault("%s" % DataSome.get("Node"), DataSome.get("strategy"))
                dic = dict(Tf.items() + self.FDList.items())

                YamlMsg["%s"%(DataSome.get("PintList"))]=dic

        Fn = open(FileName, 'w')
        yaml.dump(YamlMsg, default_flow_style=False,stream=Fn, indent=4, encoding='utf-8', allow_unicode=True)
        Fn.close()
        FileSome.close()


    def RemoveYaml(self,FileName,PintList,NodeName):
        '''删除节点'''
        FileSome=open(FileName,'r')
        YamlMsg=yaml.load(FileSome)
        print("YamlMsg",YamlMsg,FileName)
        if not YamlMsg is None and not YamlMsg.get("%s"%PintList) is None:
            YamlMsg.get("%s"%PintList,"").pop("%s"%NodeName,"")

        Fn = open(FileName,"w")
        yaml.dump(YamlMsg, default_flow_style=False,stream=Fn, indent=4, encoding='utf-8', allow_unicode=True)
        Fn.close()
        FileSome.close()



    def ReadYaml_datasome(self,FileName):
        YamlFile=open(FileName,'r')
        YamlMsg = yaml.load(YamlFile)
        YamlFile.close()
        return YamlMsg




class CollectionView(TemplateView):
    '''采集地址管理'''
    template_name="z_app/ip_list.html"

    def __init__(self):
        self.FileAdress=Url.korea
        self.File_gamename = Url.game_category
        self.Fd=FileDetach()

    def TakeMsg(self):
        '''返回ip_inner,ip_public'''
        ip_public,ip_inner=self.Fd.ReadYaml(self.FileAdress)
        Ip_msg=[]

        for i in range(len(ip_inner)):
            Ip_msg.append({
                "ip_inner":ip_inner[i],
                "ip_public":ip_public[i]
            })
        return Ip_msg

    def Game_name(self):
        '''游戏名称,在文件中获取'''
        Fn_some=self.Fd.ReadFile(self.File_gamename)[:-1]
        return Fn_some


    def PlatFrom_name(self):
        '''平台名称,为文件名'''
        FileName=(self.FileAdress.split("/")[-1]).split(".")[0]
        return FileName

    def get_context_data(self, **kwargs):
        context = super(CollectionView, self).get_context_data(**kwargs)

        context['ip_msg']=self.TakeMsg()
        context['PlatFrom']=self.PlatFrom_name()
        context['Fn_some'] =self.Game_name()
        return context




class NodeView(TemplateView):
    '''采集节点管理'''
    template_name = "z_app/node.html"

    def __init__(self):
        self.FileAdress = Url.DataSome


    def TakeMsg(self):
        '''遍历文件内容'''
        FileList=[]


        Fd = FileDetach()

        FileSome = Fd.ReadYaml_datasome(self.FileAdress)

        if FileSome is not None:
            for k,v in FileSome.items():
                for l,j in v.items():
                    FileList.append({
                        "PintList":k,
                        "Node": l,
                        "strategy": j,
                    })
        return FileList


    def get_context_data(self, **kwargs):
        context = super(NodeView, self).get_context_data(**kwargs)
        context['Node'] = self.TakeMsg()
        return context



class DeltepNode(TemplateView):
    '''节点删除'''
    def __init__(self):
        self.Fd = FileDetach()
        self.FileName = Url.DataSome

    def post(self,request):
        NodeName=request.POST.get("NodeName")
        PintList=request.POST.get("PintList")

        if NodeName is not None and PintList is not None:
            self.Fd.RemoveYaml(self.FileName,PintList,NodeName)
            return JsonRes(json.dumps({"NodeName":NodeName}))
        else:
            return JsonRes(json.dumps("0401"))



class NodepAdd(FormView):
    '''接受参数写入yaml文件'''

    def __init__(self):
        self.Fd=FileDetach()
        self.FileName=Url.DataSome
        self.zhPattern = re.compile(u'[\u4e00-\u9fa5]+')

    def check_contain_chinese(self,check_str):
        for ch in check_str.decode('utf-8'):
            if u'\u4e00' <= ch <= u'\u9fff':
                return True
        return False

    def post(self, request):
        PintList = request.POST.get("PintList")
        Node = request.POST.get("Node")
        strategy = request.POST.get("strategy")

        PintList_bool=self.check_contain_chinese(PintList)
        Node_bool = self.check_contain_chinese(Node)
        strategy_bool = self.check_contain_chinese(strategy)

        if PintList_bool==True:
            pass
        else:
            PintList=PintList.encode("utf-8")

        if Node_bool==True:
            pass
        else:
            Node=Node.encode("utf-8")

        if strategy_bool==True:
            pass
        else:
            strategy=strategy.encode("utf-8")

        DataSome={
            "PintList":PintList,
            "Node":Node,
            "strategy":strategy
        }
        # print ("DataSome",type(Node),type(PintList),type(strategy))
        print("NodeAdd")
        self.Fd.RsWriteYaml(self.FileName,DataSome)
        return JsonRes(json.dumps(DataSome))




class DeployView(TemplateView):
    '''配置文件修改'''
    template_name = "z_app/deploy.html"

    def __init__(self):
        self.File_gamename = Url.game_category
        self.Fd = FileDetach()
        self.Fn_some = self.Fd.ReadFile(self.File_gamename)[:-1]
        self.GameCategary = ''
        self.PlatForms = ''
        self.Api_show=Api()
        self.PlatName_list=[]


    def GameId_fun(self):
        '''获取游戏id'''
        self.GameCategary = '{"jsonrpc":"2.0","method":"getCategories","params":{"prefix":"%s"}}' % self.Fn_some
        Pita = self.Api_show.get_data(json_str=self.GameCategary)
        Game_id=Pita.get('result')[0].get('id')
        return Game_id


    def PlatForm_fun(self):
        '''通过id获取游戏平台数据集合'''

        Game_id=self.GameId_fun()
        self.PlatForms='{"jsonrpc":"2.0","method":"getPlatforms","params":{"main_category_id":"%s"}}' % Game_id
        PlatSome=(self.Api_show.get_data(json_str=self.PlatForms)).get('result')
        for i in range(len(PlatSome)):
            self.PlatName_list.append({
                "name":PlatSome[i].get('prefix')
            })

        return self.PlatName_list


    def get_context_data(self, **kwargs):
        context = super(DeployView, self).get_context_data(**kwargs)
        context['PlatName_list'] = self.PlatForm_fun()
        return context










class FailNodeView(TemplateView):
    '''失败节点管理页面'''
    template_name = "z_app/fillnode.html"

    def __init__(self):
        self.FileAdress = Url.fileDatasome


    def TakeMsg(self):
        '''遍历文件内容'''
        FileList=[]


        Fd = FileDetach()

        FileSome = Fd.ReadYaml_datasome(self.FileAdress)

        if FileSome is not None:
            for k,v in FileSome.items():
                for l,j in v.items():
                    FileList.append({
                        "PintList":k,
                        "Node": l,
                        "strategy": j,
                    })

        return FileList


    def get_context_data(self, **kwargs):
        context = super(FailNodeView, self).get_context_data(**kwargs)
        context['Node'] = self.TakeMsg()
        return context







class FileDeployView(TemplateView):
    '''失败配置文件修改页面'''
    template_name = "z_app/filldeploy.html"

    def __init__(self):
        self.File_gamename = Url.game_category
        self.Fd = FileDetach()
        self.Fn_some = self.Fd.ReadFile(self.File_gamename)[:-1]
        self.GameCategary = ''
        self.PlatForms = ''
        self.Api_show=Api()
        self.PlatName_list=[]


    def GameId_fun(self):
        '''获取游戏id'''
        self.GameCategary = '{"jsonrpc":"2.0","method":"getCategories","params":{"prefix":"%s"}}' % self.Fn_some
        Pita = self.Api_show.get_data(json_str=self.GameCategary)
        Game_id=Pita.get('result')[0].get('id')
        return Game_id


    def PlatForm_fun(self):
        '''通过id获取游戏平台数据集合'''

        Game_id=self.GameId_fun()
        self.PlatForms='{"jsonrpc":"2.0","method":"getPlatforms","params":{"main_category_id":"%s"}}' % Game_id
        PlatSome=(self.Api_show.get_data(json_str=self.PlatForms)).get('result')

        for i in range(len(PlatSome)):
            self.PlatName_list.append({
                "name":PlatSome[i].get('prefix')
            })

        return self.PlatName_list


    def get_context_data(self, **kwargs):
        context = super(FileDeployView, self).get_context_data(**kwargs)
        context['PlatName_list'] = self.PlatForm_fun()
        return context






class FillNodeAdd(TemplateView):
    '''失败节点添加'''

    def __init__(self):
        self.Fd=FileDetach()
        self.FileName=Url.fileDatasome
        self.zhPattern = re.compile(u'[\u4e00-\u9fa5]+')

    def check_contain_chinese(self,check_str):
        for ch in check_str.decode('utf-8'):
            if u'\u4e00' <= ch <= u'\u9fff':
                return True
        return False

    def post(self, request):
        PintList = request.POST.get("PintList")
        Node = request.POST.get("Node")
        strategy = request.POST.get("strategy")

        PintList_bool=self.check_contain_chinese(PintList)
        Node_bool = self.check_contain_chinese(Node)
        strategy_bool = self.check_contain_chinese(strategy)

        if PintList_bool==True:
            pass
        else:
            PintList=PintList.encode("utf-8")

        if Node_bool==True:
            pass
        else:
            Node=Node.encode("utf-8")

        if strategy_bool==True:
            pass
        else:
            strategy=strategy.encode("utf-8")

        DataSome={
            "PintList":PintList,
            "Node":Node,
            "strategy":strategy
        }

        print ("DataSome",type(Node),type(PintList),type(strategy))
        self.Fd.RsWriteYaml(self.FileName,DataSome)
        return JsonRes(json.dumps(DataSome))



class FillDelteNode(TemplateView):
    '''失败节点删除'''
    def __init__(self):
        self.Fd = FileDetach()
        self.FileName = Url.fileDatasome

    def post(self,request):
        NodeName=request.POST.get("NodeName")
        PintList=request.POST.get("PintList")

        if NodeName is not None and PintList is not None:
            print("selfFileName",self.FileName)
            self.Fd.RemoveYaml(self.FileName,PintList,NodeName)
            return JsonRes(json.dumps({"NodeName":NodeName}))
        else:
            return JsonRes(json.dumps("0401"))




class FileTimeGoView(TemplateView):
    '''失败节点补充提交页面'''
    template_name = "z_app/Nodepay.html"


class FileTakeShell(TemplateView):
    '''提交运行shell脚本'''

    def post(self, request):
        TimeSome = request.POST.get("TimeSome")

        rule=r'(\d{4}-\d{2}-\d{2})'
        ShowStr=re.findall(rule,TimeSome)
        if not ShowStr:
            return JsonRes(json.dumps("0401"))
        url=Url.testshell
        subprocess.Popen([
            "sh","%s"%url,"%s"%ShowStr[0]
        ])
        return JsonRes(json.dumps(TimeSome))








class FileListJsonView(JSONResponseMixin,TemplateView):
    
    def get(self, request, *args, **kwargs):
        
        result = ['1.yaml','2.yaml']
        return self.render_to_response({'flag':1,'message':result})
