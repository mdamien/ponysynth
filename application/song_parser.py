import re

def parse(song):
    result = []
    for match in re.findall(r"[a-gA-G ][#*]*\d*",song):
        match = match.replace(' ','r').lower()
        if len(match) == 1:
            result.append((match,1))
        elif len(match) == 3:
            result.append((match[:2],int(match[2])))
        elif re.match(r".\d",match):
            result.append((match[0],int(match[1])))
        else:
            result.append((match,1))
    return result

#print parse("A4BCD3F*3 3F3DEFC#3FF")

if __name__ == "__main__":
    song = parse("A4BCD3F*3 3F3DEFC#3FF")
    print song
    
    import pysynth
    pysynth.make_wav(song)
