import os
import math
import shutil

# 한 폴더 안에 들어갈 파일 개수 지정
fileUnit = input("목표 확장자 : ")

basePath = "C:\\Users\\BIT-R42\\opencvEx\\labelImg"

# 파일 경로 관련 문자열을 붙여주는 역할을 하는 메소드
# catPath = os.path.join(basePath, "Cat")
# dogPath = os.path.join(basePath, "Dog")
dataPath = os.path.join(basePath, "data")

# # 내가 확인하고자 하는 경로의 파일 목록을 보여준다.
# # ls와 유사
# filenames = os.listdir(basePath)
#
# # 폴더의 파일목록을 읽어옴
# catFiles = os.listdir(catPath)
#
# # 파일 목록의 개수 확인
# catLeng = len(catFiles)
#
# # 개수 출력
# # print(catLeng)
#
# # 폴더를 생성하는 개수를 구함
# # folderNum = math.ceil(catLeng/2000)
# folderNum = math.ceil(catLeng / fileUnit)
# print(folderNum)
#
# catFiles = os.listdir(catPath)
# folderArray = [os.path.join(catPath, "cat_{}".format(i)) for i in range(0, folderNum)]
# print(folderArray)
#
# for i in range(0, folderNum):
#     if not os.path.isdir(os.path.join(catPath, "cat_{}".format(i))):
#         # print(catPath)
#         mkname = os.path.join(catPath, "cat_{}".format(i))
#
#         # print(mkname)
#         os.mkdir(mkname)
#
#     else:
#         pass
#
# count = 0
# for catFile in catFiles:
#
#     # catFile은 파일명만 보여주므로 전체 경로를 지정해줘야 함
#     myList = os.path.join(catPath, catFile)
#     if os.path.isdir(myList):
#         count += 1
#
# if count == folderNum:
#     print("정상적으로 폴더가 생성되었습니다.")
#
# # cat_0 : 0 ~ 1999
# # cat_1 : 2000 ~ 3999
# # ...
#
# for catFile in catFiles:
#
#     j = 0
#
#     # 파일명과 확장자 분리
#     name, ext = os.path.splitext(catFile)
#
#     # 폴더 제외
#     if ext == '.jpg':
#         num = int(name)
#
#         while j < folderNum:
#
#             if fileUnit * j <= num < fileUnit * (j + 1):
#
#                 myFile = os.path.join(catPath, catFile)
#
#                 # src 경로, target 경로
#                 # print(myFile)
#                 # print(folderArray[j] + "/" + catFile)
#                 shutil.move(myFile, folderArray[j] + "/" + catFile)
#                 j = folderNum
#
#             else:
#                 j += 1
#
#     else:
#         pass
#
# i = 0
#
# while i < catLeng - 1:
#     fileList = os.listdir(os.path.join(catPath, "cat_{}".format(i)))
#     print(len(fileList))
#     i += 1

# 폴더의 파일목록을 읽어옴
# dogFiles = os.listdir(dogPath)
dataFiles = os.listdir(dataPath)

# 파일 목록의 개수 확인
# dogLeng = len(dogFiles)
dataLeng = len(dataFiles)

# 개수 출력
# print(dogLeng)

# 폴더를 생성하는 개수를 구함
# folderNum = math.ceil(dogLeng/2000)
folderNum = math.ceil(dataLeng / fileUnit)
print(folderNum)

# dogFiles = os.listdir(dogPath)
# folderArray = [os.path.join(dogPath, "chair ()".format(i)) for i in range(0, folderNum)]
dataFiles = os.listdir(dataPath)
folderArray = [os.path.join(dataPath, "saved_frame{}".format(i)) for i in range(0, folderNum)]
print(folderArray)

for i in range(0, folderNum):
    # if not os.path.isdir(os.path.join(dogPath, "dog_{}".format(i))):
    if not os.path.isdir(os.path.join(dataPath, "saved_frame{}".format(i))):

        # print(dogPath)
        # mkname = os.path.join(dogPath, "dog_{}".format(i))
        mkname = os.path.join(dataPath, "saved_frame{}".format(i))

        # print(mkname)
        os.mkdir(mkname)

    else:
        pass

count = 0
# for dogFile in dogFiles:
for dataFile in dataFiles:

    # catFile은 파일명만 보여주므로 전체 경로를 지정해줘야 함
    # myList = os.path.join(dogPath, dogFile)
    myList = os.path.join(dataPath, dataFile)
    if os.path.isdir(myList):
        count += 1

if count == folderNum:
    print("정상적으로 폴더가 생성되었습니다.")

# cat_0 : 0 ~ 1999
# cat_1 : 2000 ~ 3999
# ...

# for dogFile in dogFiles:
for dataFile in dataFiles:

    # for 문 내에서 초기값 지정
    j = 0

    # 파일명과 확장자 분리
    # name, ext = os.path.splitext(dogFile)
    name, ext = os.path.splitext(dataFile)

    # 폴더 제외
    if ext == '.jpg':
        num = int(name)

        while j < folderNum:

            if fileUnit * j <= num < fileUnit * (j + 1):

                # myFile = os.path.join(dogPath, dogFile)
                myFile = os.path.join(dataPath, dataFile)

                # src 경로, target 경로
                # print(myFile)
                # print(folderArray[j] + "/" + dogFile)
                # shutil.move(myFile, folderArray[j] + "/" + dogFile)
                shutil.move(myFile, folderArray[j] + "/" + dataFile)
                j = folderNum

            else:
                j += 1

    else:
        pass

i = 0
# while i < dogLeng - 1:
while i < dataLeng - 1:
    # fileList = os.listdir(os.path.join(dogPath, "dog_{}".format(i)))
    fileList = os.listdir(os.path.join(dataPath, "data_{}".format(i)))
    print(len(fileList))
    i += 1
