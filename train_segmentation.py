from models import unet, segnet
from utils import segdata_generator
from keras.optimizers import Adam
from keras import backend as K
import os
import argparse

K.clear_session()


def main():
    nClasses = 12
    train_batch_size = 5
    val_batch_size = 1
    init_lr = 0.001
    epochs = 20
    img_height = 360
    img_width = 480
    loss_weight = [0.2595, 0.1826, 4.5640, 0.1417, 0.9051, 0.3826, 9.6446, 1.8418, 0.6823, 6.2478, 7.3614, 1.0974]
    train_images_path = args.img_path + 'images_prepped_train/'
    train_segs_path = args.img_path + 'annotations_prepped_train/'
    val_images_path = args.img_path + 'images_prepped_test/'
    val_segs_path = args.img_path + 'annotations_prepped_test/'
    if args.model == 'unet':
        model = unet.Unet(nClasses, input_height=img_height, input_width=img_width)
    elif args.model == 'segnet':
        model = segnet.SegNet(nClasses, input_height=img_height, input_width=img_width)
    else:
        raise ValueError('Does not support {}, only supports unet and segnet now'.format(args.model))

    model.compile(loss='categorical_crossentropy',
                  optimizer='adam',
                  metrics=['accuracy'])
    model.summary()

    train = segdata_generator.imageSegmentationGenerator(train_images_path, train_segs_path, train_batch_size, nClasses,
                                                         img_height, img_width, 360, 480)

    val = segdata_generator.imageSegmentationGenerator(val_images_path, val_segs_path, val_batch_size, nClasses,
                                                       img_height, img_width, 360, 480)

    model.fit_generator(train,
                        steps_per_epoch=367 // train_batch_size,
                        validation_data=val,
                        validation_steps=101 // val_batch_size,
                        epochs=epochs,
                        class_weight=loss_weight)
    if not os.path.exists('./results/'):
        os.mkdir('./results')
    model.save_weights('./results/{}_weights.h5'.format(args.model))


if __name__ == '__main__':
    parse = argparse.ArgumentParser(description='command for training segmentation models with keras')
    parse.add_argument('--model', type=str, default='segnet', help='support unet, segnet')
    parse.add_argument('--img-path', type=str, default='./data/', help='the path of training data and test data')
    args = parse.parse_args()

    main()
