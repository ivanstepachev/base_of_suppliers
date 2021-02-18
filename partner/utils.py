from partner.models import Action, Partner

admin = Partner.objects.get(id=1)


def action_alert(verb, to_partner, to_grand_partner=admin):
    action = Action(verb=verb, to_partner=to_partner, to_grand_partner=to_grand_partner)
    action.save()
