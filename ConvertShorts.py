import re

exampleList = [
    "https://www.youtube.com/shorts/3LHKO-2eC-M",
    "https://www.youtube.com/watch?v=YRK-NahQsfw",
    "https://www.youtube.com/shorts/YRK-NahQsfw",
    "https://www.youtube.com/shorts/wLonxHi0yRk",
    "https://www.youtube.com/shorts/i3vngxQSVpk",
    "https://www.youtube.com/shorts/O2lBBUb9pAw",
    "https://www.youtube.com/watch?v=O2lBBUb9pAw"
]

def convert_shorts(link):
    newLink = ""
    containsShort = re.search(r'shorts', link)

    if(containsShort):
        newLink = link.replace('/shorts/', '/watch?v=')
    else:
        newLink = link
    return newLink

for e in exampleList:
    e = convert_shorts(e)
    print(e)
