Simple Example for SOAP Client
================================
#### Description

This is an example graph for SOAP Client that shows the use of the Py2 SOAP Client operator (com.sap.soapclient.soapclientpy2).

A request for SOAP service created by the constantgenerator operator labelled 'Constant Generator' is given to the Py2 SOAP Client operator, which sends the request to the web service server.

If the web service server successfully deal with the request, then the response will be sent to response port, and the Py2 SOAP Client operator will output the result as a string to the Response Terminal.

Otherwise, any error message will be sent to the debug port, and the Py2 SOAP Client operator, will output the result as a string to the Debug Terminal.

#### Prerequisites
To run the graph, the following configurations need to be set.

Operator: constantgenerator1 (label: Constant Generator)

* content: Service name.
* mode: pulse.
* duration: 2s.

See also the Py2 SOAP Client operator documentation for more information about request parameters.
