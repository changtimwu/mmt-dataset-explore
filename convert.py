import csv
import sys
import json

'''
{
  "categories": [
    {
      "id": 1,
      "name": "person",
      "supercategory": ""
    }
  ],
  "annotations": [
    {
      "category_id": 1,
      "is_occluded": false,
      "attributes": {},
      "iscrowd": 0,
      "bbox": [
        1000,
        196,
        194,
        493
      ],
      "id": 0,
      "image_id": 0,
      "segmentation": null,
      "area": 95642
    },
  ], 
  "images": [
    {
      "dataset": "IOTG_RSD_Team_datasets",
      "license": null,
      "date_captured": null,
      "image": "val/image_000000.jpg",
      "coco_url": null,
      "file_name": "image_000000.jpg",
      "id": 0,
      "flickr_url": null,
      "width": 1920,
      "height": 1080
    },
  ]
 
'''


gannot = { 
        "categories":[ { "id":1, "name":"person", "supercategory":[] }], 
        "annotations":[], 
        "images":[] 
}

def get_imgid():
    get_imgid.cnt+=1
    return get_imgid.cnt
get_imgid.cnt=0

def get_annoid():
    get_annoid.cnt+=1
    return get_annoid.cnt
get_annoid.cnt=0

#'img_size': '[720, 1280, 3]', 'nbboxes': '1', 'bbox_coords': '[[694, 275, 876, 696]]', 
prefix=''
def insert_image( origanno):
    img_tmpl={ "dataset": "Momentum", "license":None, "data_captured": None} 
    img=img_tmpl.copy()
    imgsize=origanno['img_size']
    img['width']=imgsize[1]
    img['height']=imgsize[0]
    img['id']=get_imgid()
    img['file_name']= prefix + origanno['image'] # 'mmt0329ch004_12254.jpg', 'img_path': 'PersonDetection/For_OpenVINO_PD_Test/MMTPerson200329_Ch004/mmt0329ch004_12254.jpg'
    gannot['images'].append(img)
    return img['id']


def insert_annotation( origanno):
    anno_tmpl = { "category_id":1, "is_occluded": False, "attributes": {}, "iscrowd":0, "segmentation":None, "area":1}
    for coord in origanno['bbox_coords']:
        anno =anno_tmpl.copy()
        anno["bbox"] =  coord 
        imgid = insert_image( origanno)
        anno['image_id'] = imgid
        anno['id'] = get_annoid()
        gannot['annotations'].append( anno)
    

def arrange_row(row):
    row['img_size'] = json.loads( row['img_size'])
    row['nbboxes'] = int(row['nbboxes'])
    row['bbox_coords'] = json.loads( row['bbox_coords'])   ## '[[694, 275, 876, 696]]', 
    return row


with open(sys.argv[1], newline='') as csvfile:
    listreader = csv.DictReader(csvfile) #, delimiter=' ', quotechar='|')
    reclist = [ arrange_row(row) for row in listreader]
    #print('{} of records'.format(len(reclist)))
    #print(reclist[0])

for rec in reclist:
    insert_annotation( rec)

print( json.dumps( gannot,  indent=4))
