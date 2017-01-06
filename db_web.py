# coding = utf-8

from db_manage import cxOracle
import logging
from spyne import Application, rpc, ServiceBase, String
from spyne.protocol.xml import XmlDocument
from spyne.protocol.http import HttpRpc
from spyne.server.wsgi import WsgiApplication
from wsgiref.simple_server import make_server

class CardIdCheck(ServiceBase):
    @rpc(String, String, _returns=String)
    def CheckID(ctx, cardno, idno):
        cid = _GetID(cardno)
        if idno == cid:
            return "True"
        return "False"

def _GetID(cardno):
    conn = cxOracle()
    sql = "select gen_encrypt_decrypt.decryptHEX(code_idcard) from card where card_number = %s " % cardno
    result = conn.Query(sql, 0, 1)
    idno = str(result[0][0][-4:])
    return idno


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    application = Application([CardIdCheck], 'id_check',
                              in_protocol=HttpRpc(validator='soft'),
                              out_protocol=XmlDocument(),
                              )
    wsgi_application = WsgiApplication(application)

    server = make_server("10.137.60.198", 8000, wsgi_application)
    logging.info("listening to http://10.137.60.198:8000")
    logging.info("wsdl is at: http://10.137.60.198:8000/?wsdl")
    server.serve_forever()

