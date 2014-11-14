from django.conf.urls import url

from .views import (
    Profile,
    login,
    logout,
    Signup,
)


urlpatterns = (
    # User Login
    url(r'^login/$',
        login, name='login'),

    # User Logout
    url(r'^logout/$',
        logout, name='logout'),

    # User Profile
    url(r'^profile/$',
        Profile.as_view(), name='profile'),

    # User Signup
    url(r'^cadastro/$',
        Signup.as_view(), name='signup'),
)
