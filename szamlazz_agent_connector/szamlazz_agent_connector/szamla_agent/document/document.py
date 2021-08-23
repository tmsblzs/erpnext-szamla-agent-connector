from szamlazz_agent_connector.szamlazz_agent_connector.szamla_agent.currency import Currency
from szamlazz_agent_connector.szamlazz_agent_connector.szamla_agent.language import Language


class Document:
    PAYMENT_METHOD_TRANSFER = 'átutalás'
    PAYMENT_METHOD_CASH = 'készpénz'
    PAYMENT_METHOD_BANKCARD = 'bankkártya'
    PAYMENT_METHOD_CHEQUE = 'csekk'
    PAYMENT_METHOD_CASH_ON_DELIVERY = 'utánvét'
    PAYMENT_METHOD_PAYPAL = 'PayPal'
    PAYMENT_METHOD_SZEP_CARD = 'SZÉP kártya'
    PAYMENT_METHOD_OTP_SIMPLE = 'OTP Simple'

    DOCUMENT_TYPE_INVOICE = 'invoice'

    DOCUMENT_TYPE_INVOICE_CODE = 'SZ'

    DOCUMENT_TYPE_REVERSE_INVOICE = 'reverseInvoice'

    DOCUMENT_TYPE_REVERSE_INVOICE_CODE = 'SS'

    DOCUMENT_TYPE_PAY_INVOICE = 'payInvoice'

    DOCUMENT_TYPE_PAY_INVOICE_CODE = 'JS'

    DOCUMENT_TYPE_CORRECTIVE_INVOICE = 'correctiveInvoice'

    DOCUMENT_TYPE_CORRECTIVE_INVOICE_CODE = 'HS'

    DOCUMENT_TYPE_PREPAYMENT_INVOICE = 'prePaymentInvoice'

    DOCUMENT_TYPE_PREPAYMENT_INVOICE_CODE = 'ES'

    DOCUMENT_TYPE_FINAL_INVOICE = 'finalInvoice'

    DOCUMENT_TYPE_FINAL_INVOICE_CODE = 'VS'

    DOCUMENT_TYPE_PROFORMA = 'proforma'

    DOCUMENT_TYPE_PROFORMA_CODE = 'D'

    DOCUMENT_TYPE_DELIVERY_NOTE = 'deliveryNote'

    DOCUMENT_TYPE_DELIVERY_NOTE_CODE = 'SL'

    DOCUMENT_TYPE_RECEIPT = 'receipt'

    DOCUMENT_TYPE_RECEIPT_CODE = 'NY'

    DOCUMENT_TYPE_RESERVE_RECEIPT = 'reserveReceipt'

    DOCUMENT_TYPE_RESERVE_RECEIPT_CODE = 'SN'

    @staticmethod
    def get_default_currency():
        return Currency.get_default()

    @staticmethod
    def get_default_language():
        return Language.get_default()
