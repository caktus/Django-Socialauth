class AssureEmailForThirdPartyAccounts(object):
    """Adds fake email to authenticated users who don't have any,
    if they had logged in via a third party service.
    """

    def process_request(self, request):

        try:
            user = request.user
        except AttributeError:
            return
        else:
            if user.is_anonymous():
                return
            try:
                auth_meta = AuthMeta.objects.get(user=user)
            except AuthMeta.DoesNotExist:
                return
            else:
                if not user.email:
                    user.email = "%s@%s" % (user.username, auth_meta.provider)
                    user.save()
