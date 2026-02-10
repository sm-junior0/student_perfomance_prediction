import joblib
import numpy as np
import os
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render
from .models import StudentPerformance
from .serializers import PredictionSerializer

# Load model
MODEL_PATH = os.path.join(os.path.dirname(__file__), 'model.pkl')
_cached_model = None


def get_model():
    global _cached_model
    if _cached_model is None:
        _cached_model = joblib.load(MODEL_PATH)
    return _cached_model


def _make_prediction(validated_data):
    """
    Run the ML model on validated data and return a clamped prediction.
    Accepts the dict returned by serializer.validated_data.
    """
    features = np.array([[
        validated_data['hours_studied'],
        validated_data['previous_scores'],
        1 if validated_data['extracurricular'] else 0,
        validated_data['sleep_hours'],
        validated_data['sample_papers'],
    ]])

    model = get_model()
    prediction = model.predict(features)[0]
    prediction = round(float(prediction), 2)

    # Clamp to valid range
    return max(0, min(prediction, 100))


@api_view(['POST'])
def predict_performance(request):
    """API endpoint: validate input via serializer, then predict."""
    serializer = PredictionSerializer(data=request.data)

    if not serializer.is_valid():
        return Response(
            {'errors': serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )

    try:
        prediction = _make_prediction(serializer.validated_data)

        return Response({
            'predicted_performance_index': prediction,
            'input_validated': True,
        })
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


def home(request):
    """Template view: form submission validated via the same serializer."""
    context = {}

    if request.method == 'POST':
        # Convert form checkbox to boolean for the serializer
        form_data = {
            'hours_studied': request.POST.get('hours_studied', 0),
            'previous_scores': request.POST.get('previous_scores', 0),
            'sleep_hours': request.POST.get('sleep_hours', 0),
            'sample_papers': request.POST.get('sample_papers', 0),
            'extracurricular': request.POST.get('extracurricular') == 'on',
        }

        serializer = PredictionSerializer(data=form_data)

        if not serializer.is_valid():
            # Flatten all error messages into a readable string for the template
            error_messages = []
            for field, messages in serializer.errors.items():
                label = field.replace('_', ' ').title() if field != 'non_field_errors' else ''
                for msg in messages:
                    if label:
                        error_messages.append(f"{label}: {msg}")
                    else:
                        error_messages.append(str(msg))

            context['error'] = ' | '.join(error_messages)
            # Keep form data so the user can correct it
            context.update(form_data)
        else:
            try:
                data = serializer.validated_data
                prediction = _make_prediction(data)

                # Save to database
                StudentPerformance.objects.create(
                    hours_studied=int(data['hours_studied']),
                    previous_scores=data['previous_scores'],
                    extracurricular=data['extracurricular'],
                    sleep_hours=int(data['sleep_hours']),
                    sample_papers=data['sample_papers'],
                    performance_index=prediction,
                )

                context['prediction'] = prediction
                context['hours_studied'] = data['hours_studied']
                context['previous_scores'] = data['previous_scores']
                context['sleep_hours'] = data['sleep_hours']
                context['sample_papers'] = data['sample_papers']
                context['extracurricular'] = data['extracurricular']
                context['validated'] = True

            except Exception as e:
                context['error'] = f"Prediction error: {str(e)}"

    return render(request, 'index.html', context)

