from zeep import Client
from requests import Session
from requests.auth import HTTPBasicAuth
from zeep.cache import SqliteCache
from zeep.transports import Transport
from zeep.settings import Settings
import json


def populate_transport():
    transport = None

    try:
        session = None
        if api.config.sslVerificationPath:
            session = Session()
            session.verify = api.config.sslVerificationPath

        if api.config.httpAuthUser:
            user = api.config.httpAuthUser
            password = api.config.httpAuthPassword

            if not session:
                session = Session()
            session.auth = HTTPBasicAuth(user, password)

        session_timeout = None
        if api.config.sessionTimeout:
            session_timeout = int(api.config.sessionTimeout)

        cache_path = None
        if api.config.cachePath:
            cache_path = api.config.cachePath

        if session or session_timeout or cache_path:
            transport = Transport(cache=SqliteCache(path=cache_path) if cache_path else None,
                                  timeout=session_timeout if session_timeout else 300,
                                  session=session)
    except Exception as excp:
        api.send("debug", "40 " + str(excp))

    return transport


def populate_soap_header():
    lst_normalized_header = []

    try:
        if api.config.soapHeaders:
            header = api.config.soapHeaders
            for key in header.keys():
                if isinstance(header[key], dict):
                    lst_normalized_header.append(key + '=' + json.dumps(header[key]))
                else:
                    lst_normalized_header.append(key + '=' + header[key])
    except Exception as excp:
        api.send("debug", excp)

    return lst_normalized_header


def on_input(servicename):
    service_name = servicename
    wsdl = api.config.wsdl

    strict = api.config.strict
    xml_huge_tree = api.config.xmlHugeTree

    setting = None
    try:
        setting = Settings(strict=strict, xml_huge_tree=xml_huge_tree)
    except Exception as other:
        api.send("debug", "73 " + str(other))

    port_name = None
    if api.config.portName:
        port_name = api.config.portName

    op_name = None
    if api.config.operationName:
        op_name = api.config.operationName

    op_params = None
    try:
        if api.config.operationParameters:
            op_params = api.config.operationParameters.split(',')
    except Exception as other:
        api.send("debug", "88 " + str(other))

    transport = populate_transport()
    lst_normalized_header = populate_soap_header()

    try:
        client = Client(wsdl=wsdl, transport=transport, service_name=service_name, port_name=port_name,
                        settings=setting)
        if op_name:
            response = client.service[op_name](*op_params, _soapheaders=lst_normalized_header)
            api.send("response", str(response))
        else:
            api.send("debug", 'No Operation Name specified!')
    except Exception as other:
        api.send("debug", "101 " + str(other))


# Mock pipeline engine api to allow testing outside pipeline engine
try:
    api
except NameError:
    class api:
        def send(port, data):
             print("Send data \"" + str(data) + "\" to port \"" + port + "\"")

        def set_port_callback(port, callback):
             print(
                 "Call \"" + callback.__name__ + "\" to simulate behavior when messages arrive at port \"" + port + "\"..")
             callback()

        class config:

            wsdl = 'http://www.soapclient.com/xml/soapresponder.wsdl'#'/home/hadoop/datahub/operators/soapclient/calculator.asmx?WSDL' #'http://www.soapclient.com/xml/soapresponder.wsdl'#'http://www.dneonline.com/calculator.asmx?WSDL'
            portName = ''#'CalculatorSoap'  #'SoapResponderPortType'#"CalculatorSoap12"
            operationName = 'Method1'#"Subtract"
            operationParameters = "Hello, World"#"100, 40" #"Oh, shot me"

            soapHeaders = json.loads('{"username": "SAPT_FG_BW", "password": "test", "connector": "__runreport", "argument": {"__p1": "reportId=z17102510142718901115980", "format": "csv"}}')
            # {"username":"SAPT_FG_BW","password":"test"}

            httpAuthUser = ''#'andy'
            httpAuthPassword = ''#'1234'

            sessionTimeout = '300'#'100'
            sslVerificationPath = ''#'/tmp/cert.pem'

            strict = True
            xmlHugeTree = False

            cachePath = '/tmp/sqlite.db'#'/tmp/soapclient_cache/sqlite.db'


'''
# Interface for integrating the request_stock_price() function into the pipeline engine
'''
def interface():

    service_name = 'SoapResponder'#'Calculator'

    try:
        result = on_input(service_name)
    except Exception as excp:
        api.send("debug", excp)


api.set_port_callback("serviceName", interface)
