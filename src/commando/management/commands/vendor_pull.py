from typing import Any
from django.core.management.base import BaseCommand
from helpers.downloader import download_to_local
from django.conf import settings

STATIC_FILES_VENDORS = settings.STATIC_FILES_VENDORS

urls = {
        'flowbite.min.css': 'https://cdn.jsdelivr.net/npm/flowbite@2.5.2/dist/flowbite.min.css',
        'flowbite.min.js':'https://cdn.jsdelivr.net/npm/flowbite@2.5.2/dist/flowbite.min.js',
        'flowbite.min.js.map': 'https://cdn.jsdelivr.net/npm/flowbite@2.5.2/dist/flowbite.min.js.map'
    }

class Command(BaseCommand):

    def handle(self, *args: Any, **options: Any):
        completed_url = set()
        for destination, url in urls.items():
            correct_dest = STATIC_FILES_VENDORS / destination
            dl_success = download_to_local(url=url, destination=correct_dest)
            if dl_success:
                completed_url.add(url)
            else:
                self.stdout.write(
                    self.style.ERROR(f'Failed to download {correct_dest}')
                )
        if completed_url == set(urls.values()):
            self.stdout.write(
                self.style.SUCCESS('Successfully updated vendors static files')
            )
        else:
            self.stdout.write(
                self.style.ERROR('Something went wrong!')
            )