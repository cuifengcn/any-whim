import tensorflow as tf
from numpy import *

inpt = tf.placeholder(tf.float32,[1,None,None,3])
im_info = tf.placeholder(tf.float32,shape = [1,3])
gt_boxes = tf.placeholder(tf.float32,shape = [None,5])
gt_ishard = tf.placeholder(tf.int32,shape = [None])
dontcare_areas = tf.placeholder(tf.float32,shape = [None,4])
keep_prob = tf.placeholder(tf.float32)

conv_stride,pool = [1,1,1,1],[1,2,2,1]
conv1_1 = tf.Variable(tf.truncated_normal([3,3,3,64],stddev=0.01),trainable = False)
conv1_2 = tf.Variable(tf.truncated_normal([3,3,64,64],stddev=0.01),trainable = False)
conv2_1 = tf.Variable(tf.truncated_normal([3,3,64,128],stddev=0.01),trainable = False)
conv2_2 = tf.Variable(tf.truncated_normal([3,3,128,128],stddev=0.01),trainable = False)
conv3_1 = tf.Variable(tf.truncated_normal([3,3,128,256],stddev=0.01))
conv3_2 = tf.Variable(tf.truncated_normal([3,3,256,256],stddev=0.01))
conv4_1 = tf.Variable(tf.truncated_normal([3,3,256,512],stddev=0.01))
conv4_2 = tf.Variable(tf.truncated_normal([3,3,512,512],stddev=0.01))
conv4_3 = tf.Variable(tf.truncated_normal([3,3,512,512],stddev=0.01))
conv5_1 = tf.Variable(tf.truncated_normal([3,3,512,512],stddev=0.01))
conv5_2 = tf.Variable(tf.truncated_normal([3,3,512,512],stddev=0.01))
conv5_3 = tf.Variable(tf.truncated_normal([3,3,512,512],stddev=0.01))

hide = tf.nn.relu(tf.nn.conv2d(inpt,conv1_1,conv_stride,"SAME"))
hide = tf.nn.relu(tf.nn.conv2d(hide,conv1_2,conv_stride,"SAME"))
hide = tf.nn.max_pool(hide,pool,pool,"VALID")
hide = tf.nn.relu(tf.nn.conv2d(hide,conv2_1,conv_stride,"SAME"))
hide = tf.nn.relu(tf.nn.conv2d(hide,conv2_2,conv_stride,"SAME"))
hide = tf.nn.max_pool(hide,pool,pool,"VALID")
hide = tf.nn.relu(tf.nn.conv2d(hide,conv3_1,conv_stride,"SAME"))
hide = tf.nn.relu(tf.nn.conv2d(hide,conv3_2,conv_stride,"SAME"))
hide = tf.nn.max_pool(hide,pool,pool,"VALID")
hide = tf.nn.relu(tf.nn.conv2d(hide,conv4_1,conv_stride,"SAME"))
hide = tf.nn.relu(tf.nn.conv2d(hide,conv4_2,conv_stride,"SAME"))
hide = tf.nn.relu(tf.nn.conv2d(hide,conv4_3,conv_stride,"SAME"))
hide = tf.nn.max_pool(hide,pool,pool,"VALID")
hide = tf.nn.relu(tf.nn.conv2d(hide,conv5_1,conv_stride,"SAME"))
hide = tf.nn.relu(tf.nn.conv2d(hide,conv5_2,conv_stride,"SAME"))
hide = tf.nn.relu(tf.nn.conv2d(hide,conv5_3,conv_stride,"SAME"))

#rpn3x3
rpn_3x3_v = tf.Variable(tf.truncated_normal([3,3,512,512]))
rpn_3x3 = tf.nn.conv2d(hide,rpn_3x3_v,conv_stride,"SAME")

#1:<-rpn_cls_score,2:<-rpn_bbox_pred
rpn_cls_score_v = tf.Variable(tf.truncated_normal([1,1,512,9*2],stddev=0.01))
rpn_cls_score   = tf.nn.conv2d(rpn_3x3,rpn_cls_score_v,conv_stride,"SAME")
rpn_bbox_pred_v = tf.Variable(tf.truncated_normal([1,1,512,9*4],stddev=0.01))
rpn_bbox_pred   = tf.nn.conv2d(rpn_3x3,rpn_bbox_pred_v,conv_stride,"SAME")

