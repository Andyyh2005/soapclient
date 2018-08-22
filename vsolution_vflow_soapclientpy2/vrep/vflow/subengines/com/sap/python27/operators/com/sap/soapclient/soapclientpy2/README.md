SOAP Client
===========

This operator inspects the WSDL document and generates the corresponding code to use the services and types in the document. It will run the specified operation with the specified parameters.

Configuration parameters
------------

* **WSDL File** (type string): The WSDL document path.
* **Port Name** (type string): The port name for the binding service. Defaults to the first port defined in the service element in the WSDL document.
* **Operation Name** (type string): The operation name you want to call 
* **Operation Parameters** (type object): The operation parameters you want to pass to the specified operation
* **SOAP Headers** (type string): A JSON object consists of SOAP Headers. Please note: when the header expects a complex type you can wrape it in a dict.
* **HTTP Authentication User** (type string): Provides the HTTP Authentication user name if the service provider uses the HTTP Authentication header to provide security features instead of incorporating them in the header of a SOAP message.
* **HTTP Authentication Password** (type string): Provide the HTTP Authentication password
* **Session timeout** (type string): To set a transport timeout. The default timeout is 300 seconds
* **SSL Certificate Path** (type string): Specifiy a self-signed certificate path for your host if you need to verify the SSL connection
* **Strict mode** (type bool):  boolean to indicate if the lxml should be parsed a ‘strict’. If false then the recover mode is enabled which tries to parse invalid XML as best as it can. Choose false only if you are working with a SOAP server which is not standards compliant.
* **XML huge tree** (type bool): boolean to indicate if need to disable lxml/libxml2 security restrictions and support very deep trees and very long text content.
* **Cache backend path** (type string): To specify a SqliteCache cache backend to improve performance. If specified, it caches the WSDL and XSD files for 1 hour by default.

Input
------------
* **serviceName** (type string): SOAP service name.

Output
------------
* **response** (type string): The return value of the operation call on the specified soap service.
* **debug** (type string): Debug messages.
