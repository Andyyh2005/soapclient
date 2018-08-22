FROM $com.sap.python27

ENV SOAP_CLIENT_HOME=/soapclient

RUN mkdir -p $SOAP_CLIENT_HOME/config
RUN mkdir -p /tmp/soapclient_cache

RUN apt-get install wget -y

RUN wget http://www.soapclient.com/xml/soapresponder.wsdl && \
    cp -R soapresponder.wsdl $SOAP_CLIENT_HOME/config/connector.wsdl && \
    rm soapresponder.wsdl

RUN wget https://bootstrap.pypa.io/get-pip.py && \
    python get-pip.py && \
    hash -r && \
    pip --no-cache-dir install --upgrade pip && \
    rm get-pip.py 

RUN pip --no-cache-dir install 'zeep==3.0.0'