# coding=gbk
import os
import shutil

current_path = os.chdir('D:\\projects\\scu_data_mining\\data\\depth3_layer\\1980-1999\\���')

current_path = os.getcwd()
print('��ǰĿ¼��'+current_path)

filename_list = os.listdir(current_path)
print('��ǰĿ¼���ļ���', filename_list)

print('���ڷ���������ļ���ing...')
for filename in filename_list:
    try:
        name1, name2, name3 = filename.split('_')
        print(name1)
        if '����' in name2:
            try:
                os.mkdir(name2[:-1])
                print('�����ļ���'+name2[:-1])
            except:
                print('wrong1')
            try:
                shutil.move(current_path+'\\'+filename,current_path+'\\'+name2[:-1])
                print(filename+'ת�Ƴɹ���')
            except Exception as e:
                print('�ƶ�ʧ��:' + e)
        elif '����' in name2:
            try:
                os.mkdir(name2[:-1])
                print('�����ļ���'+name2[:-1])
            except:
                pass
            try:
                shutil.move(current_path+'\\'+filename,current_path+'\\'+name2[:-1])
                print(filename+'ת�Ƴɹ���')
            except Exception as e:
                print('�ƶ�ʧ��:' + e)
        elif 'Ӣ��' in name2:
            try:
                os.mkdir(name2[:-1])
                print('�����ļ���'+name2[:-1])
            except:
                pass
            try:
                shutil.move(current_path+'\\'+filename,current_path+'\\'+name2[:-1])
                print(filename+'ת�Ƴɹ���')
            except Exception as e:
                print('�ƶ�ʧ��:' + e)
        elif '�й�' in name2:
            try:
                os.mkdir(name2[:-1])
                print('�����ļ���'+name2[:-1])
            except:
                pass
            try:
                shutil.move(current_path+'\\'+filename,current_path+'\\'+name2[:-1])
                print(filename+'ת�Ƴɹ���')
            except Exception as e:
                print('�ƶ�ʧ��:' + e)
        elif '�պ�' in name2:
            try:
                os.mkdir(name2[:-1])
                print('�����ļ���'+name2[:-1])
            except:
                pass
            try:
                shutil.move(current_path+'\\'+filename,current_path+'\\'+name2[:-1])
                print(filename+'ת�Ƴɹ���')
            except Exception as e:
                print('�ƶ�ʧ��:' + e)
    except:
        print('wrong')
# print('���ڷ���������ļ���ing...')
# for filename in filename_list:
    # try:
        # name1, name2, name3 = filename.split('_')
        # print(name1)
        # if '����' in name1:
            # try:
                # os.mkdir(name1[:-1])
                # print('�����ļ���'+name1[:-1])
            # except:
                # print('wrong1')
            # try:
                # shutil.move(current_path+'\\'+filename,current_path+'\\'+name1[:-1])
                # print(filename+'ת�Ƴɹ���')
            # except Exception as e:
                # print('�ƶ�ʧ��:' + e)
        # elif '����' in name1:
            # try:
                # os.mkdir(name1[:-1])
                # print('�����ļ���'+name1[:-1])
            # except:
                # print('wrong1')
            # try:
                # shutil.move(current_path+'\\'+filename,current_path+'\\'+name1[:-1])
                # print(filename+'ת�Ƴɹ���')
            # except Exception as e:
                # print('�ƶ�ʧ��:' + e)
        # elif '����' in name1:
            # try:
                # os.mkdir(name1[:-1])
                # print('�����ļ���'+name1[:-1])
            # except:
                # print('wrong1')
            # try:
                # shutil.move(current_path+'\\'+filename,current_path+'\\'+name1[:-1])
                # print(filename+'ת�Ƴɹ���')
            # except Exception as e:
                # print('�ƶ�ʧ��:' + e)
        # elif '���' in name1:
            # try:
                # os.mkdir(name1[:-1])
                # print('�����ļ���'+name1[:-1])
            # except:
                # print('wrong1')
            # try:
                # shutil.move(current_path+'\\'+filename,current_path+'\\'+name1[:-1])
                # print(filename+'ת�Ƴɹ���')
            # except Exception as e:
                # print('�ƶ�ʧ��:' + e)

    # except:
        # print('wrong')

print('������ϣ�')
input()


