import random


class QueryBuilder:
    LF = "\n"
    CRLF = "\r\n"

    @staticmethod
    def build_query(xml_data, xml_filename):
        letters = list("0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ")
        random.shuffle(letters)
        delim = "".join(letters[0: 16])
        query_data = f'--{delim}{QueryBuilder.CRLF}'
        query_data += f'Content-Disposition: form-data; name="{xml_filename}"; ' \
                      f'filename="{xml_filename}"{QueryBuilder.CRLF}'
        query_data += f'Content-Type: text/xml{QueryBuilder.CRLF}{QueryBuilder.CRLF}'
        query_data += xml_data.decode('utf-8') + QueryBuilder.CRLF
        query_data += f"--{delim}--{QueryBuilder.CRLF}"
        return query_data
