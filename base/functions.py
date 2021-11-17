from django.conf import settings

import librosa
import librosa.display
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
import moviepy.editor as mp
import os
import tensorflow as tf

project_name = "project7"
default_save_location = os.path.expanduser(f'~/Documents/{project_name}')


def create_folder(folder_name: str):
    if not os.path.exists(default_save_location):
        os.mkdir(default_save_location)
    folder_path = os.path.join(default_save_location, folder_name)
    if not os.path.exists(folder_path):
        os.mkdir(folder_path)
    return folder_path


def trim_audio_fun(file_path: str, start_time: int, end_time: int, new_file_name: str):
    folder_path = "Trimming"
    new_file_path = os.path.join(folder_path, new_file_name)
    ffmpeg_extract_subclip(file_path, start_time, end_time, new_file_path)


def generate_spectrogram_fun(audio_folder_path: str, sample_rate: int, spectrogram_type: str):
    folder_path = create_folder("Spectrogram")
    if os.path.exists(audio_folder_path):
        audio_list = {
            os.path.join(audio_folder_path, audio): audio for audio in os.listdir(audio_folder_path) if
            audio.lower().endswith(('.wav',))
        }
        for audio_abs_path, audio_file in audio_list.items():
            audio_file_name = audio_file.split('.')
            spectrogram(audio_abs_path, folder_path, audio_file_name[0]+'.png', sample_rate, spectrogram_type)


def spectrogram(file_path, save_folder_path, file_name, sample_rate, spectrogram_type):
    data, samp_rate = librosa.load(file_path, sr=sample_rate)
    data = librosa.stft(data)
    data_db = librosa.amplitude_to_db(abs(data))
    fig = plt.Figure()
    canvas = FigureCanvas(fig)
    ax = fig.add_subplot(111)
    librosa.display.specshow(data_db, sr=sample_rate, x_axis="time", y_axis=spectrogram_type, ax=ax)
    fig.savefig(os.path.join(save_folder_path, file_name))


def extract_audio_fun(file_path: str, audio_format: str, file_name: str):

    folder_path = create_folder("Extract_Audio")
    new_file_path = os.path.join(folder_path, file_name.split('.')[0]+"."+audio_format)
    temp_video = mp.VideoFileClip(file_path)
    temp_audio = temp_video.audio
    temp_audio.write_audiofile(new_file_path)


def pre_processing(file_path: str):
    audio, _ = tf.audio.decode_wav(tf.io.read_file(file_path), 1)
    audio_len = audio.shape[0]
    batching_size = 12000
    batches = []
    i = 0
    for i in range(0, audio_len-batching_size, batching_size):
        batches.append(audio[i:i+batching_size])
    batches.append(audio[-batching_size:])
    d = audio_len - (i + batching_size)
    return tf.stack(batches), d


def generate_clean_audio(file_path: str, model_path: str):
    pre_processed_data, diff = pre_processing(file_path)
    model = tf.keras.models.load_model(model_path)
    temp_out = model.predict(pre_processed_data)
    temp_out_post = tf.reshape(temp_out[:-1], ((temp_out.shape[0] - 1) * temp_out.shape[1], 1))
    final_out = tf.concat((temp_out_post, temp_out[-1][-diff:]), axis=0)
    return final_out


def noise_reduction_fun(model_name: str, file_path: str, file_name: str, sample_rate: int = 48000):
    folder_path = create_folder(folder_name='noise_reduction')
    new_file_path = os.path.join(folder_path, file_name)
    model_path = os.path.join(settings.MEDIA_ROOT, model_name)
    audio_val = generate_clean_audio(file_path, model_path)
    output = tf.squeeze(audio_val)
    encoded_output = tf.audio.encode_wav(output, sample_rate=sample_rate, name=file_name)
    tf.write_file(new_file_path, encoded_output)

