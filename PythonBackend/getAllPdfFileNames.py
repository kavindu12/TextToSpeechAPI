import os
import glob


def getListOfFileNames():
    path = './pdfs'
    list = []
    files = [f for f in glob.glob(path + "**/*.pdf", recursive=True)]

    for f in files:
        _, tail = os.path.split(f)
        replaceString =tail.replace(".pdf","");
        list.append(replaceString)
        # print(tail)
    return list

# print (len([name for name in os.listdir(path) if os.path.isfile(os.path.join(path, name))]))
# print(list)