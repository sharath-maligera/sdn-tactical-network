import json
import logging

from ryu.app.qos import qos_switch

from webob import Response
from ryu.controller import ofp_event
from ryu.controller.handler import CONFIG_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.app.wsgi import ControllerBase, WSGIApplication, route
from ryu.lib import dpid as dpid_lib

simple_switch_instance_name = "simple_switch_api_app"

add_reservation_url = "/add_reservation"
start_qos_url = "/start_qos"


class QoSSwitchRest13(qos_switch.QoSSwitch13):

    _CONTEXTS = { "wsgi": WSGIApplication }

    def __init__(self, *args, **kwargs):
        super(QoSSwitchRest13, self).__init__(*args, **kwargs)
        self.switches = {}
        print "SELF_QOS: " + str(self.qos)
        wsgi = kwargs["wsgi"]
        wsgi.register(QoSController, {simple_switch_instance_name : self})

    @set_ev_cls(ofp_event.EventOFPSwitchFeatures, CONFIG_DISPATCHER)
    def switch_features_handler(self, ev):
        super(QoSSwitchRest13, self).switch_features_handler(ev)
        datapath = ev.msg.datapath
        self.switches[datapath.id] = datapath
        QOS_OBJECT = self.qos
        self.mac_to_port.setdefault(datapath.id, {})

class QoSController(ControllerBase):

    def __init__(self, req, link, data, **config):
        super(QoSController, self).__init__(req, link, data, **config)
        self.simple_switch_app = data[simple_switch_instance_name]


    @route("start_qos", start_qos_url, methods=["POST"])
    def start_qos(self, req, **kwargs):
        simple_switch = self.simple_switch_app
        simple_switch.qos.start()


    @route("add_reservation", add_reservation_url, methods=["POST"])
    def list_mac_table(self, req, **kwargs):
        data = req.json
        simple_switch = self.simple_switch_app
        request_data = {
            "src": data["src"],
            "dst": data["dst"],
            "bw": data["bw"]
        }

        simple_switch.qos.add_reservation(request_data)
        body = json.dumps({"mac_table": "hi"})
        return Response(content_type="application/json", body=body)
