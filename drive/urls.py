from django.urls import path
from . import views

urlpatterns = [path('data/<path:path>', views.data, name='data'),
               path('upload_file/<path:path>', views.upload_file, name='upload_file'),
               path('create_folder/<path:path>', views.create_folder, name='create_folder'),
               path('download_file/<int:id>', views.download_file, name='download_file'),
               ]
