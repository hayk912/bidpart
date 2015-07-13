# coding=utf-8
from django.core.management.base import BaseCommand, CommandError
from application import settings
from application.apps.accounts.models import UserProfile, BusinessProfile, OldPassword
from application.apps.files.models import Image, File
from django.core.files import File as CoreFile
from application.apps.ads.models import Ad, ProductType, ProductCategory, BusinessDomain, Field, Value, FieldChoice, AdImage, AdFile
from application.apps.deals.models import Deal
from django.contrib.auth.models import User
from django.db.utils import IntegrityError
from optparse import make_option
from currencies.models import Currency
from phpserialize import serialize, unserialize
import csv
import time
import os
import pytz
import datetime
import shutil
from pprint import pprint
from application.settings import DATABASES
database = 'default'
sep = '\t'
ext = 'tsv'

# todo: remove memberlevel.

class Command(BaseCommand):
    args = '<...>'
    help = 'Takes a directory of csv files and imports to new bidpart'
    option_list = BaseCommand.option_list + (
        make_option('--type',
            action='store',
            dest='import_type',
            default=False,
            help='Specify a import type'),
        ) + (
        make_option('--path',
            action='store',
            dest='path',
            default=False,
            help='Specify a path to csv-files'),
        ) + (
        make_option('--use-empty',
            action='store',
            dest='empty_db',
            default=False,
            help='Specify if to copy empty db'),
        ) + (
        make_option('--database',
            action='store',
            dest='database',
            default=False,
            help='Specify a db'),
        )

    def handle(self, *args, **options):
        global database
        if options['database']:
            database = options['database']

        if int(options['empty_db']) == 1:
            shutil.copy2(DATABASES['empty']['NAME'], DATABASES[database]['NAME'])

        if not options['import_type'] or not options['path']:
            raise CommandError('--type and --path are required')
        path = options['path']
        upload_path = os.path.join(path, 'uploads')
        import_type = options['import_type']

        if not os.path.exists(path):
            raise CommandError('%s does not exist' % path)

        required_files = ['users', 'ads', 'ads_categories', 'product_categories', 'products', 'product_subcategories', 'products_subcategories', 'product_fields', 'products_fields', 'ads_values', 'ads_uploads', 'ads_uploads', 'deals']
        for f in required_files:
            try:
                open(path + f + '.' + ext, 'rb')
            except IOError as e:
                raise CommandError('%s.%s was not found. (%s)' % (f, ext, e))

        start = time.time()

        """ Users """
        if import_type == 'users':
            import_simple_data()
            filename = path + 'users.' + ext
            mapping = [
                ('id', 'id', User),
                ('un', 'username', User),
                ('pw', 'old_password', OldPassword),
                ('nonce', 'old_nonce', OldPassword),
                ('last_activity', False, False),
                ('first_name', 'first_name', User),
                ('last_name', 'last_name', User),
                ('email', 'email', User),
                ('phone', 'phone', UserProfile),
                ('cellphone', 'mobile', UserProfile),
                ('company_name', 'business_name', BusinessProfile),
                ('company_description', 'business_description', BusinessProfile),
                ('city', 'address_city', BusinessProfile),
                ('zipcode', 'address_zipcode', BusinessProfile),
                ('street', 'address', BusinessProfile),
                ('forgot_hash', False, False),
                ('forgot_time', False, False),
                #('level_id', 'member_level', BusinessProfile),
                #('level_promoted_timestamp', 'member_level_promoted', BusinessProfile),
                ('moderator', False, False),
                ('created', 'date_joined', User),
                ('avatar_160', False, False),  # image
                ('avatar_240', 'avatar', UserProfile),
                ('logo_160', False, False),
                ('logo_240', 'logo', BusinessProfile),
                ('imported', False, False),
                ('pw_pain', False, False),
                ('gps_lat', False, False),
                ('gps_lon', False, False),
                ('admin_id', False, False),
            ]
            f = open(filename, 'rb',)
            OldPassword.objects.using(database).delete()
            reader = csv.reader(f, delimiter=sep)
            header = []
            failed = []
            num = -1
            try:
                for row in reader:
                    num += 1
                    if num == 0:
                        for field in row:
                            header.append(field)
                        print header
                        continue

                    user = User()

                    user.password = "pbkdf2_sha256$10000$0$0="
                    user_profile = UserProfile()
                    old_password = OldPassword()

                    business_profile = False

                    for i in range(len(header)):
                        for old_field, new_field, model in mapping:
                            if new_field and model and old_field == header[i]:
                                row[i] = row[i].decode('utf-8')
                                #print "%s\t->\t%s\t(%s): %s - %s" % (old_field, new_field, model, i, row[i])

                                if model == User:
                                    if new_field == 'date_joined':
                                        row[i] = ts_to_datetime(row[i])
                                    elif new_field == 'email':
                                        setattr(user, 'username', row[i])
                                    setattr(user, new_field, row[i])
                                elif model == UserProfile:
                                    if new_field == 'phone' and row[i] != 'NULL':
                                        setattr(user_profile, 'cellphone', row[9])
                                    if new_field == 'avatar' and row[i] != 'NULL':
                                        row[i] = save_image(os.path.join(upload_path, 'avatars/' + row[0], row[i]), 'Avatar for %s %s' % (row[5], row[6]))
                                    elif new_field == 'avatar':
                                        row[i] = None
                                    if row[i] != 'NULL' and row[i]:
                                        setattr(user_profile, new_field, row[i])
                                elif model == BusinessProfile:
                                    if new_field == 'business_name':
                                        business_profile = BusinessProfile.objects.using(database).get_or_create(business_name=row[i])[0]
                                        business_profile.business_name = row[i]
                                        user_profile.active_profile = business_profile
                                    elif business_profile:
                                        if new_field == 'logo' and row[i] != 'NULL':
                                            row[i] = save_image(os.path.join(upload_path, 'logos/' + row[0], row[i]), 'Logo for ' + business_profile.business_name)
                                        elif new_field == 'logo':
                                            row[i] = None
                                        #elif new_field == 'member_level':
                                        #    row[i] = MemberLevel.objects.using(database).get(id=row[i])
                                        #elif new_field == 'member_level_promoted':
                                        #    row[i] = ts_to_datetime(row[i])
                                        setattr(business_profile, new_field, row[i])
                                elif model == OldPassword:
                                    setattr(old_password, new_field, row[i])
                                break
                    try:
                        user.save(using=database)
                    except IntegrityError:
                        print "error2 " + str(row[0])
                        failed.append(row)
                        continue
                    # Snatch the signal created profile and convert it!
                    try:
                        created_user_profile = user.get_userprofile()
                    except:
                        created_user_profile = user_profile
                    user_profile.user = user
                    user_profile.id = created_user_profile.id

                    created_user_profile = user_profile
                    created_user_profile.save(using=database)
                    if created_user_profile.avatar:
                        created_user_profile.avatar.creator = user
                        created_user_profile.avatar.save(using=database)

                    old_password.user = user
                    old_password.save(using=database)
                    if business_profile:
                        user_profile.business_profiles.add(business_profile)
                        if not business_profile.creator:
                            business_profile.creator = user_profile
                        if business_profile.logo:
                            if not business_profile.logo.creator:
                                business_profile.logo.creator = user
                                business_profile.logo.save()
                        business_profile.save(using=database)
                    print user

                    if num % 100 == 0:
                        timediff = time.time() - start
                        print "Rows: %s, %s" % (num, num / timediff)
            except csv.Error, e:
                exit('file %s, line %d: %s' % (filename, reader.line_num, e))

            print "%s Users" % (num, )

            print "%s failed" % len(failed)
            if failed:
                for row in failed:
                    u = User.objects.using(database).get(email=row[7])
                    print " - %s: %s %s %s (DUPLICATE: %s, %s)" % (row[0], row[5], row[6], row[7], u.id, u.email)

        elif import_type == 'producttypes':

            """ BusinessDomain """

            filename = path + 'product_categories.' + ext
            f = open(filename, 'rb')
            reader = csv.reader(f, delimiter=sep)
            num = -1
            try:
                for row in reader:
                    num += 1
                    if num == 0:
                        continue
                    c_id, category = row
                    BusinessDomain.objects.using(database).get_or_create(id=c_id, title=category)
            except csv.Error, e:
                exit('file %s, line %d: %s' % (filename, reader.line_num, e))

            print "%s BusinessDomains" % (num, )

            """ ProductCategory """

            filename = path + 'product_subcategories.' + ext
            f = open(filename, 'rb')
            reader = csv.reader(f, delimiter=sep)
            num2 = -1
            try:
                for row in reader:
                    num2 += 1
                    if num2 == 0:
                        continue
                    c_id, category, _ = row
                    ProductCategory.objects.using(database).get_or_create(id=c_id, title=category)
            except csv.Error, e:
                exit('file %s, line %d: %s' % (filename, reader.line_num, e))
            num += num2

            print "%s ProductCategories" % (num2, )

            """ ProductType """

            filename = path + 'products.' + ext
            f = open(filename, 'rb')
            reader = csv.reader(f, delimiter=sep)
            num2 = -1
            try:
                for row in reader:
                    num2 += 1
                    if num2 == 0:
                        continue
                    c_id, category, _ = row
                    ProductType.objects.using(database).get_or_create(id=c_id, title=category)
            except csv.Error, e:
                exit('file %s, line %d: %s' % (filename, reader.line_num, e))
            num += num2

            print "%s ProductTypes" % (num2, )

            """ ProductType Categories """

            filename = path + 'products_subcategories.' + ext
            f = open(filename, 'rb')
            reader = csv.reader(f, delimiter=sep)
            num2 = -1
            try:
                for row in reader:
                    num2 += 1
                    if num2 == 0:
                        continue
                    pcs_id, category_id, subcategory_id = row
                    pt = ProductType.objects.using(database).get(id=category_id)
                    pc = ProductCategory.objects.using(database).get(id=subcategory_id)
                    pt.product_categories.add(pc)
                    pt.save()
            except csv.Error, e:
                exit('file %s, line %d: %s' % (filename, reader.line_num, e))
            num += num2

            print "%s ProductType Categories" % (num2, )

            """ Fields """

            filename = path + 'product_fields.' + ext
            f = open(filename, 'rb')
            reader = csv.reader(f, delimiter=sep)
            num2 = -1
            try:
                for row in reader:
                    num2 += 1
                    if num2 == 0:
                        continue
                    if len(row) < 15:
                        print '[ERROR] Invalid row: #%s' % num2
                        continue
                    for i in range(len(row)):
                        if row[i] == 'NULL':
                            row[i] = None
                    #print row
                    f_id, work_name, name, description, ftype, options, public, admin, searchable, required, alpha, is_natural, min_length, max_length, imported_id = row
                    if is_natural:
                        is_natural = int(is_natural)

                    if options:
                        options = options.replace('\\"', '"').replace('""', '"').replace('\\', '"', 2)[:-1]  # Clean up csv molested serialize-data

                    f, new = Field.objects.using(database).get_or_create(id=f_id)
                    f.required = required
                    f.help_text = description
                    if is_natural:
                        f.type = 'IntegerField'
                    elif description:
                        f.type = 'CharField'
                    elif ftype == 'dropdown' and options:
                        f.type = 'ChoiceField'
                        try:
                            options = unserialize(options)
                        except ValueError as e:
                            print '[ERROR] unserialize error: %s' % e
                        else:
                            print options.items()
                            f.save()
                            for k, v in options.items():
                                if v in ['Ja', 'Nej']:
                                    f.type = 'BooleanField'
                                    print '- Made boolean'
                                    break
                                else:
                                    FieldChoice.objects.using(database).get_or_create(name=v, field=f)
                    else:
                        f.type = 'CharField'
                    if name:
                        f.label = name
                    if work_name:
                        f.name = work_name
                    f.save()

            except csv.Error, e:
                exit('file %s, line %d: %s' % (filename, reader.line_num, e))
            num += num2

            print "%s Fields" % (num2, )

            """ Fields ProductType """

            filename = path + 'products_fields.' + ext
            f = open(filename, 'rb')
            reader = csv.reader(f, delimiter=sep)
            num2 = -1
            try:
                for row in reader:
                    num2 += 1
                    if num2 == 0:
                        continue
                    for i in range(len(row)):
                        if row[i] == 'NULL':
                            row[i] = None

                    ptf_id, pt_id, f_id = row

                    pt = ProductType.objects.using(database).get(id=pt_id)
                    f = Field.objects.using(database).get(id=f_id)

                    pt.fields.add(f)
                    pt.save()

            except csv.Error, e:
                exit('file %s, line %d: %s' % (filename, reader.line_num, e))
            num += num2

            print "%s Fields ProductType" % (num2, )

        elif import_type == 'ads':

            """ Ads """

            Ad.objects.using(database).all().delete()
            sek_currency = Currency.objects.using(database).get(code='SEK')
            filename = path + 'ads.' + ext
            failed = []
            f = open(filename, 'rb')
            reader = csv.reader(f, delimiter=sep)
            num = 0
            num2 = -1
            try:
                for row in reader:
                    num2 += 1
                    if num2 == 0:
                        continue

                    for i in range(len(row)):
                        row[i] = row[i].decode('utf-8')
                        if row[i] == 'NULL':
                            row[i] = None
                    if len(row) < 18 or not row[10]:
                        print "[ERROR] Invalid data! row " + str(num2)
                        if len(row):
                            failed.append(row[0])
                        num2 -= 1
                        continue
                    #member_level = MemberLevel.objects.using(database).get(id=row[14])
                    try:
                        user = User.objects.using(database).get(id=row[1])
                    except:
                        print "FAILED user: " + row[1]
                        failed.append(row[0])
                    user_profile = user.get_userprofile()
                    active_business_profile = user_profile.active_profile
                    product_type = ProductType.objects.using(database).get(id=row[2])
                    ad = Ad(
                        id=row[0],
                        creator=user_profile,
                        owner=active_business_profile,
                        product_type=product_type,
                        title=row[3],
                        description=row[4] or 'Ingen beskrivning',
                        price=float(row[5]),
                        updated=ts_to_datetime(row[10]),
                        created=ts_to_datetime(row[11]),
                        active=row[12],
                        published=row[12],  # col: created
                        #member_level=member_level,
                        youtube_code=row[16],
                        amount=row[18],
                        currency=sek_currency,
                        is_request=False,
                    )
                    ad.save(using=database)
                    Ad.objects.using(database).filter(id=row[0]).update(
                        updated=ts_to_datetime(row[10]),
                        created=ts_to_datetime(row[11]),
                        )
            except csv.Error, e:
                exit('file %s, line %d: %s' % (filename, reader.line_num, e))
            num += num2

            print "%s Ads" % (num2, )

            """ Field Ad: Value """

            Value.objects.using(database).all().delete()

            filename = path + 'ads_values.' + ext
            f = open(filename, 'rb')
            reader = csv.reader(f, delimiter=sep)
            num2 = -1
            try:
                for row in reader:
                    num2 += 1
                    if num2 == 0:
                        continue
                    for i in range(len(row)):
                        if row[i] == 'NULL':
                            row[i] = row[i].decode('utf-8')
                            row[i] = None

                    adf_id, ad_id, ptf_id, value = row
                    value = value or ""
                    if value in ['Ja', 'Nej']:
                        if value == 'Ja':
                            value = 1
                        else:
                            value = 0
                    try:
                        Ad.objects.using(database).get(id=ad_id)
                    except Ad.DoesNotExist:
                        print "[ERROR] Ad does not exist id:%s" % ad_id
                        continue
                    v, new = Value.objects.using(database).get_or_create(id=adf_id, field_id=ptf_id, ad_id=ad_id, value=value or "")

            except csv.Error, e:
                exit('file %s, line %d: %s' % (filename, reader.line_num, e))
            num += num2

            print "%s Field Ad: Value" % num2

            filename = path + 'ads_categories.' + ext
            f = open(filename, 'rb')
            reader = csv.reader(f, delimiter=sep)
            num2 = -1
            try:
                for row in reader:
                    num2 += 1
                    if num2 == 0:
                        continue

                    ac_id, ad_id, category_id = row
                    #print row
                    try:
                        ad = Ad.objects.using(database).get(id=ad_id)
                    except:
                        print "[ERROR] Unknown ad_id: %s" % ad_id
                        num2 -= 1
                    business_domain = BusinessDomain.objects.using(database).get(id=category_id)
                    ad.business_domains.add(business_domain)
                    ad.save(using=database)

            except csv.Error, e:
                exit('file %s, line %d: %s' % (filename, reader.line_num, e))
            num += num2

            print "%s Ads BusinessDomains" % (num2, )

            print "The following ads failed to import: "
            print failed

        elif import_type == 'common':
            import_simple_data()
            num = 1

        elif import_type == 'uploads':
            """ Uploads """

            files = []
            filename = path + 'uploads.' + ext
            f = open(filename, 'rb')
            reader = csv.reader(f, delimiter=sep)
            num = 0
            num2 = -1
            try:
                for row in reader:
                    num2 += 1
                    if num2 == 0:
                        continue

                    u_id, mime, u_path, thumb160, thumb240 = row

                    files.append((u_id, mime, u_path, ))

            except csv.Error, e:
                exit('file %s, line %d: %s' % (filename, reader.line_num, e))

            filename = path + 'ads_uploads.' + ext
            f = open(filename, 'rb')
            reader = csv.reader(f, delimiter=sep)
            num2 = -1
            try:
                for row in reader:
                    num2 += 1
                    if num2 == 0:
                        continue

                    au_id, ad_id, u_id, name = row

                    #print row
                    try:
                        ad = Ad.objects.using(database).get(id=ad_id)
                    except:
                        print '[ERROR] Invalid ad_id: %s' % ad_id
                        continue

                    for f_u_id, mime, u_path in files:

                        if f_u_id == u_id:

                            if name.find('image') > -1:
                                im = save_image(os.path.join(upload_path, u_path), 'Bild for ' + ad.get_localized('title', settings.LANGUAGE_CODE), ad)
                                #if im:
                                #    ai, n = AdImage.objects.using(database).get_or_create(ad=ad, image=im)
                            elif name == 'documentation':
                                f = save_file(os.path.join(upload_path, u_path), 'Dokumentation for ' + ad.get_localized('title', settings.LANGUAGE_CODE), ad)
                                #if f:
                                #    AdFile.objects.using(database).get_or_create(ad=ad, file=f)
                            else:
                                raise Exception('dafuq?')

                            ad.save()
            except csv.Error, e:
                exit('file %s, line %d: %s' % (filename, reader.line_num, e))
            num += num2

            print "%s Uploads" % (num2, )

        elif import_type == 'deals':

            """ Deals """

            Deal.objects.using(database).all().delete()
            sek_currency = Currency.objects.using(database).get(code='SEK')
            filename = path + 'deals.' + ext
            failed = []
            f = open(filename, 'rb')
            reader = csv.reader(f, delimiter=sep)
            num = 0
            num2 = -1
            try:
                for row in reader:
                    num2 += 1
                    if num2 == 0:
                        continue

                    for i in range(len(row)):
                        #row[i] = row[i]
                        if row[i] == 'NULL':
                            row[i] = None
                    if len(row) < 16:
                        print "[ERROR] Invalid data! row " + str(num2)
                        if len(row):
                            failed.append(row[0])
                        num2 -= 1
                        continue
                    d_id, ad_id, user_id, status, read, created, updated, last_reminder, manual_processing, commission, end_price, reason, amount, bid, is_payed_to_agent, agent_commission = row

                    try:
                        user = User.objects.using(database).get(id=user_id)
                    except:
                        print "[ERROR] Invalid user: %s" % user_id
                        continue

                    user_profile = user.get_userprofile()
                    business_profile = BusinessProfile.objects.using(database).get(id=user_profile.active_profile_id)

                    try:
                        ad = Ad.objects.using(database).get(id=ad_id)
                    except:
                        print "[ERROR] Invalid ad: %s" % ad_id
                        continue

                    d = Deal()
                    d.creator = user_profile
                    d.owner = business_profile
                    d.ad = ad

                    if status == 'done':
                        status = 'completed'
                    elif status == 'aborted':
                        status = 'canceled'

                    d.state = status

                    d.created = ts_to_datetime(created)
                    d.updated = ts_to_datetime(updated)

                    d.last_reminder = ts_to_datetime(last_reminder)
                    d.manual_processing = int(manual_processing)
                    d.commission = commission
                    d.payed_to_agent = int(is_payed_to_agent)
                    d.agent_commission = agent_commission
                    d.cancel_reason = reason

                    d.price = end_price
                    if not bid:
                        bid = 0.00
                    d.bid = bid
                    if not amount:
                        amount = 0
                    d.amount = amount
                    #d.currency = sek_currency
                    #d.commission_currency = sek_currency
                    #d.agent_currency = sek_currency
                    try:
                        d.save(using=database)
                    except IntegrityError:
                        dd = Deal.objects.get(owner=business_profile, ad=ad)
                        print "[ERROR] Unique conflict: Owner: %s for ad: %s" % (dd.owner, ad.pk)

            except csv.Error, e:
                exit('file %s, line %d: %s' % (filename, reader.line_num, e))

            print "%s Deals" % (num2, )
            num += num2

        elif import_type == 'test':
            print ts_to_datetime(1337766315)
            num = 0
        else:
            raise CommandError('Invalid import type. :/')

        self.stdout.write('\nSuccessfully imported %1s rows from task "%0s" in %3f secs! \n' % (num, import_type, time.time() - start, ))


