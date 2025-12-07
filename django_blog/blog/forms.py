from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

User = get_user_model()


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user


class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("first_name", "last_name", "email")


from .models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ("title", "content")
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "content": forms.Textarea(attrs={"class": "form-control", "rows": 10}),
        }
    tags = forms.CharField(
        required=False,
        help_text="Comma-separated tags",
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields["tags"].initial = ", ".join([t.name for t in self.instance.tags.all()])

    def save(self, commit=True):
        # Save post instance and handle tags (create if not exists)
        post = super().save(commit=False)
        if commit:
            post.save()
        tags_str = self.cleaned_data.get("tags", "")
        tag_names = [t.strip() for t in tags_str.split(",") if t.strip()]
        from .models import Tag

        tag_objs = []
        for name in tag_names:
            obj, _ = Tag.objects.get_or_create(name=name)
            tag_objs.append(obj)

        if commit:
            post.tags.set(tag_objs)
        else:
            # store for later setting by calling code
            self._tag_objs = tag_objs
        return post
