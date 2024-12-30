from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    content = models.CharField(max_length=200)
    timestamp = models.DateTimeField(auto_now=True)

    def serialize(self):
        return {
            "id": self.id,
            "user": {
                "id": self.user.id,
                "usenname": self.user.username
            },
            "content": self.content,
            "timestamp": self.timestamp
        }

    def __str__(self):
        return f"{self.id} by {self.user} ({self.timestamp})"

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="likes")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="likes")

    def __str__(self):
        return f"{self.id} by {self.user} on post {self.post}"

class Follower(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="followers")
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name="following")

    def __str__(self):
        return f"{self.id}: {self.follower} following {self.user}"
