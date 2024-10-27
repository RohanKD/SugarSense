import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow.keras.applications import ResNet50
from tensorflow.keras.layers import Dense, Dropout, Input, Conv2D, multiply, GlobalAveragePooling2D, BatchNormalization, \
    Lambda
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import ModelCheckpoint, EarlyStopping, ReduceLROnPlateau
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import confusion_matrix
import itertools
import warnings
from tensorflow.data import Dataset

warnings.filterwarnings('ignore')


def download_kaggle_data():
    if not os.path.exists('./data/train_11') or not os.path.exists('./trainLabels.csv'):
        print("Downloading dataset from Kaggle...")
        os.system('kaggle competitions download -c diabetic-retinopathy-detection -p ./data')
        os.system('unzip -o ./data/diabetic-retinopathy-detection.zip -d ./data')
        print("Download complete.")


def load_labels_and_paths(base_dir, label_csv):
    train_labels = pd.read_csv(label_csv)
    train_labels['path'] = train_labels['image'].map(lambda x: os.path.join(base_dir, f'{x}.jpeg'))
    train_labels = train_labels[train_labels['path'].map(os.path.exists)]
    return train_labels


def parse_image(filename, label):
    image = tf.io.read_file(filename)
    image = tf.image.decode_jpeg(image, channels=3)
    image = tf.image.resize(image, [224, 224])
    image /= 255.0
    return image, label


def load_dataset(file_paths, labels, batch_size=32):
    dataset = Dataset.from_tensor_slices((file_paths, labels))
    dataset = dataset.map(parse_image, num_parallel_calls=tf.data.AUTOTUNE)
    dataset = dataset.shuffle(buffer_size=len(file_paths)).batch(batch_size)
    dataset = dataset.prefetch(buffer_size=tf.data.AUTOTUNE)
    return dataset

def create_deeper_attention_model(input_shape, num_classes, learning_rate=0.0001):
    in_lay = Input(input_shape)
    base_model = ResNet50(input_shape=input_shape, include_top=False, weights='imagenet')
    base_model.trainable = False
    pt_features = base_model(in_lay)
    bn_features = BatchNormalization()(pt_features)

    attn_layer = Conv2D(128, kernel_size=(3, 3), padding='same', activation='relu')(Dropout(0.5)(bn_features))
    attn_layer = Conv2D(1, kernel_size=(1, 1), padding='valid', activation='sigmoid')(attn_layer)
    mask_features = multiply([attn_layer, bn_features])

    gap_features = GlobalAveragePooling2D()(mask_features)
    gap_mask = GlobalAveragePooling2D()(attn_layer)
    gap = Lambda(lambda x: x[0] / x[1], name='RescaleGAP')([gap_features, gap_mask])
    dr_steps = Dropout(0.5)(Dense(256, activation='relu')(gap))
    out_layer = Dense(num_classes, activation='softmax')(dr_steps)

    model = Model(inputs=[in_lay], outputs=[out_layer])
    model.compile(optimizer=Adam(learning_rate=learning_rate), loss='categorical_crossentropy',
                  metrics=['categorical_accuracy', 'AUC'])
    return model


def balance_data(df, class_size):
    train_df = df.groupby('level').apply(lambda x: x.sample(class_size, replace=True)).reset_index(drop=True)
    return train_df.sample(frac=1).reset_index(drop=True)


def show_confusion_matrix(cm, target_names):
    plt.figure(figsize=(8, 8))
    plt.imshow(cm, interpolation='nearest', cmap='Blues')
    plt.colorbar()
    plt.xticks(np.arange(len(target_names)), target_names, rotation=45)
    plt.yticks(np.arange(len(target_names)), target_names)

    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        plt.text(j, i, format(cm[i, j], 'd'), horizontalalignment="center", color="black")

    plt.ylabel('True label')
    plt.xlabel('Predicted label')
    plt.tight_layout()
    plt.show()


def train_model(dataframe, base_dir):
    n_splits = 10
    skf = StratifiedKFold(n_splits=n_splits, shuffle=True, random_state=42)
    cumulative_cm = None
    all_results = {'train_accu': [], 'val_accu': [], 'train_loss': [], 'val_loss': [], 'train_auc': [], 'val_auc': []}

    for fold, (train_idx, val_idx) in enumerate(skf.split(dataframe, dataframe['level'])):
        train_df, val_df = dataframe.iloc[train_idx], dataframe.iloc[val_idx]
        max_class_size = train_df['level'].value_counts().max()
        train_df = balance_data(train_df, max_class_size)

        train_gen = ImageDataGenerator(rescale=1.0 / 255, shear_range=0.2, horizontal_flip=True, zoom_range=0.2)
        val_gen = ImageDataGenerator(rescale=1.0 / 255)

        train_flow = train_gen.flow_from_dataframe(train_df, directory=base_dir, x_col="path", y_col="level",
                                                   target_size=(256, 256), batch_size=64, class_mode='categorical')
        val_flow = val_gen.flow_from_dataframe(val_df, directory=base_dir, x_col="path", y_col="level",
                                               target_size=(256, 256), batch_size=64, class_mode='categorical')

        if cumulative_cm is None:
            cumulative_cm = np.zeros((len(train_flow.class_indices), len(train_flow.class_indices)), dtype=int)

        model = create_deeper_attention_model((256, 256, 3), len(train_flow.class_indices))

        callbacks = [
            ModelCheckpoint('resnet50_best', monitor="val_categorical_accuracy", save_best_only=True, mode="max"),
            EarlyStopping(monitor='val_categorical_accuracy', patience=15, restore_best_weights=True),
            ReduceLROnPlateau(monitor='val_loss', factor=0.1, patience=7, min_lr=1e-7)
        ]

        history = model.fit(train_flow, epochs=5, validation_data=val_flow, callbacks=callbacks)

        train_loss, train_accu, train_auc = model.evaluate(train_flow)
        val_loss, val_accu, val_auc = model.evaluate(val_flow)

        all_results['train_accu'].append(train_accu)
        all_results['val_accu'].append(val_accu)
        all_results['train_loss'].append(train_loss)
        all_results['val_loss'].append(val_loss)
        all_results['train_auc'].append(train_auc)
        all_results['val_auc'].append(val_auc)

        y_pred_train = model.predict(train_flow)
        y_pred_train = np.argmax(y_pred_train, axis=1)
        cm_train = confusion_matrix(train_flow.classes, y_pred_train)
        cumulative_cm += cm_train


    print(
        f"Mean train accuracy: {np.mean(all_results['train_accu']):.2f}, Mean val accuracy: {np.mean(all_results['val_accu']):.2f}")
    show_confusion_matrix(cumulative_cm / n_splits, list(train_flow.class_indices.keys()))


if __name__ == '__main__':
    base_dir = "./data/train_11"
    label_csv = "./data/trainLabels.csv"

    download_kaggle_data()

    df = load_labels_and_paths(base_dir, label_csv)
    df['level'] = df['level'].astype(str)
    train_model(df, base_dir)
