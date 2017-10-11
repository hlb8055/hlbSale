#!/usr/bin/env python
#coding:utf-8






#使用方法: 在cmd里执行命令 exec_config.py -add 或者 exec_config.py -remove 

import os
import sys; 
sys.dont_write_bytecode = True #防止之后import 其他自定义模块(xxteaModule)时在当前目录生成对应的pyc文件
sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/' + '..'))

import ScripUtils



#配置路径和XXTEA算法的key、sign
path_build_gradle     = "../../proj.android-studio/app/build.gradle"
path_AppActivity_java = "../../proj.android-studio/app/src/org/cocos2dx/lua/AppActivity.java"





#Android
#   case 1:申请appid, 制作好签名文件及其签名(md5)
#   case 2:在build.gradle文件中，添加如下依赖即可：
#   dependencies {
#       compile 'com.tencent.mm.opensdk:wechat-sdk-android-without-mta:+'
#   }

def config_build_gradle(bRemove):
    print(" config ===> build.gradle")

    content = 'compile \'com.tencent.mm.opensdk:wechat-sdk-android-without-mta:+\''
    all_the_text = ScripUtils.readFile(path_build_gradle)

    pos = all_the_text.find(content)
    if pos == -1 and not bRemove: 
        pos_e = all_the_text.find('//SDK_TAG_DEPENDENCIES')
        assert( pos_e > 0)
        all_the_text = ScripUtils.insertStr(all_the_text, content, pos_e)
        ScripUtils.writeFile(path_build_gradle, all_the_text)

    elif pos > 0 and bRemove:
        all_the_text = ScripUtils.removeStr(all_the_text, content, pos)
        ScripUtils.writeFile(path_build_gradle, all_the_text)


#   case3:修改 AppActivity.java 
def config_AppActivity_java(bRemove):
    #1)文件开头 import 相关类
    str_heads = [
        'import com.tencent.mm.opensdk.modelmsg.SendMessageToWX;', 
        'import com.tencent.mm.opensdk.modelmsg.WXImageObject;',
        'import com.tencent.mm.opensdk.modelmsg.WXMediaMessage;',
        'import com.tencent.mm.opensdk.modelmsg.WXWebpageObject;',
        'import com.tencent.mm.opensdk.openapi.IWXAPI;',
        'import com.tencent.mm.opensdk.openapi.WXAPIFactory;'
    ]

    #2) 在 AppActivity 类中定义成员变量, 注意appid根据您的情况来修改
    #   private static final String APP_ID = "wx708e74f728e0e612";
    #   private static IWXAPI api;
    str_var = [
        'private static final String APP_ID = "wx708e74f728e0e612";',
        'private static IWXAPI api;'
    ]

    #3) 在onCreate()函数中注册微信添加如下内容
    str_oncreate = [
        'api = WXAPIFactory.createWXAPI(this, APP_ID);',
        'api.registerApp(APP_ID);'
    ]

    content = [ 
        [str_heads,     '//SDK_TAG_IMPORT'],
        [str_var,       '//SDK_TAG_VAR'],
        [str_oncreate,  '//SDK_TAG_ONCREATE']
    ]


    all_the_text = ScripUtils.readFile(path_AppActivity_java)

    isChanged = False 
    for item in content:
        for v in item[0]:
            pos = all_the_text.find(v)
            if pos == -1 and not bRemove: 
                tmp = all_the_text.find(item[1])
                assert(tmp > 0)
                all_the_text = ScripUtils.insertStr(all_the_text, v, tmp)
                isChanged = True 

            elif pos > 0 and bRemove:
                all_the_text = ScripUtils.removeStr(all_the_text, v, pos)
                isChanged = True             

    if isChanged:
        ScripUtils.writeFile(path_AppActivity_java, all_the_text)







def do_configs(bRemove):
    config_build_gradle(bRemove)
    config_AppActivity_java(bRemove)




def run(argv):	
    if len(argv) != 2:
        print 'Usage: python', argv[0], '-[add | remove]'
        exit(1)
    if argv[1] not in ('-add', '-remove'):
        print 'Usage: python', argv[0], '-[add | remove]'
        exit(1)	

    if argv[1] == '-add':
        print("@@@ start to merge ...")
        do_configs(False)
        print("### finish merge success ...")	

    elif argv[1] == '-remove':
        print("~~~ start remove ...")
        do_configs(True)


run(sys.argv)