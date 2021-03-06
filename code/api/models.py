from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from api.validators import validate_car
from django.utils.translation import gettext_lazy as _


class Car(models.Model):
    """Car model that holds a make and model.
    Validates and replaces `make` and `model` fields
    using :validators:`api.validate_car`
    """
    make = models.CharField(_("Car make name"), max_length=64)
    model = models.CharField(_("Model name"), max_length=64)

    class Meta:
        unique_together = ('make', 'model')

    def __str__(self):
        return "{0} {1}".format(self.make, self.model)

    def average_rating(self):
        """
        Return average rating based on :models:`Review`.
        """
        total_rating = 0
        reviews = self.reviews.all()
        for review in reviews:
            total_rating += review.review
        return total_rating / reviews.count()


    def number_of_reviews(self):
        """
        Return number of corresponding :models:`Review`.
        """
        return self.reviews.count()

    @staticmethod
    def most_popular(n=5):
        """Return most popular cars based on number of
        ratings.

        Key arguments:

        n(int) -- number of cars returned, default 5
        """
    cars = Car.objects.all()
    cars_sorted = sorted(cars, key=lambda car: car.reviews.count())
    return cars_sorted[:n]

    def clean(self):
        return validate_car(self.make, self.model)

    def save(self, *args, **kwargs):
        new_make, new_model = self.clean()
        self.make = new_make
        self.model = new_model
        super(Car, self).save(*args, **kwargs)


class Review(models.Model):
    """Review model for :models:`api.Car`.
      Validates `review` to check if value is between 1 and 5.
    """
    car = models.ForeignKey(Car,
                            on_delete=models.CASCADE,
                            related_name="reviews")
    review = models.IntegerField(_("Rating from 1 to 5"),
                                 validators=[
                                     MinValueValidator(1),
                                     MaxValueValidator(5)
                                 ]
                                 )

    @staticmethod
    def reviews_per_car():
        