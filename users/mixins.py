from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import redirect, reverse


class LoggedOutOnlyView(UserPassesTestMixin):
    permission_denied_message = "Page not found"

    def test_func(self):
        return not self.request.user.is_authenticated

    def handle_no_permission(self):
        return redirect(reverse("core:home"))
