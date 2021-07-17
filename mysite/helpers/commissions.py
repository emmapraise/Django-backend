from webapp.models import RealtorType


def calculate_commissions(amount_paid, client):
    upline = client.upline
    if client.upline is not None:
        payment_candidates = list()
        percentage_left = 30
        bp_count = 0
        p_count = 0
        ap_added = False
        ep_added = False
        while percentage_left > 5:
            last_candidate = payment_candidates[-1][0]

            if upline.realtor_type.name == RealtorType.REFERRAL:
                percentage_commission = 0
            elif upline.realtor_type > last_candidate.realtor_type:
                percentage_commission = upline.realtor_type.percentage_commission
            elif upline.realtor_type == last_candidate.realtor_type:
                percentage_commission = upline.realtor_type.percentage_commission / 2
            else:
                percentage_commission = 0

            if percentage_commission != 0:
                if upline.realtor_type.name == RealtorType.BUSINESS_PARTNER:
                    if bp_count >= 2:
                        percentage_commission = 0
                    elif len(payment_candidates) == 0:
                        percentage_commission = upline.realtor_type.percentage_commission
                    else:
                        percentage_commission = upline.realtor_type.percentage_commission / 2
                    bp_count += 1
                elif upline.realtor_type.name == RealtorType.PARTNER:
                    if p_count >= 3:
                        percentage_commission = 0
                    elif len(payment_candidates) == 0:
                        percentage_commission = upline.realtor_type.percentage_commission
                    else:
                        percentage_commission = upline.realtor_type.percentage_commission / 2
                    p_count += 1
                elif upline.realtor_type.name == RealtorType.ASSOCIATE_PARTNER:
                    if ap_added:
                        percentage_commission = 0
                    elif len(payment_candidates) == 0:
                        percentage_commission = upline.realtor_type.percentage_commission
                    else:
                        if p_count > 2:
                            partner = next(
                                candidate for candidate in
                                payment_candidates[::-1]
                                if (candidate[
                                        0].realtor_type.name == RealtorType.PARTNER) and (
                                        candidate[1] > 0))
                            payment_candidates.pop(
                                payment_candidates.index(partner))
                            percentage_commission = partner[1]
                elif upline.realtor_type.name == RealtorType.EXECUTIVE_PARTNER:
                    if ep_added:
                        percentage_commission = 0
                    elif len(payment_candidates) == 0:
                        percentage_commission = upline.realtor_type.percentage_commission
                    else:
                        if p_count > 2:
                            partner = next(
                                candidate for candidate in
                                payment_candidates[::-1]
                                if (candidate[
                                        0].realtor_type.name == RealtorType.PARTNER) and (
                                        candidate[1] > 0))
                            payment_candidates.pop(
                                payment_candidates.index(partner))
                            percentage_commission = partner[1]
                        elif p_count > 1 and ap_added:
                            for i in range(2):
                                partner = next(
                                    candidate for candidate in
                                    payment_candidates[::-1]
                                    if (candidate[
                                            0].realtor_type.name == RealtorType.PARTNER) and (
                                            candidate[1] > 0))
                                payment_candidates.pop(
                                    payment_candidates.index(partner))
                                percentage_commission = partner[1]

            commission = (percentage_commission / 100) * float(amount_paid)
            percentage_left -= percentage_commission
            payment_candidates.append([upline, commission])
            upline = upline.upline
        for index, candidate in payment_candidates:
            if candidate[1] > 0:
                payment_candidates.pop(index)
        return payment_candidates
