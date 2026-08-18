from rest_framework import generics, permissions, parsers
from .models import Listing, ListingPhoto
from .serializers import ListingSerializer, ListingPhotoSerializer


class ListingListCreateView(generics.ListCreateAPIView):
    serializer_class = ListingSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ['city', 'district', 'listing_type', 'property_type', 'is_active']

    def get_queryset(self):
        qs = Listing.objects.filter(is_active=True)
        city = self.request.query_params.get('city')
        if city:
            qs = qs.filter(city__iexact=city)
        budget_min = self.request.query_params.get('budget_min')
        budget_max = self.request.query_params.get('budget_max')
        if budget_min:
            qs = qs.filter(budget_max__gte=budget_min)
        if budget_max:
            qs = qs.filter(budget_min__lte=budget_max)
        return qs


class ListingDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ListingSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Listing.objects.all()

    def perform_destroy(self, instance):
        if instance.user == self.request.user:
            instance.delete()


class ListingPhotoUploadView(generics.CreateAPIView):
    serializer_class = ListingPhotoSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [parsers.MultiPartParser]

    def perform_create(self, serializer):
        listing = Listing.objects.get(pk=self.kwargs['listing_id'])
        serializer.save(listing=listing)
