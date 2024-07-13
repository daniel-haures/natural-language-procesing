import conllu

def check_projectivity(heads):
    heads.insert(0,0)
    for index,_ in enumerate(heads):
        if not check_head_tail(index,heads[index],heads):
            return False
    return True

#n_head: head of arrow
#n_tail: children of arrow
#heads: mapping 
def check_head_tail(n_head,n_tail,heads):
    if(n_head==n_tail and n_head==0):
        return True
    for i in range (n_head+1,n_tail):
        if heads[i]<n_head or heads[i]>n_tail:
            return False
    return True


def openConllu(type):
    if(type=="train"):
        with open('data/it_isdt-ud-train.conllu', mode="r", encoding="utf-8") as data:
            # Read the file contents and assign under 'annotations'
            annotations = data.read()
            sentences = conllu.parse(annotations)
            return sentences
    elif(type=="test"):
        with open('data/it_isdt-ud-test.conllu', mode="r", encoding="utf-8") as data:
            # Read the file contents and assign under 'annotations'
            annotations = data.read()
            sentences = conllu.parse(annotations)
            return sentences
    else:
        with open('data/it_isdt-ud-dev.conllu', mode="r", encoding="utf-8") as data:
            # Read the file contents and assign under 'annotations'
            annotations = data.read()
            sentences = conllu.parse(annotations)
            return sentences
