from django.db.models import Sum, Count
from application.apps.accounts.models import BusinessProfile, ProfileDataCache, AgentDataCache
from application.apps.ads.models import Ad
from application.apps.deals.func import commission_level
from application.apps.deals.models import Deal


def update_profile_data():
    profiles = BusinessProfile.objects.all()
    profiles = profiles.select_related('profile_data_cache', 'agent_data_cache')
    profiles = profiles.annotate(agg_num_ads=Count('ad__pk'))

    for business_profile in profiles:
        need_save = False

        agent_data = None
        profile_data = business_profile.profile_data_cache
        if not profile_data:
            profile_data = ProfileDataCache()
            need_save = True

        deals = Deal.objects.filter(state='completed', ad__owner=business_profile).aggregate(
            agg_total_price_sold=Sum('price_eur'),
            agg_total_sold=Count('pk'),
        )

        num_bought_products = Deal.objects.filter(state='completed', owner=business_profile).count()

        # calculate commission
        level, perc = commission_level(deal_price_eur__sum=deals['agg_total_price_sold'] or 0)
        if profile_data.current_commission_perc != perc:
            profile_data.current_commission_perc = perc
            need_save = True

        #num ads
        if profile_data.num_ads != business_profile.agg_num_ads:
            profile_data.num_ads = business_profile.agg_num_ads or 0
            need_save = True

        # num views on all ads
        ads = Ad.objects.filter(active=True, owner=business_profile).aggregate(
            agg_num_views=Sum('num_views')
        )
        if profile_data.num_ads_views != ads['agg_num_views']:
            profile_data.num_ads_views = ads['agg_num_views'] or 0
            need_save = True

        if profile_data.num_bought_products != num_bought_products:
            profile_data.num_bought_products = num_bought_products or 0
            need_save = True

        # sold ads
        if profile_data.num_sold_products != deals['agg_total_sold']:
            profile_data.num_sold_products = deals['agg_total_sold'] or 0
            need_save = True

        if business_profile.is_agent:
            agent_data = business_profile.agent_data_cache
            if not agent_data:
                agent_data = AgentDataCache()
                need_save = True

            agent_deals = {
                'interested': Deal.objects.filter(state='interested', ad__owner__agent=business_profile).count(),
                'active': Deal.objects.filter(state='active', ad__owner__agent=business_profile).count(),
                'completed': Deal.objects.filter(state='completed', ad__owner__agent=business_profile).count(),
                'canceled': Deal.objects.filter(state='canceled', ad__owner__agent=business_profile).count(),
            }

            if agent_data.num_sold_products != agent_deals['completed']:
                agent_data.num_sold_products = agent_deals['completed']
                need_save = True

            if agent_data.num_interested != agent_deals['interested']:
                agent_data.num_interested = agent_deals['interested']
                need_save = True

            if agent_data.num_active != agent_deals['active']:
                agent_data.num_active = agent_deals['active']
                need_save = True

            if agent_data.num_completed != agent_deals['completed']:
                agent_data.num_completed = agent_deals['completed']
                need_save = True

            if agent_data.num_canceled != agent_deals['canceled']:
                agent_data.num_canceled = agent_deals['canceled']
                need_save = True

            num_recruited = BusinessProfile.objects.filter(agent=business_profile).count()
            if agent_data.num_recruited != num_recruited:
                agent_data.num_recruited = num_recruited
                need_save = True

        if need_save:
            if agent_data:
                agent_data.save()
                business_profile.agent_data_cache = agent_data

            if profile_data:
                profile_data.save()
                business_profile.profile_data_cache = profile_data

            business_profile.save()
