from django.shortcuts import render, HttpResponse
from django.conf import settings
from django.contrib import messages


import os


from .functions import trim_audio_fun, generate_spectrogram_fun, extract_audio_fun, noise_reduction_fun, train_model_fun
from .forms import TrimAudioForm, NoiseReductionForm, SpectrogramForm, ExtractAudioForm, TrainModelForm, MixAudioForm
from .models import TrimAudio, NoiseReduction, MixAudio, ExtractAudio


project_name = "noise_reduction"
default_save_location = os.path.expanduser(f'~/Documents/{project_name}')
models_location = os.path.join(default_save_location, 'models')


def home(request):
    context = {}
    return render(request, 'base/home.html', context)


def noise_reduction(request):
    form = NoiseReductionForm()
    context = {'form': form}
    if request.method == 'POST':
        form = NoiseReductionForm(request.POST, request.FILES)
        if form.is_valid():
            new_audio = NoiseReduction(audio_file=request.FILES['audio_file'])
            new_audio.save()
            temp_model = request.POST['model']
            file_name = new_audio.audio_file.name.split('/')
            file_path = os.path.join(settings.MEDIA_ROOT, new_audio.audio_file.name)
            model = os.path.join(models_location, temp_model)
            noise_reduction_fun(
                model_name=model, file_name=file_name, file_path=file_path, sample_rate=request.POST['sample_rate'])
            messages.success(request, 'Audio file cleaned Successfully')
            return render(request, 'base/noise_reduction.html', context=context)
    return render(request, 'base/noise_reduction.html', context)


def trim_audio(request):
    form = TrimAudioForm()
    context = {'form': form}
    if request.method == 'POST':
        form = TrimAudioForm(request.POST, request.FILES)
        if form.is_valid():
            new_doc = TrimAudio(audio_file=request.FILES['audio_file'])
            new_doc.save()
            file_name = new_doc.audio_file.name.split('/')
            file_path = os.path.join(settings.MEDIA_ROOT, new_doc.audio_file.name)
            trim_audio_fun(
                file_path, int(request.POST['start_time']), int(request.POST['end_time']), file_name[2])
            messages.success(request, 'The Audio File has been trimmed successfully')
            return render(request, 'base/trim_audio.html', context)
        else:
            messages.error(request, 'There was an error in the form, Please check')

    return render(request, 'base/trim_audio.html', context)


def train_your_model(request):
    form = TrainModelForm()
    context = {'form': form}
    if request.method == 'POST':
        form = TrainModelForm(request.POST)
        if form.is_valid():
            clean_folder_path = request.POST['clean_folder']
            noisy_folder_path = request.POST['noisy_folder']
            train_size = request.POST['train_size']
            model_file_name = request.POST['model_file_name']
            model_file_path = os.path.join(models_location, model_file_name)
            batch_size = request.POST['batch_size']
            model_loss = train_model_fun(
                noisy_folder_path=noisy_folder_path,
                clean_folder_path=clean_folder_path,
                train_size=train_size,
                batch_size=batch_size,
                model_file_path=model_file_path
            )
            messages.success(request, f"Model trained successfully. And the loss is {model_loss}")
            return render(request, 'base/train_your_model.html', context)

    return render(request, 'base/train_your_model.html', context)


def mix_audio(request):
    if request.method == 'POST':
        form = MixAudioForm(request.POST, request.FILES)
        if form.is_valid():
            new_audio = MixAudio(audio_file1=request.FILES['audio_file1'], audio_file2=request.FILES['audio_file2'])
            new_audio.save()
            return HttpResponse('Audio Files uploaded successfully')
    else:
        form = MixAudioForm()
    context = {'form': form}
    return render(request, 'base/mix_audio.html', context)


def extract_audio(request):
    form = ExtractAudioForm()
    context = {'form': form}
    if request.method == 'POST':
        form = ExtractAudioForm(request.POST, request.FILES)
        if form.is_valid():
            new_video = ExtractAudio(video_file=request.FILES['video_file'])
            new_video.save()
            file_name = new_video.video_file.name.split('/')[2]
            file_path = os.path.join(settings.MEDIA_ROOT, new_video.video_file.name)
            extract_audio_fun(file_path, request.POST['audio_format'], file_name)
            messages.success(request, 'Audio has been successfully extracted')
            return render(request, 'base/extract_audio.html', context)
    return render(request, 'base/extract_audio.html', context)


def generate_spectrogram(request):
    form = SpectrogramForm()
    context = {'form': form}
    if request.method == 'POST':
        form = SpectrogramForm(request.POST)
        if form.is_valid():
            generate_spectrogram_fun(
                request.POST['folder_path'], int(request.POST['sample_rate']), request.POST['spectrogram_type']
            )
            messages.success(request, 'Successfully generated spectrogram')
            return render(request, 'base/spectrogram.html', context)

    return render(request, 'base/spectrogram.html', context)
