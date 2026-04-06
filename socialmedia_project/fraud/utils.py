from accounts.models import User

BANNED_WORDS = [
    'hate', 'kill', 'die', 'stupid', 'idiot', 'dumb', 'loser',
    'trash', 'scum', 'worthless', 'ugly', 'fat', 'retard',
    'terrorist', 'bomb', 'attack', 'weapon', 'drugs', 'porn',
    'nude', 'naked', 'sex', 'abuse', 'harass', 'threat',
    'nigger', 'faggot', 'bitch', 'bastard', 'asshole', 'fuck',
    'shit', 'crap', 'damn', 'hell', 'whore', 'slut',
]

SPAM_PATTERNS = [
    'click here', 'buy now', 'free money', 'win prize',
    'limited offer', 'act now', 'make money fast', 'earn from home',
    'crypto giveaway', 'follow for follow', 'f4f', 'l4l',
    'dm for promo', 'link in bio', '100% free', 'guaranteed profit',
]


def check_post_fraud(content, user):
    content_lower = content.lower()

    # Check banned words
    for word in BANNED_WORDS:
        if word in content_lower:
            _flag_user(user, f'Post contained banned word: {word}')
            return True, f'Hateful or abusive content detected: "{word}"'

    # Check spam patterns
    for pattern in SPAM_PATTERNS:
        if pattern in content_lower:
            return True, f'Spam content detected: "{pattern}"'

    # Check if content is too short to be meaningful
    if len(content.strip()) < 5:
        return True, 'Post content is too short or irrelevant'

    # Check if user is already flagged
    if user.is_flagged:
        return True, 'Post from a flagged account'

    # Check post frequency — more than 10 posts is spammy
    from posts.models import Post
    from django.utils import timezone
    from datetime import timedelta
    recent_posts = Post.objects.filter(
        author=user,
        created_at__gte=timezone.now() - timedelta(hours=1)
    ).count()
    if recent_posts >= 10:
        _flag_user(user, 'Posting too frequently — possible spam account')
        return True, 'Too many posts in a short time — spam detected'

    return False, None


def check_comment_fraud(content):
    content_lower = content.lower()

    for word in BANNED_WORDS:
        if word in content_lower:
            return True, f'Abusive comment: "{word}"'

    for pattern in SPAM_PATTERNS:
        if pattern in content_lower:
            return True, f'Spam comment: "{pattern}"'

    return False, None


def check_account_fraud(user):
    reasons = []

    # No profile info at all
    if not user.email:
        reasons.append('No email provided')

    # Username looks like a bot
    import re
    if re.search(r'(bot|spam|fake|auto|xxx|adult)\d*', user.username.lower()):
        reasons.append('Suspicious username pattern')

    # No interests selected
    if not user.interests.exists():
        reasons.append('No interests selected')

    if reasons:
        reason_text = ', '.join(reasons)
        _flag_user(user, reason_text)
        return True, reason_text

    return False, None


def _flag_user(user, reason):
    if not user.is_flagged:
        user.is_flagged = True
        user.flag_reason = reason
        user.save()