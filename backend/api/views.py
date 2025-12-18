from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.core.files.storage import default_storage
import cv2
import os


@api_view(['POST'])
def process_image(request):
    """
    Process an image with filters, classification, and object detection.
    
    Expected request data:
    - image: Image file
    - filter: Filter name (default: grayscale)
    """
    try:
        # Lazy import ML modules to allow server startup even if dependencies are missing
        from .ml.filters import apply_filter
        from .ml.classification import classify_image
        from .ml.detection import detect_objects
        
        # Get the uploaded image
        if 'image' not in request.FILES:
            return Response(
                {'error': 'No image file provided'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        image_file = request.FILES['image']
        filter_name = request.data.get('filter', 'grayscale')
        
        # Save the uploaded image
        path = default_storage.save(image_file.name, image_file)
        full_path = default_storage.path(path)
        
        # Read the image
        img = cv2.imread(full_path)
        if img is None:
            return Response(
                {'error': 'Could not read image file'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Apply filter
        filtered_img = apply_filter(img, filter_name)
        cv2.imwrite(full_path, filtered_img)
        
        # Classify image
        classification_result = classify_image(full_path)
        
        # Detect objects
        detected_image_path, detections = detect_objects(full_path)
        
        # Build response
        response_data = {
            'success': True,
            'image': path,
            'filter_applied': filter_name,
            'classification': classification_result,
            'objects': detections,
        }
        
        if detected_image_path:
            response_data['detected_image'] = detected_image_path.replace(
                str(default_storage.location), ''
            ).lstrip('/')
        
        return Response(response_data)
    
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

