import os.path
import tensorflow as tf
from tqdm.notebook import tqdm, trange
import glob


from .model import return_dl_model


def load_clean_data(clean_folder_path: str):
    clean_data = glob.glob(clean_folder_path)
    clean_data.sort()
    clean_sound_list, clean_samp_rate = tf.audio.decode_wav(tf.io.read_file(clean_data[0]), desired_channels=1)
    clean_data[0] = clean_data[0].split('/')[-1]
    for i in tqdm(clean_data[1:]):
        clean_cont, sample_rate = tf.audio.decode_wav(tf.io.read_file(i), desired_channels=1)
        clean_sound_list = tf.concat((clean_sound_list, clean_cont), 0)
        clean_data[i] = clean_data[i].split('/')[-1]
    return clean_data, clean_sound_list


def load_noisy_data(noisy_folder_path, clean_data):
    noisy_data = []
    for file_name in clean_data:
        noisy_data.append(os.path.join(noisy_folder_path, file_name))
    noisy_sound_list, noisy_samp_rate = tf.audio.decode_wav(tf.io.read_file(noisy_data[0]), desired_channels=1)
    for i in tqdm(noisy_data[1:]):
        noisy_cont, sample_rate = tf.audio.decode_wav(tf.io.read_file(i), desired_channels=1)
        noisy_sound_list = tf.concat((noisy_sound_list, noisy_cont), 0)
    return noisy_sound_list


def create_batches(batch_size: int, clean_sound_list: list, noisy_sound_list: list):
    clean_train, noisy_train = [], []
    for i in trange(0, clean_sound_list.shape[0] - batch_size, batch_size):
        clean_train.append(clean_sound_list[i:i + batch_size])
        noisy_train.append(noisy_sound_list[i:i + batch_size])

    clean_train = tf.stack(clean_train)
    noisy_train = tf.stack(noisy_train)
    return clean_train, noisy_train


def get_data(clean_train, noisy_train):
    dataset = tf.data.Dataset.from_tensor_slices((clean_train, noisy_train))
    dataset = dataset.shuffle(100).batch(64, drop_remainder=True)
    return dataset


def create_datasets(clean_train: list, noisy_train: list, training_size: int):
    train_size = round((training_size * clean_train.shape[0]) / 100)
    train_dataset = get_data(noisy_train[:train_size], clean_train[:train_size])
    test_dataset = get_data(noisy_train[train_size:], clean_train[train_size:])
    return train_dataset, test_dataset


def train_model(batch_size: int, train_dataset: list, test_dataset: list, model_file_path: str):
    model = return_dl_model(batch_size)
    model.compile(optimizer=tf.keras.optimizers.Adam(0.002), loss=tf.keras.losses.MeanAbsoluteError())
    model.fit(train_dataset, epochs=20)
    model.save(model_file_path)
    return model.evaluate(test_dataset)


def train_and_save_model(
        noisy_folder_path: str, clean_folder_path: str, train_size: int, model_file_path: str, batch_size: int = 12000):
    clean_data, clean_sound_list = load_clean_data(clean_folder_path=clean_folder_path)
    noisy_sound_list = load_noisy_data(noisy_folder_path=noisy_folder_path, clean_data=clean_data)
    clean_train, noisy_train = create_batches(
        batch_size=batch_size, clean_sound_list=clean_sound_list, noisy_sound_list=noisy_sound_list)
    train_dataset, test_dataset = create_datasets(
        clean_train=clean_train, noisy_train=noisy_train, training_size=train_size)
    model_loss = train_model(
        batch_size=batch_size, train_dataset=train_dataset, test_dataset=test_dataset, model_file_path=model_file_path)
    return model_loss
