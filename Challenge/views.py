from django.shortcuts import render
from django.utils import timezone
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from Question.models import StudentAnswer
from .models import Challenge, StudentChallengeAttempt
from .serializer import ChallengeSerializer, StudentChallengeAttemptSerializer


# Create your views here.
class ChallengeViewSet(viewsets.ModelViewSet):
    queryset = Challenge.objects.all()
    serializer_class = ChallengeSerializer

    @action(detail=False, methods=['get'])
    def today(self, request):
        today = timezone.now().date()
        challenge, created = Challenge.objects.get_or_create(date=today)

        if created:
            try:
                challenge.generate_questions(num_easy=3, num_medium=2, num_hard=1)
            except ValueError as e:
                return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(challenge)
        return Response(serializer.data)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class StudentChallengeAttemptViewSet(viewsets.ModelViewSet):
    queryset = StudentChallengeAttempt.objects.all()
    serializer_class = StudentChallengeAttemptSerializer

    @action(detail=False, methods=['post'])
    def calculate_score(self, request):
        attempt_id = request.data.get('attempt_id')
        if not attempt_id:
            return Response({"detail": "attempt_id is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            attempt = StudentChallengeAttempt.objects.get(id=attempt_id)
        except StudentChallengeAttempt.DoesNotExist:
            return Response({"detail": "Challenge attempt not found."}, status=status.HTTP_404_NOT_FOUND)

        correct_answers_count = StudentAnswer.objects.filter(
            challenge_attempt=attempt,
            is_correct=True
        ).count()

        attempt.score = correct_answers_count
        attempt.end_time = timezone.now()

        attempt.save()

        time_taken = attempt.end_time - attempt.start_time

        return Response({
            'score': attempt.score,
            'total_questions': attempt.total_questions,
            'time_taken': str(time_taken)
        }, status=status.HTTP_200_OK)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            self.perform_update(serializer)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
