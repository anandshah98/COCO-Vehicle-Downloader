import json
import os
import os.path

def store_bounds():
    z = open(input("Enter path with annotation file name"))
    x = json.load(z)
    y = x['categories']
    l = {}
    for i in y:
        if i['supercategory'] == 'vehicle' and i['name'] not in 'boatairplane':
            l[i['id']] = i['name']
            #print(i)
    c = {}
    for i in x['annotations']:
        if i['category_id'] in l:
            if i['image_id'] not in c:
                c[i['image_id']]=["{} {}\n".format(i['category_id'], ' '.join(map(str, i['bbox'])))]
            else:
                c[i['image_id']].append("{} {}\n".format(i['category_id'], ' '.join(map(str, i['bbox']))))

    os.chdir(input("Enter path to store files"))
    if not os.path.exists("bboxes"):
        os.mkdir("bboxes")
    os.chdir("bboxes")
    for i in l:
        if not os.path.exists(l[i]):            
            os.mkdir(l[i])
    for i in c:
        for item in c[i]:
            p = int(item.split()[0])
            ofile = open("{}/{}.txt".format(l[p], i), 'a+')
            ofile.write(item)
            ofile.close()

if __name__ == "__main__":
    store_bounds()
