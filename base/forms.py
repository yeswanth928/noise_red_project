from django import forms
import os


project_name = "project7"
default_save_location = os.path.expanduser(f'~/Documents/{project_name}')
models_location = os.path.join(default_save_location, 'models')
model = models = [model for model in os.listdir(models_location)]


class TrimAudioForm(forms.Form):
    audio_file = forms.FileField(
        label='Audio File',
        allow_empty_file=False,
        widget=forms.TextInput(attrs={'class': 'inputStyle'})
    )
    start_time = forms.IntegerField(
        min_value=0,
        widget=forms.TextInput(attrs={'class': 'inputStyle'})
    )
    end_time = forms.IntegerField(
        min_value=1,
        widget=forms.TextInput(attrs={'class': 'inputStyle'})
    )


class SpectrogramForm(forms.Form):
    folder_path = forms.CharField(
        label='Enter the folder path',
        widget=forms.TextInput(attrs={'class': 'inputStyle'})
    )
    spectrogram_type = forms.ChoiceField(
        choices=(("hz", "hz"),
                 ("log", "log"),),
        label='Select Spectrogram type',
        widget=forms.Select(attrs={'class': 'selectStyle'})
    )
    sample_rate = forms.IntegerField(
        label='Enter the sample rate',
        widget=forms.TextInput(attrs={'class': 'inputStyle'})
    )


class NoiseReductionForm(forms.Form):
    audio_file = forms.FileField(
        label='Select the Audio File',
        allow_empty_file=False
    )
    model = forms.ChoiceField(
        label='Choose the model',
        choices=((model, model) for model in models),
    )
    sample_rate = forms.IntegerField(
        label="Enter the sample rate",
        required=False,
        initial=48000
    )


class ExtractAudioForm(forms.Form):
    video_file = forms.FileField(
        label='Select the Video File',
        allow_empty_file=False,
        widget=forms.FileInput(attrs={'class': 'fileStyle;'})
    )
    audio_format = forms.ChoiceField(
        label='Audio Format',
        choices=(("mp3", "mp3"), ("wav", "wav"), ("ogg", "ogg")),
        widget=forms.TextInput(attrs={'class': 'inputStyle', 'placeholder': 'Select the audio format'})
    )


class MixAudioForm(forms.Form):
    audio_file1 = forms.FileField(
        label='Select the First Audio File',
        allow_empty_file=False
    )
    audio_file2 = forms.FileField(
        label='Select the Second Audio File',
        allow_empty_file=False
    )


class TrainModelForm(forms.Form):
    clean_folder = forms.CharField(
        label='Enter the Clean sounds folder path',
        required=True
    )
    noisy_folder = forms.CharField(
        label='Select the Noisy sounds folder path',
        required=True
    )
    train_size = forms.IntegerField(
        label='Select the training percentage',
        required=True,
        min_value=50,
        max_value=99
    )
    model_file_name = forms.CharField(
        label='Name of the Model',
        required=True
    )
    batch_size = forms.IntegerField(
        label='Batch Size',
        required=False
    )

