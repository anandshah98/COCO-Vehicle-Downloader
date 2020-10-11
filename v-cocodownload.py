import json
import os
import os.path
from urllib.request import *


def getvehcats(file):
    """ Get vehicle indices from different coco object categories """
    vehicles = {}
    for i in file['categories']:
        if i['supercategory'] == 'vehicle' and i['name'] not in 'boatairplane':
            vehicles[i['id']] = i['name']
    return vehicles


def getimgids(file, vehicles):
    """ Get respective image IDs """
    c = {}
    for i in vehicles:
        c[i] = []
    for i in file['annotations']:
        cid = i['category_id']
        if cid in vehicles and i['image_id'] not in c[cid]:
            c[cid].append(i['image_id'])

    return c


def downloadimages(file, c, vehicles, opt):
    """ Download images"""
    p = file['images'][0]['coco_url']
    cut = p[:-16]
    st = "0" * 12
    cwd = os.getcwd()
    for i in c:
        path = vehicles[i]
        os.chdir(cwd)
        try:
            os.mkdir(path)
            print("Directory created " + path)            
        except OSError:
            print("Directory already present: " + path)
        os.chdir(path)
        print("In folder: " + path)
        for k in c[i]:
            temp = st[:(12 - len(str(k)))] + str(k) + ".jpg"
            if os.path.exists(temp):                
                print(temp + " present")
            else:
                urlretrieve(cut + temp, temp)
                print("downloaded " + temp)
            if opt == 0:
                print("\nTo change to batch download pass opt value as 1")
                break
        if opt == 0:
            break


def run():
    try:
        ann = input("Enter path of annotations directory: ")
        print()

        os.chdir(ann)
        filelist = [f for f in os.listdir(ann) if "keypoints" not in f and "captions" not in f and f.endswith(".json")]
        for i in range(len(filelist)):    
                print(str(i + 1) + ": " + filelist[i])

        inp = int(input("\nEnter annotation file number: "))
        print()
        temp = open(filelist[inp - 1])
        file = json.load(temp)
        vehicles = getvehcats(file)
        c = getimgids(file, vehicles)
        downloadimages(file, c, vehicles, opt = 1)  # opt = 1 -> batch download
                                                    # opt = 0 -> single download
    except Exception as er:
        print("Error: run again")
        print(er)

    except KeyboardInterrupt:
        """"""


if __name__ == "__main__":
    run()
