from requests import Session
from requests.auth import HTTPBasicAuth
import json

try:
    from zeep import Client
    from zeep.cache import SqliteCache
    from zeep.transports import Transport
    from zeep.settings import Settings
except:
    raise ValueError("zeep library is not installed. Run 'pip install zeep' for installing it.\n")

if api.config.wsdl == "":
    raise ValueError("The WSDL File config field cannot be empty.")

if api.config.operationName == "":
    raise ValueError("The Operation Name config field cannot be empty.")


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
        api.send("debug", str(excp))

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
        api.send("debug", str(other))

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
        api.send("debug", str(other))

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
        api.send("debug", str(other))


api.set_port_callback("serviceName", on_input)
