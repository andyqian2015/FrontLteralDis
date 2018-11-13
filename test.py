# -*- coding:utf-8 -*-

import numpy as np
import shutil
import os

import pydicom
import pylab
import cv2

def ReadContourFromFile(dir):
    with open(dir, 'r') as f:
        line = f.read()
        str1 = line.split()
    for i in range(len(str1)):
        str1[i] = int(float(str1[i]))
    return np.array(str1)

def ReadFileNameFromFile(dir):
    with open(dir, 'r') as f:
        linestr = []
        line = f.readline()
        line = line.strip()
        linestr.append(line)
        while line:
            line = f.readline()
            line = line.strip()
            linestr.append(line)
    return np.array(linestr)

def GetFrontFromFile(dir1, dirIndex, driFileName, dirDst1,dirDst2):
    nIndex = ReadContourFromFile(dirIndex)
    nFileName = ReadFileNameFromFile(driFileName)
    nFrontFileName = nFileName[nIndex]
    nLaterFileName = []
    for file in nFileName:
        if file not in nFrontFileName:
            nLaterFileName.append(file)
    nLaterFileName = np.array(nLaterFileName)
    for fileName in nFrontFileName:
        fileDir = os.path.join(dir1, fileName)
        fileDst1 = os.path.join(dirDst1, fileName)
        fileDst2 = os.path.join(dirDst2, fileName)
        shutil.copy(fileDir, fileDst1)

    for fileName in nLaterFileName:
        fileDir = os.path.join(dir1, fileName)
        fileDst2 = os.path.join(dirDst2, fileName)
        print(fileDir)
        print(fileDst2)
        shutil.copy(fileDir, fileDst2)


def GetFrontFileNameFromFile(dir1, dirIndex, driFileName, dirDst):
    fileDir = os.path.join(dirDst, 'front.txt')
    nIndex = ReadContourFromFile(dirIndex)
    nFileName = ReadFileNameFromFile(driFileName)
    nFrontFileName = nFileName[nIndex]
    file = open(fileDir, "w")
    file.write(nFrontFileName)
    file.close()

def GetFileFromFolder(dirsrc, dirDst):
    for folder1 in os.listdir(dirsrc):
        FolderType = folder1
        folder1 = os.path.join(dirsrc, folder1)
        for folder2 in os.listdir(folder1):
            folder2 = os.path.join(folder1, folder2)
            for file in os.listdir(folder2):
                suffix = os.path.splitext(file)[1]
                if not suffix == ".dcm":
                    continue
                fileDir = os.path.join(folder2, file)
                dirDstCpy = os.path.join(dirDst, FolderType)
                if not os.path.isdir(dirDstCpy):
                    os.mkdir(dirDstCpy)
                fileDstDir = os.path.join(dirDstCpy, file)
                shutil.copy(fileDir, fileDstDir)

def TransformDicomToPng(srcdir, dirDst):
    for file in os.listdir(srcdir):
        fileDir = os.path.join(srcdir, file)
        ds = pydicom.read_file(fileDir)
        pixel_bytes = ds.pixel_array
        p_max= np.max(pixel_bytes)
        p_min = np.min(pixel_bytes)
        p_max = np.max(pixel_bytes[pixel_bytes < p_max])
        p_min = np.min(pixel_bytes[pixel_bytes > p_min])

        pixel_bytes = np.float32(pixel_bytes - p_min) /np.float(p_max - p_min) *255.0

        pixel_bytes = np.clip(pixel_bytes, 0, 255)
        pixel_bytes = pixel_bytes.astype(np.uint8)

        fileDst = os.path.splitext(file)[0] + ".png"
        filedirDst = os.path.join(dirDst, fileDst)
        cv2.imwrite(filedirDst, pixel_bytes)

def GetValidDicomData(dirsrc, dirDst, dirCpyTo):
    for file in os.listdir(dirsrc):
        fileName = os.path.splitext(file)[0]
        file = fileName + ".dcm"
        if file in os.listdir(dirDst):
            fileDirSrc = os.path.join(dirDst, file)
            fileDir = os.path.join(dirCpyTo, file)
            shutil.copy(fileDirSrc, fileDir)

def GetValidDicomData2(dirsrc, dirDst, dirCpyTo):
    for file in os.listdir(dirDst):
        fileName = os.path.splitext(file)[0]
        file1 = fileName + ".png"
        if file1 not in os.listdir(dirsrc):
            fileDirSrc = os.path.join(dirDst, file)
            fileDir = os.path.join(dirCpyTo, file)
            shutil.copy(fileDirSrc, fileDir)

if __name__ == "__main__":
    dirsrc = "/home/andy/frontlatel/frontPng"
    dirDst = "/home/andy/frontlatel/front"
    dirCpyTo = "/home/andy/frontlatel/ValidFront"
    GetValidDicomData(dirsrc, dirDst, dirCpyTo)

# if __name__ =="__main__":
#     srcDir = "/home/andy/frontlatel/lateral/"
#     dirDst = "/home/andy/frontlatel/lateralPng/"
#     TransformDicomToPng(srcDir, dirDst)

# if __name__ =="__main__":
#     dir1 = '/home/andy/307TBfile/TB/'
#     dirIndex = '/home/andy/frontlatel/Index.txt'
#     driFileName = '/home/andy/frontlatel/dcm.txt'
#     dirDst1 = '/home/andy/frontlatel/front/'
#     dirDst2 = '/home/andy/frontlatel/lateral/'
#     GetFrontFromFile(dir1, dirIndex, driFileName, dirDst1, dirDst2)
#     # GetFrontFileNameFromFile(dir1, dirIndex, driFileName, dirDst1)




# if __name__ == "__main__":
#     dirsrc = "/home/andy/307TB"
#     dirDst = "/home/andy/307TBfile"
#     GetFileFromFolder(dirsrc, dirDst)