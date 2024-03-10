from django.shortcuts import render
from .models import Approval
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny


class ApprovalView(APIView):
  permission_classes = [IsAuthenticated] #[IsAuthenticated]

  def get_non_approved_users(request):
      # Retrieve non-approved users
      non_approved_users = Approval.objects.filter(is_approved=False)

      # Pass non-approved users to the template
      context = {
          'non_approved_users': non_approved_users
      }
      return render(request, 'approval/non_approved_users.html', context)
