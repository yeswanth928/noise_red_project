from django import forms


class TrimAudioForm(forms.Form):
    audio_file = forms.FileField(
        label='Select the audio file',
        help_text='max 42 megabytes',
        allow_empty_file=False
    )
    start_time = forms.IntegerField(min_value=0)
    end_time = forms.IntegerField(min_value=1)


class SpectrogramForm(forms.Form):
    folder_path = forms.CharField(
        label='Enter the folder path',
    )
    spectrogram_type = forms.ChoiceField(
        choices=(("hz", "hz"),
                 ("log", "log"),),
        label='Select Spectrogram type',
    )
    sample_rate = forms.IntegerField(
        label='Enter the sample rate'
    )


class NoiseReductionForm(forms.Form):
    audio_file = forms.FileField(
        label='Select the Audio File',
        help_text='max 42 MB',
        allow_empty_file=False
    )


class ExtractAudioForm(forms.Form):
    video_file = forms.FileField(
        label='Select the Video File',
        help_text='max 42 MB',
        allow_empty_file=False
    )
    audio_format = forms.ChoiceField(
        label='Select the audio format',
        choices=(("mp3", "mp3"), ("wav", "wav"), ("ogg", "ogg"))
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
