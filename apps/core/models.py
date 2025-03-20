# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission, BaseUserManager


class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(username, email, password, **extra_fields)
    
    
# Create your models here.
class User(AbstractUser):
    email = models.EmailField(unique=True)
    profile_picture = models.ImageField(upload_to="profile_pics/", blank=True, null=True)

    # Fix reverse accessor conflicts
    groups = models.ManyToManyField(Group, related_name="custom_user_groups", blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name="custom_user_permissions", blank=True)

# Community Model
class Community(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    supervisor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="supervised_communities")
    members = models.ManyToManyField(User, related_name="joined_communities", through="CommunityMembership")

    def __str__(self):
        return self.name

# Community Membership Model (tracks which users joined which communities)
class CommunityMembership(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    community = models.ForeignKey(Community, on_delete=models.CASCADE)
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "community")

    def __str__(self):
        return f"{self.user.username} in {self.community.name}"

# Event Model
class Event(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    date = models.DateField()
    time = models.TimeField()
    location = models.CharField(max_length=255, blank=True, null=True)
    max_participants = models.PositiveIntegerField()
    event_supervisor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="supervised_events")
    community = models.ForeignKey(Community, on_delete=models.CASCADE, related_name="events")
    interested_users = models.ManyToManyField(User, related_name="interested_events", blank=True)
    attendees = models.ManyToManyField(User, related_name="attended_events", through="EventAttendance")

    def __str__(self):
        return self.title

# Event Attendance Model (tracks who is coming to an event)
class EventAttendance(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "event")

    def __str__(self):
        return f"{self.user.username} attending {self.event.title}"

# Post Model (For Campus Updates & Discussions)
class Post(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    community = models.ForeignKey(Community, on_delete=models.CASCADE, related_name="posts", blank=True, null=True)

    def __str__(self):
        return f"Post by {self.creator.username} on {self.created_at.strftime('%Y-%m-%d')}"

# Permission Model (Tracks supervisors and event supervisors)
class Permission(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    community = models.ForeignKey(Community, on_delete=models.CASCADE, null=True, blank=True, related_name="community_permissions")
    event = models.ForeignKey(Event, on_delete=models.CASCADE, null=True, blank=True, related_name="event_permissions")
    role = models.CharField(max_length=50, choices=[("Community Supervisor", "Community Supervisor"), ("Event Supervisor", "Event Supervisor")])

    class Meta:
        unique_together = ("user", "community", "event", "role")

    def __str__(self):
        return f"{self.user.username} - {self.role}"