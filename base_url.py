def get_base_url():
    '''
    Retorna a URL base da API de marcio, a depender do ambiente.\n
    Desenvolvimento: http://75.119.134.38:2004/dp/hunnodev/file/\n
    Produção: http://75.119.134.38:2004/dp/hunno/file/
    '''
    import os
    from dotenv import load_dotenv
    load_dotenv()

    ROTA_API_HUNNO = os.getenv('ROTA_API_HUNNO')
    if ROTA_API_HUNNO is None:
        raise Exception('Crie uma variavel de ambiente, para a ROTA_API_HUNNO, dica:\nDesenvolvimento: http://75.119.134.38:2004/dp/hunnodev/\nProdução: http://75.119.134.38:2004/dp/hunno/')
    return ROTA_API_HUNNO
if __name__ == "__main__":
    print(get_base_url())
    