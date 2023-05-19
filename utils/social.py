from accounts.models import User


def get_social_image(user_pk):
    user = User.objects.get(pk=user_pk)
    social_accounts = user.socialaccount_set.all()
    if social_accounts:
        image_url = social_accounts[0].get_picture_url()
        if image_url:
            print(image_url)
