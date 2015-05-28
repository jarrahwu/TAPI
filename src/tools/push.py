__author__ = 'jarrah'
import jpush

KEY = 'bb2a2ad8ff2179e3cadb9e29'
SECRET = 'f01143b6fe4a1c1abcda0ffb'


class Messenger:

    def __init__(self):
        context = jpush.JPush(KEY, SECRET)
        self.push = context.create_push()
        self.push.audience = jpush.all_

    def send_message(self, message, alias=None, **kwargs):

        if alias is not None:
            self.push.audience = jpush.audience(jpush.alias(*alias))

        self.push.message = jpush.message(msg_content=message, extras=kwargs)
        self.push.platform = jpush.platform('android', 'ios')
        self.push.send()

    def send_notification(self, title, alert, alias=None, **kwargs):
        android = jpush.android(alert=alert, title=title, extras=kwargs)

        if alias is not None:
            self.push.audience = jpush.audience(jpush.alias(*alias))

        # ios = None
        self.push.notification = jpush.notification(alert=alert, android=android)
        self.push.platform = jpush.platform('android', 'ios')
        self.push.send()


# msg = Messenger()
# msg.send_notification('hello', alert='hi', alias=['abcdef'], key='k', value='v')
# msg.send_notification(title='TITLE', alert='ALERT', key='k', value='v')

