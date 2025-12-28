from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.urls import reverse_lazy


class CustomLoginView(auth_views.LoginView):
    """Custom login view with role-based redirection"""
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True
    
    def get_success_url(self):
        """Redirect to dashboard after successful login"""
        return reverse_lazy('dashboard:home')


class CustomLogoutView(auth_views.LogoutView):
    """Custom logout view"""
    next_page = '/login/'


@login_required
def profile_view(request):
    """User profile view"""
    return redirect('dashboard:home')
