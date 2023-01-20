from urllib.parse import unquote

from szamlazz_agent_connector.szamlazz_agent_connector.model.constant.invoice_constant import InvoiceConstant
from szamlazz_agent_connector.szamlazz_agent_connector.model.constant.response_constant import ResponseConstant
from szamlazz_agent_connector.szamlazz_agent_connector.model.response.invoice_response import InvoiceResponse


class InvoiceParser:
    @staticmethod
    def parse_data(data, response_type=ResponseConstant.RESULT_AS_TEXT):
        response = InvoiceResponse()
        headers = data['headers']
        is_pdf = InvoiceParser.is_pdf_response(data)
        pdf_file = ''

        if 'body' in data:
            pdf_file = data['body']
        elif response_type == ResponseConstant.RESULT_AS_XML and 'pdf' in data:
            pdf_file = data['pdf']

        if headers:
            response.headers = headers

            if 'szlahu_szamlaszam' in headers:
                response.invoice_number = headers['szlahu_szamlaszam']
            if 'szlahu_vevoifiokurl' in headers:
                response.user_account_url = headers['szlahu_vevoifiokurl']
            if 'szlahu_kintlevoseg' in headers:
                response.asset_amount = headers['szlahu_kintlevoseg']
            if 'szlahu_nettovegosszeg' in headers:
                response.net_price = headers['szlahu_nettovegosszeg']
            if 'szlahu_bruttovegosszeg' in headers:
                response.gross_amount = headers['szlahu_bruttovegosszeg']
            if 'szlahu_error' in headers:
                error = unquote(headers['szlahu_error'])
                response.error_message = error
            if is_pdf and pdf_file:
                response.pdf_data = pdf_file
            if not response.is_error():
                response.success = True

            return response

    @staticmethod
    def is_pdf_response(result):
        if 'pdf' in result:
            return True

        if 'content-type' in result['headers'] \
                and result['headers']['content-type'] == 'application/pdf':
            return True

        if 'content-disposition' in result['headers'] \
                and result['headers']['content-disposition'].find('pdf') != -1:
            return True

        return False