#1:->rpn_cls_score->rpn_cls_score_reshape.softmax->rpn_cls_prob->rpn_cls_prob_reshape
rpn_cls_score_reshape = tf.reshape(rpn_cls_score,[tf.shape(rpn_cls_score)[1],\
                                                  tf.shape(rpn_cls_score)[2],9,2])
rpn_cls_prob          = tf.nn.softmax(tf.reshape(rpn_cls_score_reshape,[-1,2]))
rpn_cls_prob_reshape  = tf.reshape(rpn_cls_prob,tf.shape(rpn_cls_score))


def proposal_layer(rpn_cls_prob_reshape,rpn_bbox_pred,im_info):
    generate_anchors = array([[ -83.,  -39.,  100.,   56.],
                              [-175.,  -87.,  192.,  104.],
                              [-359., -183.,  376.,  200.],
                              [ -55.,  -55.,   72.,   72.],
                              [-119., -119.,  136.,  136.],
                              [-247., -247.,  264.,  264.],
                              [ -35.,  -79.,   52.,   96.],
                              [ -79., -167.,   96.,  184.],
                              [-167., -343.,  184.,  360.]])
    im_info       = im_info[0]
    _anchors      = generate_anchors[None,:]
    _anchors_num  = generate_anchors.shape[0]
    _feat_stride  = [16,]
    anchor_scales = [8, 16, 32]
    assert rpn_cls_prob_reshape.shape[0] == 1, 'Only single item batches are supported'

    height,width = rpn_cls_prob_reshape.shape[1:3]
    scores = reshape(rpn_cls_prob_reshape,[1,height,width,9,2])[:,:,:,:,1]
    #scores = reshape(rpn_cls_prob_reshape,[1,height,width,9])
    bbox_deltas = rpn_bbox_pred
    shift_x = arange(width) * _feat_stride
    shift_y = arange(height) * _feat_stride
    shift_x,shift_y = meshgrid(shift_x,shift_y)
    shift_x,shift_y = shift_x.ravel(),shift_y.ravel()
    shifts = vstack((shift_x,shift_y,shift_x,shift_y))
    shifts = shifts[None,:].transpose([2,0,1])
    anchors = _anchors + shifts
    anchors = anchors.reshape((width*height*_anchors_num,4))

    bbox_deltas = bbox_deltas.reshape((-1,4))
    scores = scores.reshape((-1,1))

    # anchors + bbox_deltas -> pred_boxes
    anchors = anchors.astype(bbox_deltas.dtype, copy=False)
    widths = anchors[:,2] - anchors[:,0] + 1.
    heights = anchors[:,3] - anchors[:,1] + 1.
    ctr_x = anchors[:,0] + .5*widths
    ctr_y = anchors[:,1] + .5*heights
    dx = bbox_deltas[:,0::4]
    dy = bbox_deltas[:,1::4]
    dw = bbox_deltas[:,2::4]
    dh = bbox_deltas[:,3::4]
    pred_ctr_x = dx * widths[:,None] + ctr_x[:,None]
    pred_ctr_y = dy * heights[:,None] + ctr_y[:,None]
    pred_w = exp(dw) * widths[:,None]
    pred_h = exp(dh) * heights[:,None]
    pred_boxes = zeros(bbox_deltas.shape, dtype=bbox_deltas.dtype)
    pred_boxes[:,0::4] = pred_ctr_x - .5 * pred_w
    pred_boxes[:,1::4] = pred_ctr_y - .5 * pred_h
    pred_boxes[:,2::4] = pred_ctr_x + .5 * pred_w
    pred_boxes[:,3::4] = pred_ctr_y + .5 * pred_h
    pred_boxes[:,0::4] = maximum(minimum(pred_boxes[:,0::4], im_info[1]-1), 0)
    pred_boxes[:,1::4] = maximum(minimum(pred_boxes[:,1::4], im_info[0]-1), 0)
    pred_boxes[:,2::4] = maximum(minimum(pred_boxes[:,2::4], im_info[1]-1), 0)
    pred_boxes[:,3::4] = maximum(minimum(pred_boxes[:,3::4], im_info[0]-1), 0)

    # filter by pic min_size, im_info[2]=min_size
    min_size = 16
    proposals = pred_boxes
    ws = proposals[:,2] - proposals[:,0] + 1
    hs = proposals[:,3] - proposals[:,1] + 1
    keep = where((ws > min_size) & (hs > min_size))[0]
    proposals = proposals[keep,:]
    scores = scores[keep]

    nms_top_pre = 6000
    order = scores.ravel().argsort()[::-1]
    order = order[:nms_top_pre]
    proposals = proposals[order,:]
    scores = scores[order]
    
    # nms -> cells
    nms_thresh = .7
    nms_top_post = 300
    #keeper = hstack((proposals,scores))
    keeper = proposals
    cells = []
    while len(keeper):
        remov = [0]
        cell = keeper[0]
        cells.append(cell)
        for i,j in enumerate(keeper[0:],1):
            x01,y01,x02,y02 = cell[:4]
            x11,y11,x12,y12 = j[:4]

            xx1 = max(x01,x11)
            yy1 = max(y01,y11)
            xx2 = min(x02,x12)
            yy2 = min(y02,y12)

            w = xx2 - xx1
            h = yy2 - yy1
            iou = w*h
            if w>0 and h>0:
                sa = (y02 - y01) * (x02 - x01)
                sb = (y12 - y11) * (x12 - x11)
                g = iou / (sa + sb - iou)
                if g>nms_thresh:
                    remov.append(i)
        keeper = delete(keeper,remov,0)
    cells = array(cells[:nms_top_post])

    return cells

