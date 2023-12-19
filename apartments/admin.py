
from django.contrib import admin
from .models import *
from .forms import * 
from .utils import *
  

class ApartmentImagesAdmin(admin.StackedInline):
    extra = 1
    model = ApartmentImage
    list_display = [
        "id",
    ]
    list_display_links = ["id"]
    formfield_overrides = {models.ImageField: {'widget': AdminImageWidget}}

# class ApartmentCleaningAdmin(admin.StackedInline):
#     extra = 1
#     model = ApartmentCleaningExpense
#     list_display = [
#         "id",
#     ]
#     list_display_links = ["id"]
#     formfield_overrides = {models.ImageField: {'widget': AdminImageWidget}}

class ApartmentMaintenanceAdmin(admin.StackedInline):
    extra = 1
    model = ApartmentMaintenance
    list_display = [
        "id",
    ]
    list_display_links = ["id"]
    formfield_overrides = {models.ImageField: {'widget': AdminImageWidget}}

class ApartmentAddressAdmin(admin.StackedInline):
    extra = 1
    max_num = 1
    min_num = 1
    can_delete = False
    model = ApartmentAddress
    list_display_links = ["id"]
    form = ApartmentAddressForm



    # def clean(self):
    #     print(here)
    #     cleaned_data = super().clean()
    #     postcode = cleaned_data.get("postcode")
    #     if not validation.is_valid_postcode(postcode):
    #         raise forms.ValidationError("field1 and field2 should not be the same")
            
class ApartmentAdmin(admin.ModelAdmin):

    list_display = [
        "id",
        "title",
        "price",
        "category",
    ]
    
    list_display_links = ["title"]
    inlines  = [ApartmentImagesAdmin,ApartmentAddressAdmin,ApartmentCleaningAdmin,ApartmentMaintenanceAdmin]

    formfield_overrides = {models.ImageField: {'widget': AdminImageWidget}}
    
    
    def save_formset(self, request, form, formset, change):
        for form in formset:
            if form.cleaned_data.get('name') == 'invalid':
                form.add_error('name', 'Invalid name')
        if formset.is_valid():
            formset.save()
        else:
            print('not done ')
                    
                    
    def get_form(self, request, obj=None, **kwargs):
        form = super(ApartmentAdmin, self).get_form(request, obj, **kwargs)
        owner,_ = ApartmentOwner.objects.get_or_create(
            full_name="Capital Apartment",
            phone_number="07878919878",
            payment_options='Direct',
            # address='test',
            ownership_details='test')
        
        form.base_fields['owner'].initial = owner.id
        return form

class  ApartmentCleaningAdmin(admin.StackedInline):
    extra = 1
    model = ApartmentCleaningExpense
    list_display = [
        "id",
    ]
    list_display_links = ["id"]
    formfield_overrides = {models.ImageField: {'widget': AdminImageWidget}}

class ApartmentEarningTransactionAdmin(admin.StackedInline):
    extra = 1
    model = ApartmentEarningTransaction
    list_display = [
        "id",
    ]
    list_display_links = ["id"]
    formfield_overrides = {models.ImageField: {'widget': AdminImageWidget}}

class ApartmentEarningAdmin(admin.ModelAdmin):

    list_display = [
        "id",
        "cleaning_expenses",
        "total_earnings",
        "turnover",
        "apartment",
        "created_at",
    ]
    
    list_display_links = ["id"]

    inlines  = [ApartmentEarningTransactionAdmin]

class BookingAdmin(admin.ModelAdmin):
    
    list_display = [
        "id",
        "apartment",
        "phone",
        "guest",
        "check_in_date",
        "check_in_time",
        "created_at",
    ]

class ApartmentOwnerAddressAdmin(admin.StackedInline):
    extra = 1
    max_num = 1
    model = ApartmentOwnerAddress
    list_display_links = ["id"]

class ApartmentOwnerAdmin(admin.ModelAdmin):

    list_display = [
        "id",
        "full_name",
        "phone_number",
        "created_at",
        "updated_at",
    ]
    list_display_links = ["id"]

    inlines  = [ApartmentOwnerAddressAdmin]




admin.site.register(ApartmentCleaner)    
admin.site.register(Booking,BookingAdmin)
admin.site.register(ApartmentCategory)
admin.site.register(ApartmentOwner,ApartmentOwnerAdmin)


admin.site.register(Apartment,ApartmentAdmin)
admin.site.register(ApartmentEarning,ApartmentEarningAdmin)
admin.site.register(ApartmentCleaningExpense)


admin.site.register(ApartmentAddress)
admin.site.register(ApartmentOwnerAddress)
admin.site.register(ApartmentEarningTransaction)    


