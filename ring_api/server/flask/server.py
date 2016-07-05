from flask import Flask
from flask_restful import Api

from flask_socketio import SocketIO

from ring_api.server.flask import socketio_cb_api as cb_api
from ring_api.server.flask.api import account, video, calls, certificate

class FlaskServer:
    def __init__(self, host, port, dring):
        self.host = host
        self.port = port
        self.dring = dring

        self.app = Flask(__name__)
        self.app.config['SECRET_KEY'] = 't0p_s3cr3t'
        self.app.config.update(
            PROPAGATE_EXCEPTIONS = True
        )
        self.api = Api(self.app, catch_all_404s=True)
        self.socketio = SocketIO(self.app)

        self._add_resources()
        self._register_callbacks()

    def _add_resources(self):
        """Keep the same order as in the rest-api.json."""

        # Accounts

        self.api.add_resource(account.Account, '/account/',
            resource_class_kwargs={'dring': self.dring})
        
        self.api.add_resource(account.Accounts, '/accounts/',
            resource_class_kwargs={'dring': self.dring})
        
        self.api.add_resource(account.AccountsID, '/accounts/<account_id>/',
            resource_class_kwargs={'dring': self.dring})
        
        self.api.add_resource(account.AccountsDetails,
            '/accounts/<account_id>/details/',
            resource_class_kwargs={'dring': self.dring})
        
        self.api.add_resource(account.AccountsCall,
            '/accounts/<account_id>/call/',
            resource_class_kwargs={'dring': self.dring})
        
        self.api.add_resource(account.AccountsCertificates,
            '/accounts/<account_id>/certificates/<cert_id>/',
            resource_class_kwargs={'dring': self.dring})

        # Calls 

        self.api.add_resource(calls.Calls,
            '/calls/<call_id>/',
            resource_class_kwargs={'dring': self.dring})

        # Codecs
        # Crypto
        # Certificate

        self.api.add_resource(certificate.Certificate,
            '/certificates/',
            resource_class_kwargs={'dring': self.dring})

        self.api.add_resource(certificate.Certificates,
            '/certificate/<cert_id>/',
            resource_class_kwargs={'dring': self.dring})

        # Audio
        # Video

        self.api.add_resource(video.VideoDevices,
            '/video/devices/',
            resource_class_kwargs={'dring': self.dring})

        self.api.add_resource(video.VideoSettings,
            '/video/<device_id>/settings/',
            resource_class_kwargs={'dring': self.dring})
        
        self.api.add_resource(video.VideoCamera,
            '/video/camera/',
            resource_class_kwargs={'dring': self.dring})

    def _register_callbacks(self):
        callbacks = self.dring.callbacks_to_register()

        # TODO add dynamically from implemented function names
        callbacks['text_message'] = cb_api.text_message

        self.dring.register_callbacks(callbacks, context=self.socketio)

    def start(self):
        self.socketio.run(self.app, host=self.host, port=self.port)

    def stop(self):
        pass

