import os, sys


def generatePumlFileName(fileName):
    return fileName.replace("/","-")+"_relation.puml"

def generatePngFileName(fileName):
    return fileName.replace("/","-")+"_relation.png"

def generatePng( filepath):
    os.system("java -jar plantuml/plantuml.jar " + filepath)