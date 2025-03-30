import ssl

protocolos = {
    "PROTOCOL_TLS_CLIENT": ssl.PROTOCOL_TLS_CLIENT,
    "PROTOCOL_TLS_SERVER": ssl.PROTOCOL_TLS_SERVER,
    "PROTOCOL_TLSv1": ssl.PROTOCOL_TLSv1,
    "PROTOCOL_TLSv1_1": ssl.PROTOCOL_TLSv1_1,
    "PROTOCOL_TLSv1_2": ssl.PROTOCOL_TLSv1_2,
    # "PROTOCOL_TLSv1_3": ssl.PROTOCOL_TLSv1_3
}

for nome_proto, proto in protocolos.items():
    try:
        contexto = ssl.SSLContext(proto)
        ciphers = contexto.get_ciphers()
        print(f"\nProtocolo: {nome_proto}")
        for c in ciphers:
            print(f"  - {c['name']}")
    except Exception as e:
        print(f"\nProtocolo: {nome_proto} não é suportado neste ambiente ({e}).")