#1+2:->rpn_rois
#rpn_rois = proposal_layer(rpn_cls_prob_reshape,rpn_bbox_pred,im_info)



# -------------------------------------------------------------------------------------------
def anchors_target_layer(rpn_cls_score,gt_boxes,im_info):
    generate_anchors = array([[ -83.,  -39.,  100.,   56.],
                              [-175.,  -87.,  192.,  104.],
                              [-359., -183.,  376.,  200.],
                              [ -55.,  -55.,   72.,   72.],
                              [-119., -119.,  136.,  136.],
                              [-247., -247.,  264.,  264.],
                              [ -35.,  -79.,   52.,   96.],
                              [ -79., -167.,   96.,  184.],
                              [-167., -343.,  184.,  360.]])
    im_info       = im_info[0]
    _anchors      = generate_anchors[None,:]
    _anchors_num  = generate_anchors.shape[0]

    assert rpn_cls_score.shape[0] == 1, 'Only single item batches are supported'

    height,width = rpn_cls_score.shape[1:3]
    shift_x = arange(width) * _feat_stride
    shift_y = arange(height) * _feat_stride
    shift_x,shift_y = meshgrid(shift_x,shift_y)
    shift_x,shift_y = shift_x.ravel(),shift_y.ravel()
    shifts = vstack((shift_x,shift_y,shift_x,shift_y))
    shifts = shifts[None,:].transpose([2,0,1])
    all_anchors = _anchors + shifts
    all_anchors = anchors.reshape((width*height*_anchors_num,4))
    total_anchors = int(shifts.shape[0]*9)

    inds_inside = where(
        (all_anchors[:,0]>=-_allowed_border)&
        (all_anchors[:,1]>=-_allowed_border)&
        (all_anchors[:,2]<im_info[1]+_allowed_border)&
        (all_anchors[:,3]<im_info[1]+_allowed_border)
    )[0]

    anchors = all_anchors[inds_inside,:]
    labels = empty((len(inds_inside),),dtype=float32)
    labels.fill(-1)

    # overlaps
    overlaps = zeros((len(anchors),len(gt_boxes)))
    for i in arange(len(anchors)):
        for j in arange(len(gt_boxes)):
            x1,y1,x2,y2 = anchors[i]
            X1,Y1,X2,Y2 = gt_boxes[j]
            xx1 = max(x01,x11)
            yy1 = max(y01,y11)
            xx2 = min(x02,x12)
            yy2 = min(y02,y12)
            w = xx2 - xx1
            h = yy2 - yy1
            iou = w*h
            if w>0 and h>0:
                sa = (x2-x1)*(y2-y1)
                sb = (X2-X1)*(Y2-Y1)
                overlaps[i,j] = iou / (sa + sb - iou)

    argmax_overlaps = overlaps.argmax(axis=1)
    max_overlaps    = overlaps[arange(len(inds_inside)),argmax_overlaps]

    gt_argmax_overlaps = overlaps.argmax(axis=0)
    gt_max_overlaps    = overlaps[gt_argmax_overlaps,arange(overlaps.shape[1])]
    gt_argmax_overlaps = where(overlaps == gt_max_overlaps)[0]

    # ? TRAIN.RPN_CLOBBER_POSITIVES
    labels[gt_argmax_overlaps] = 1
    labels[max_overlaps>=.7] = 1
    labels[max_overlaps<.3] = 0

    # NO dontcare_area and NO hard_sample

    # subsample positive and negative if them is too many
    num_fg = .5 * 256
    fg_inds = where(labels == 1)[0]
    if len(fg_inds) > num_fg:
        disable_inds = random.choice(fg_inds,len(fg_inds)-num_fg,replace=False)
        labels[disable_inds] = -1
    num_bg = .5 * 256
    bg_inds = where(labels == 0)[0]
    if len(bg_inds) > num_bg:
        disable_inds = random.choice(bg_inds,len(bg_inds)-num_bg,replace=False)
        labels[disable_inds] = -1

    # ? bbox_targets = zeros((len(inds_inside), 4), dtype=float32)
    # compare anchors,gt_boxes[argmax_overlaps,:]
    gt_box = gt_boxes[argmax_overlaps,:]
    ex_w = anchors[:,2] - anchors[:,0] + 1.
    ex_h = anchors[:,3] - anchors[:,1] + 1.
    ex_ctr_x = anchors[:,0] + .5 * ex_w
    ex_ctr_y = anchors[:,1] + .5 * ex_h
    gt_w = gt_box[:,2] - gt_box[:,0] + 1.
    gt_h = gt_box[:,3] - gt_box[:,1] + 1.
    gt_ctr_x = gt_box[:,0] + .5 * gt_w
    gt_ctr_y = gt_box[:,1] + .5 * gt_h
    dx = (gt_ctr_x - ex_ctr_x)/ex_w
    dy = (gt_ctr_y - ex_ctr_y)/ex_h
    dw = log(gt_w/ex_w)
    dh = log(gt_h/ex_h)
    bbox_targets = vstack((dx,dy,dw,dh)).transpose()
    
    bbox_inside_weights = zeros((len(inds_inside), 4), dtype=float32)
    bbox_inside_weights[labels==1,:] = array((1.,1.,1.,1.))
    # ? RPN_POSITIVE_WEIGHT = -1
    bbox_outside_weights = zeros((len(inds_inside), 4), dtype=float32)
    bbox_outside_weights[labels==1,:] = ones((1,4))
    bbox_outside_weights[labels==0,:] = zeros((1,4))

    # labels,bbox_target,bbox_inside_weight,bbox_ouside_weight
    # total_anchors,inds_inside
    t_labels                            = empty((total_anchors,)).fill(-1)
    t_labels[inds_inside]               = labels
    t_bbox_targets                      = empty((total_anchors,4)).fill(0)
    t_bbox_targets[inds_inside]         = bbox_targets
    t_bbox_inside_weights               = empty((total_anchors,4)).fill(0)
    t_bbox_inside_weights[inds_inside]  = bbox_inside_weights
    t_bbox_outside_weights              = empty((total_anchors,4)).fill(0)
    t_bbox_outside_weights[inds_inside] = bbox_outside_weights

    labels               = t_labels.reshape((1,height,width,9))
    bbox_targets         = t_bbox_targets((1,height,width,9*4))
    bbox_inside_weights  = t_bbox_inside_weights((1,height,width,9*4))
    bbox_outside_weights = t_bbox_outside_weights((1,height,width,9*4))

    return labels,bbox_targets,bbox_inside_weights,bbox_outside_weights

