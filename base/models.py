from django.db import models


upload_destination_audio = 'documents/audio'
upload_destination_video = 'documents/video'


class TrimAudio(models.Model):
    audio_file = models.FileField(upload_to=upload_destination_audio)


class Spectrogram(models.Model):
    audio_file = models.FileField(upload_to=upload_destination_audio)


class ExtractAudio(models.Model):
    video_file = models.FileField(upload_to=upload_destination_video)


class MixAudio(models.Model):
    audio_file1 = models.FileField(upload_to=upload_destination_audio)
    audio_file2 = models.FileField(upload_to=upload_destination_audio)


class NoiseReduction(models.Model):
    audio_file = models.FileField(upload_to=upload_destination_audio)

