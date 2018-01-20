import cv2, random
from llk import *
from easy_getscreen import *
from grid_spliter import *
from keras.models import load_model
from CreateCate import CreateCate

##s = get_window_abs_by_name('QQ游戏 - 连连看角色版',True)
##v = cv2.imwrite('123.png',s)[181:566,14:603]
v = cv2.imread('456.png')[181:566,14:603]
gridh,gridw = 11,19

def cat_val2num(cates2class):
    ids = list(range(1,len(cates2class)))
    for idx,value in cates2class.items():
        if value!='0':
            cates2class[idx] = ids.pop()
        else:
            cates2class[idx] = 0

print('loading models...')
grider = GridSpliter(v,gridh,gridw)
modeler = load_model('mytrain_model.h5')
cater = CreateCate()
cates2class = cater.load_mapdict('mycate_model.pickle')
cat_val2num(cates2class)
print('loading models ok.')

s_map = np.zeros((gridh,gridw))
for i in range(gridh):
    for j in range(gridw):
        pic = grider.get_picmat_by_point(i,j)[None,]
        pr = modeler.predict(pic.astype(np.float32)/255.)
        cls = cater.get_class_by_cate(cates2class,pr)
        s_map[i,j] = cls

s_map = s_map.astype(np.int32)
print(s_map)
cv2.imshow('456',v)
cv2.waitKey()
cv2.destroyAllWindows()

i = 0
final_chain = []
while np.any(s_map!=0):
    print('time:',i)
    zpoints = list(zip(*map(lambda i:i.tolist(),np.where(s_map==0))))
    point = random.choice(zpoints)
    result = get_1point_results(s_map,point)
    print(result)
    for idx1,idx2 in result:
        final_chain.append((idx1,idx2))
        s_map[idx1],s_map[idx2] = 0,0
    i += 1