# -------------------------------------------------------------------------------------------
def proposal_target_layer(rpn_rois):
    pass


# build_loss1.0
def smooth_l1_dist(deltas, sigma2=9.0):
    deltas_abs = tf.abs(deltas)
    smoothL1_sign = tf.cast(tf.less(deltas_abs, 1.0/sigma2), tf.float32)
    return tf.square(deltas) * 0.5 * sigma2 * smoothL1_sign + \
                (deltas_abs - 0.5 / sigma2) * tf.abs(smoothL1_sign - 1)

def build_anchor_loss(rpn_cls_score,gt_boxes,im_info):
    labels,bbox_targets,bbox_inside_weights,bbox_outside_weights =
        tf.py_func(anchors_target_layer,[rpn_cls_score,gt_boxes,im_info],tf.float32)
    
    # find keeps_index
    rpn_label           = tf.reshap(labels, [-1])
    fg_keep             = tf.equal(rpn_label, 1)
    rpn_keep            = tf.where(tf.not_equal(rpn_label, -1))

    # label_score_loss
    rpn_label           = tf.reshape(tf.gather(rpn_label, rpn_keep), [-1])
    rpn_cls_score       = tf.reshape(tf.gather(rpn_cls_score, rpn_keep), [-1, 2])
    rpn_cross_entropy_n = tf.nn.sparse_softmax_cross_entropy_with_logits(logits=rpn_cls_score, labels=rpn_label)
    rpn_cross_entropy   = tf.reduce_mean(rpn_cross_entropy_n)

    # box_score_loss
    rpn_bbox_targets         = bbox_targets
    rpn_bbox_pred            = tf.reshape(tf.gather(tf.reshape(rpn_bbox_pred, [-1, 4]), rpn_keep), [-1, 4])
    rpn_bbox_inside_weights  = bbox_inside_weights
    rpn_bbox_outside_weights = bbox_outside_weights
    rpn_bbox_pred            = tf.reshape(tf.gather(tf.reshape(rpn_bbox_pred, [-1, 4]), rpn_keep), [-1, 4]) # shape (N, 4)
    rpn_bbox_targets         = tf.reshape(tf.gather(tf.reshape(rpn_bbox_targets, [-1, 4]), rpn_keep), [-1, 4])
    rpn_bbox_inside_weights  = tf.reshape(tf.gather(tf.reshape(rpn_bbox_inside_weights, [-1, 4]), rpn_keep), [-1, 4])
    rpn_bbox_outside_weights = tf.reshape(tf.gather(tf.reshape(rpn_bbox_outside_weights, [-1, 4]), rpn_keep), [-1, 4])
    rpn_loss_box_n           = tf.reduce_sum(smooth_l1_dist(
                                             rpn_bbox_inside_weights * (rpn_bbox_pred - rpn_bbox_targets)), axis=[1])
    rpn_loss_box = tf.reduce_sum(rpn_loss_box_n) / (tf.reduce_sum(tf.cast(fg_keep, tf.float32)) + 1.0)

    # fc_loss...

    return rpn_loss_box,rpn_cross_entropy

rpn_loss_box,rpn_cross_entropy = build_anchor_loss(rpn_cls_score,gt_boxes,im_info)

'''
rpn_rois = tf.py_func(proposal_layer,[rpn_cls_prob_reshape,rpn_bbox_pred,im_info],tf.float32)
sess = tf.Session()
sess.run(tf.global_variables_initializer())

import cv2,time
s = cv2.imread('nier.jpg')
v = s.shape[:2]
p = s[None,:]
v = array([list(v)+[.5]])
tim = time.time()
m = sess.run(rpn_rois, feed_dict={inpt:p,im_info:v})
print(time.time()-tim)
for x1,y1,x2,y2 in m:
    rd = random.randint
    cv2.rectangle(s,(x1,y1),(x2,y2),(rd(0,255),rd(0,255),rd(0,255)),rd(3,6))

s.astype(int32)
s = cv2.resize(s,tuple(array(s.shape[:2][::-1])//2))
cv2.imshow('nier',s)
cv2.waitKey()
cv2.destroyAllWindows()

'''





