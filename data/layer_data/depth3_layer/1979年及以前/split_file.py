# coding=gbk
import os
import shutil

current_path = os.chdir('D:\\projects\\scu_data_mining\\data\\depth3_layer\\1980-1999\\惊悚')

current_path = os.getcwd()
print('当前目录：'+current_path)

filename_list = os.listdir(current_path)
print('当前目录下文件：', filename_list)

print('正在分类整理进文件夹ing...')
for filename in filename_list:
    try:
        name1, name2, name3 = filename.split('_')
        print(name1)
        if '法国' in name2:
            try:
                os.mkdir(name2[:-1])
                print('创建文件夹'+name2[:-1])
            except:
                print('wrong1')
            try:
                shutil.move(current_path+'\\'+filename,current_path+'\\'+name2[:-1])
                print(filename+'转移成功！')
            except Exception as e:
                print('移动失败:' + e)
        elif '美国' in name2:
            try:
                os.mkdir(name2[:-1])
                print('创建文件夹'+name2[:-1])
            except:
                pass
            try:
                shutil.move(current_path+'\\'+filename,current_path+'\\'+name2[:-1])
                print(filename+'转移成功！')
            except Exception as e:
                print('移动失败:' + e)
        elif '英国' in name2:
            try:
                os.mkdir(name2[:-1])
                print('创建文件夹'+name2[:-1])
            except:
                pass
            try:
                shutil.move(current_path+'\\'+filename,current_path+'\\'+name2[:-1])
                print(filename+'转移成功！')
            except Exception as e:
                print('移动失败:' + e)
        elif '中国' in name2:
            try:
                os.mkdir(name2[:-1])
                print('创建文件夹'+name2[:-1])
            except:
                pass
            try:
                shutil.move(current_path+'\\'+filename,current_path+'\\'+name2[:-1])
                print(filename+'转移成功！')
            except Exception as e:
                print('移动失败:' + e)
        elif '日韩' in name2:
            try:
                os.mkdir(name2[:-1])
                print('创建文件夹'+name2[:-1])
            except:
                pass
            try:
                shutil.move(current_path+'\\'+filename,current_path+'\\'+name2[:-1])
                print(filename+'转移成功！')
            except Exception as e:
                print('移动失败:' + e)
    except:
        print('wrong')
# print('正在分类整理进文件夹ing...')
# for filename in filename_list:
    # try:
        # name1, name2, name3 = filename.split('_')
        # print(name1)
        # if '动作' in name1:
            # try:
                # os.mkdir(name1[:-1])
                # print('创建文件夹'+name1[:-1])
            # except:
                # print('wrong1')
            # try:
                # shutil.move(current_path+'\\'+filename,current_path+'\\'+name1[:-1])
                # print(filename+'转移成功！')
            # except Exception as e:
                # print('移动失败:' + e)
        # elif '剧情' in name1:
            # try:
                # os.mkdir(name1[:-1])
                # print('创建文件夹'+name1[:-1])
            # except:
                # print('wrong1')
            # try:
                # shutil.move(current_path+'\\'+filename,current_path+'\\'+name1[:-1])
                # print(filename+'转移成功！')
            # except Exception as e:
                # print('移动失败:' + e)
        # elif '悬疑' in name1:
            # try:
                # os.mkdir(name1[:-1])
                # print('创建文件夹'+name1[:-1])
            # except:
                # print('wrong1')
            # try:
                # shutil.move(current_path+'\\'+filename,current_path+'\\'+name1[:-1])
                # print(filename+'转移成功！')
            # except Exception as e:
                # print('移动失败:' + e)
        # elif '惊悚' in name1:
            # try:
                # os.mkdir(name1[:-1])
                # print('创建文件夹'+name1[:-1])
            # except:
                # print('wrong1')
            # try:
                # shutil.move(current_path+'\\'+filename,current_path+'\\'+name1[:-1])
                # print(filename+'转移成功！')
            # except Exception as e:
                # print('移动失败:' + e)

    # except:
        # print('wrong')

print('整理完毕！')
input()