def save_image(filename, title, ad=None):
    #print filename + " " + title
    if ad is None:
        im = Image()
    else:
        im = AdImage()
        im.ad = ad
    im.title = title
    im.description = title
    im.description_short = title
    im.save()
    try:
        im.image_filename.save(
            os.path.basename(filename),
            CoreFile(open(filename, 'rb')),
            save=False
        )
        im.save(using=database)
        return im
    except Exception as e:
        print e
        return None


def save_file(filename, title, ad):
    print filename + " " + title
    f = AdFile()
    f.title = title
    f.description = title
    f.description_short = title
    f.ad = ad
    f.save()
    try:
        f.filename.save(
            os.path.basename(filename),
            CoreFile(open(filename, 'rb')),
            save=False
        )
        f.save(using=database)
        return f
    except Exception as e:
        print e
        return None


def ts_to_datetime(timestamp):
    timestamp = datetime.datetime.fromtimestamp(int(timestamp))
    utc = pytz.timezone('UTC')
    return timestamp.replace(tzinfo=utc)


def import_simple_data():
#    member_levels = (
#        (1, 'Brons'),
#        (2, 'Silver'),
#        (3, 'Guld'),
#        (4, 'Diamant'),
#    )
#    for i, t in member_levels:
#        ml, new = MemberLevel.objects.using(database).get_or_create(id=i, title=t)
#        if new:
#            ml.save()

    c, new = Currency.objects.using(database).get_or_create(code='SEK')
    if new:
        c.name = 'Svensk krona'
        c.factor = 1
        c.is_active = 1
        c.is_default = 1
        c.save()
