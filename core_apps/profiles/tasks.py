from uuid import UUID
from celery import shared_task
from .models import Profile
from cloudinary import uploader


@shared_task(name="upload_avatar_to_cloudinary")
def upload_avatar_to_cloudinary(profile_id: UUID, image_content: bytes) -> None:
    profile = Profile.objects.get(id=profile_id)
    response = uploader.upload(image_content)
    profile.avatar = response["secure_url"]
    profile.save()


@shared_task(name="update_reputation_score")
def update_reputation_score():
    for profile in Profile.objects.all():
        profile.update_reputation()
        profile.save()