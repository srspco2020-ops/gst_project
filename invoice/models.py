from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


class CustomUserManager(BaseUserManager):
    def create_user(self, mobile, password=None, **extra_fields):
        if not mobile:
            raise ValueError('The Mobile number is required')
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)

        user = self.model(mobile=mobile, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, mobile, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(mobile, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    mobile = models.CharField(max_length=15, unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'mobile'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.mobile


class Trader(models.Model):
    #s_no = models.CharField(primary_key=True)
    gstin = models.CharField(max_length=15, db_column='GSTIN',primary_key=True)
    trader_name = models.CharField(max_length=255, db_column='Trader Name')
    legal_name = models.CharField(max_length=255, db_column='Legal Name')
    group = models.CharField(max_length=100, db_column='Group')
    contact_person_name = models.CharField(max_length=255, db_column='Contact Person Name')
    mo = models.CharField(max_length=15, db_column='Mo')

    class Meta:
        db_table = 'list'



class OnlyPInv(models.Model):
    my_gstin = models.CharField(max_length=15, db_column='My GSTIN')  # Add this field for filtering
    supplier_gstin = models.CharField(max_length=15, db_column='Supplier GSTIN', primary_key=True)
    supplier_trade_name = models.CharField(max_length=255, db_column='Supplier Trade Name')
    document_number = models.CharField(max_length=50, db_column='Document Number')
    document_date = models.DateField(db_column='Document Date')
    total_taxable_value = models.DecimalField(max_digits=12, decimal_places=2, db_column='Total Taxable Value')
    igst_amount = models.DecimalField(max_digits=12, decimal_places=2, db_column='IGST Amount')
    cs_gst_amount = models.DecimalField(max_digits=12, decimal_places=2, db_column='CS_GST_Amount')

    class Meta: 
        managed = False
        db_table = 'only_p_inv'


class OnlyBInv(models.Model):
    my_gstin = models.CharField(max_length=15, db_column='My GSTIN')  # Required for filtering
    gstin_of_supplier = models.CharField(max_length=15, db_column='GSTIN of Supplier', primary_key=True)
    supplier_trade_name = models.CharField(max_length=255, db_column='Supplier Trade Name')
    invoice_number = models.CharField(max_length=50, db_column='Invoice Number')
    invoice_date = models.DateField(db_column='Invoice date')
    taxable_value = models.DecimalField(max_digits=12, decimal_places=2, db_column='Taxable Value')
    integrated_tax_paid = models.DecimalField(max_digits=12, decimal_places=2, db_column='Integrated Tax Paid')
    centralstate_tax_paid = models.DecimalField(max_digits=12, decimal_places=2, db_column='CentralState_Tax_Paid')

    class Meta:
        managed = False
        db_table = 'only_b_inv'

class OnlyPCn(models.Model):
    my_gstin = models.CharField(max_length=15, db_column='My GSTIN')  # Add this field for filtering
    supplier_gstin = models.CharField(max_length=15, db_column='Supplier GSTIN', primary_key=True)
    supplier_trade_name = models.CharField(max_length=255, db_column='Supplier Trade Name')
    document_number = models.CharField(max_length=50, db_column='Document Number')
    document_date = models.DateField(db_column='Document Date')
    total_taxable_value = models.DecimalField(max_digits=12, decimal_places=2, db_column='Total Taxable Value')
    igst_amount = models.DecimalField(max_digits=12, decimal_places=2, db_column='IGST Amount')
    cs_gst_amount = models.DecimalField(max_digits=12, decimal_places=2, db_column='CS_GST_Amount')

    class Meta: 
        managed = False
        db_table = 'only_p_cn'


class OnlyBCn(models.Model):
    my_gstin = models.CharField(max_length=15, db_column='My GSTIN')  # Required for filtering
    gstin_of_supplier = models.CharField(max_length=15, db_column='GSTIN of Supplier', primary_key=True)
    supplier_trade_name = models.CharField(max_length=255, db_column='Supplier Trade Name')
    invoice_number = models.CharField(max_length=50, db_column='Note/Refund Voucher Number')
    invoice_date = models.DateField(db_column='Note/Refund Voucher date')
    taxable_value = models.DecimalField(max_digits=12, decimal_places=2, db_column='Taxable Value')
    integrated_tax_paid = models.DecimalField(max_digits=12, decimal_places=2, db_column='Integrated Tax Paid')
    centralstate_tax_paid = models.DecimalField(max_digits=12, decimal_places=2, db_column='CentralState_Tax_Paid')

    class Meta:
        managed = False
        db_table = 'only_b_cn'


class OnlyPDn(models.Model):
    my_gstin = models.CharField(max_length=15, db_column='My GSTIN')  # Add this field for filtering
    supplier_gstin = models.CharField(max_length=15, db_column='Supplier GSTIN', primary_key=True)
    supplier_trade_name = models.CharField(max_length=255, db_column='Supplier Trade Name')
    document_number = models.CharField(max_length=50, db_column='Document Number')
    document_date = models.DateField(db_column='Document Date')
    total_taxable_value = models.DecimalField(max_digits=12, decimal_places=2, db_column='Total Taxable Value')
    igst_amount = models.DecimalField(max_digits=12, decimal_places=2, db_column='IGST Amount')
    cs_gst_amount = models.DecimalField(max_digits=12, decimal_places=2, db_column='CS_GST_Amount')

    class Meta: 
        managed = False
        db_table = 'only_p_dn'


class OnlyBDn(models.Model):
    my_gstin = models.CharField(max_length=15, db_column='My GSTIN')  # Required for filtering
    gstin_of_supplier = models.CharField(max_length=15, db_column='GSTIN of Supplier', primary_key=True)
    supplier_trade_name = models.CharField(max_length=255, db_column='Supplier Trade Name')
    invoice_number = models.CharField(max_length=50, db_column='Note/Refund Voucher Number')
    invoice_date = models.DateField(db_column='Note/Refund Voucher date')
    taxable_value = models.DecimalField(max_digits=12, decimal_places=2, db_column='Taxable Value')
    integrated_tax_paid = models.DecimalField(max_digits=12, decimal_places=2, db_column='Integrated Tax Paid')
    centralstate_tax_paid = models.DecimalField(max_digits=12, decimal_places=2, db_column='CentralState_Tax_Paid')

    class Meta:
        managed = False
        db_table = 'only_b_dn'