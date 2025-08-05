from django.contrib.auth.base_user import BaseUserManager


class CustomUserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_field):
        if not email:
            raise ValueError("Email Required")

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_field)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_field):
        extra_field.setdefault("is_staff", True)
        extra_field.setdefault("is_superuser", True)

        if not extra_field.get("is_staff"):
            raise ValueError("SuperUser must have is_staff True")
        if not extra_field.get("is_superuser"):
            raise ValueError("SuperUser must have is_superuser True")

        return self.create_user(email, password, **extra_field)
