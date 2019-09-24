import subprocess
import os, sys
import pandas
import datetime, time
import csv

line=[]
pathLine=[]
dirName=[]
def search(dirname):
    try:
        filenames = os.listdir(dirname)
        for filename in filenames:
            full_filename = os.path.join(dirname, filename)
            if os.path.isdir(full_filename):
                search(full_filename)
            else:
                ext = os.path.splitext(full_filename)[-1]
                if ext == '.apk':
                    line.append(filename)
                    dirName.append(dirname)
                    if dirname[-1] == '/':
                        pathLine.append(full_filename)
                    else:
                        pathLine.append(dirname + '/' + filename)
    except PermissionError:
        pass

InputApkPath = 'Z:/0.Dataset/AndroZoo/2017/goodware'
search(InputApkPath)
a=0

tool_sel=['nothing','classyshark','apktool']
sel_option=int(input())

a=0
try:
    st_time=time.time()
    while True:
        apk_fn = line[a]
        apk_path = pathLine[a]
        apk_name = apk_fn[:-4]
#         if 'empty' in apk_path:
#             w_ware = '@@empty'
#         elif 'goodware' in apk_path:
#             w_ware = '@@goodware'
#         elif 'greyware' in apk_path:
#             w_ware = '@@greyware'
#         elif 'malware' in apk_path:
#             w_ware = '@@malware'

        if sel_option == 1:
            cmd_mkdir = 'D:/az_decom && md '+apk_name+' && cd D:/az_decom/'+apk_name+' && java -jar D:/decom_tool/ClassyShark.jar -export '+apk_path+' && mv AndroidManifest.xml_dump AndroidManifest.txt' # && mkdir '+w_ware'
            new = subprocess.run(cmd_mkdir,shell=True,encoding='utf-8')
        elif sel_option == 2:
            cmd_mkdir = 'E: && cd az_decom && java -jar apktool.jar d '+apk_path
#             cmd_mkdir2 = 'cd D:/az_decom/'+apk_name+' && mv AndroidManifest.xml AndroidManifest.txt' # && mkdir ' + w_ware
            new = subprocess.run(cmd_mkdir,shell=True,encoding='utf-8')
#             new2 = subprocess.call(cmd_mkdir2,shell=True,encoding='utf-8')
        if len(pathLine) == a + 1:
            break
        else:
            a += 1
    print("Decoding is Done! : ", (time.time()-st_time)/60)
except KeyboardInterrupt:
    pass


apkListNum = len(apkList)
apkList=[]
apkWare=[]
apkPath=[]
if sel_option == 1:
    os_path = '/media/csos/dataset/apis/'
    path_size = 25
elif sel_option == 2:
    os_path = '/media/csos/dataset/apktool_apis/'
    path_size = 33
for (path, dir, files) in os.walk(os_path):
    for filename in files:
        ext = filename
        if ext == 'AndroidManifest.txt':
            apkList.append(path[path_size:])
        ext2 = filename
        if ext2 == 'empty':
            print(dir)


def permission_extract():
    with open('/media/csos/dataset/apps/permission_list.txt', 'r', encoding='utf-8') as pl:
        p_list = ['apk_name'] + pl.readlines()
        p_len = len(p_list)

    with open('/media/csos/dataset/apps/permission.csv', 'w+', encoding='utf-8', newline='') as perm:
        writer = csv.DictWriter(perm, fieldnames=p_list)
        writer.writeheader()
    writer = csv.writer(perm)

    a = 0
    while apkListNum != a:
        getName = apkList[a]
        getRow = [0] * p_len
        getRow[0] = apkList[a]
    #         getRow[2] = apkList[a]
        with open(os_path + getName + '/' + 'AndroidManifest.txt') as xml_Read:
            permR = xml_Read.readlines()
        for b in permR:
            count = 0
            for c in p_list[1:]:
                if count > len(getRow):
                    break
                if b.find(c[:-1]) != -1:
                    getRow[count + 1] = 1
                count += 1
        with open('/media/csos/dataset/apps/permission.csv', 'a+', newline='') as perm:
            writer = csv.writer(perm)
            writer.writerow(getRow)
        a += 1

def oswalk_smali(getName):
    smaliList=[]
    os_path = '/media/csos/dataset/apktool_apis/'+getName+'/smali/'
    path_size = 33
    for (path, dir, files) in os.walk(os_path):
        for filename in files:
            ext = filename
            smaliList.append(path+'/'+ext)
    return smaliList
#     print(smaliList)



def api_extract():
    a = 0
    while apkListNum != a:
        reg=[]
        getName = apkList[a]
        getRow=[]
        smaliList = oswalk_smali(getName)
        try:
            for sl in smaliList:
                with open(sl,'r') as apiRead:
                    apiR = apiRead.readlines()
                for b in apiR:
#                     if b.find('.method ') != -1:
#                         getRow.append(b.split('method ')[1])
                    if b.find('invoke-') != -1:
                        getRow.append(b.split('}, ')[1])
#                     if b.find('invoke-direct') != -1:
#                         getRow.append(b.split('}, ')[1])
#                         newfolder = '/media/csos/dataset/apps/apktool_api_extract/'+getName+'.txt'
#                         with open(newfolder,'a+',encoding='utf-8') as api_Read:
#                             api_Read.writelines(b.split('}, ')[1])
        except IndexError:
            pass
        newfolder = '/media/csos/dataset/apps/apktool_api_extract/'+getName+'.txt'
        with open(newfolder,'w',encoding='utf-8') as api_Read:
            api_Read.writelines(getRow)
        a += 1



def apicounting():
    txtList = []
    os_path = '/media/csos/dataset/apps/apktool_api_extract/'
    for (path, dir, files) in os.walk(os_path):
        for filename in files:
            ext = filename
            txtList.append(ext)
    txtListLen = len(txtList)
    tc = 0
    while txtListLen != tc:
        cmd_mkdir = 'cat /media/csos/dataset/apps/apktool_api_extract/'+txtList[tc]+' | sort | uniq -c | sort -r -n > /media/csos/dataset/apps/api_extract_methodcounting/'+txtList[tc]
#         cmd_mkdir2 = 'cat /media/csos/dataset/apps/apktool_api_extract/'+txtList[tc]+' | sort -n -r > /media/csos/dataset/apps/api_extract_methodcounting/'+txtList[tc]
        new = subprocess.run(cmd_mkdir,shell=True,encoding='utf-8')
#         new = subprocess.call(cmd_mkdir2,shell=True,encoding='utf-8')
        tc += 1



operand2=['nothing','permission','apis','apicounting']
op_num=int(input())

if operand2[op_num] == 'permission':
    try:
        perm_time = time.time()
        permission_extract()
        print('Permission is Done! : ',time.time()-perm_time)
    except IndexError:
        print('Permission is Done! : ',time.time()-perm_time)
    except KeyboardInterrupt:
        print('Permission is Done! : ',time.time()-perm_time)
elif operand2[op_num] == 'apis':
    try:
        api_time = time.time()
        api_extract()
        print('Api is Done! : ',time.time()-api_time)
    except IndexError:
         print('Api is Done! : ',time.time()-api_time)
    except KeyboardInterrupt:
         print('Api is Done! : ',time.time()-api_time)
elif operand2[op_num] == 'apicounting':
    try:
        mc_time = time.time()
        apicounting()
        print('Apicounting is Done! : ', time.time()-mc_time)
    except IndexError:
        print('Apicounting is Done! : ', time.time()-mc_time)
    except KeyboardInterrupt:
        print('Apicounting is Done! : ', time.time()-mc_time)




