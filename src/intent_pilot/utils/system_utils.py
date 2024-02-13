from plyer import notification

def show_notification(title, message):
    notification.notify(
        title=title,
        message=message,
        app_name='Your Application Name',
        timeout=10  # Duration in seconds the notification stays
    )
