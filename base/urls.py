from . import views
from django.urls import path


urlpatterns = [
    path('', views.home, name='home'),
    path('extract-audio/', views.extract_audio, name='extract-audio'),
    path('noise-reduction/', views.noise_reduction, name='noise-reduction'),
    path('mix-audio/', views.mix_audio, name='mix-audio'),
    path('trim-audio/', views.trim_audio, name='trim-audio'),
    path('train-your-model', views.train_your_model, name='train-your-model'),
    path('generate-spectrogram', views.generate_spectrogram, name='generate-spectrogram')
]
