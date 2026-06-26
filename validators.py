import re


def is_digits(value):
    return value.isdigit()


def is_hex(value):
    return re.fullmatch(r"[0-9a-fA-F]+", value) is not None


def luhn_ok(number):
    total = 0
    reverse_digits = number[::-1]

    for i in range(len(reverse_digits)):
        digit = int(reverse_digits[i])

        if i % 2 == 1:
            digit = digit * 2
            if digit > 9:
                digit = digit - 9

        total = total + digit

    return total % 10 == 0


def validate_program_form(form_data):
    errors = []

    adm = form_data.get("adm", "").strip()
    iccid = form_data.get("iccid", "").strip()
    imsi = form_data.get("imsi", "").strip()
    isdn = form_data.get("isdn", "").strip()
    key = form_data.get("key", "").strip()
    opc = form_data.get("opc", "").strip()
    op = form_data.get("op", "").strip()
    acc = form_data.get("acc", "").strip()
    spn = form_data.get("spn", "").strip()
    mnc_size = form_data.get("mnc_size", "").strip()

    authenticate = form_data.get("authenticate")
    noreadafter = form_data.get("noreadafter")

    if adm == "":
        errors.append("L'ADM és obligatori.")
    elif len(adm) != 8:
        errors.append("L'ADM ha de tenir exactament 8 caràcters.")

    if imsi == "":
        errors.append("L'IMSI és obligatori.")
    elif len(imsi) != 15:
        errors.append("L'IMSI ha de tenir exactament 15 dígits.")
    elif not is_digits(imsi):
        errors.append("L'IMSI només pot contenir dígits.")

    if isdn == "":
        errors.append("L'ISDN és obligatori.")
    elif len(isdn) != 8:
        errors.append("L'ISDN ha de tenir exactament 8 dígits.")
    elif not is_digits(isdn):
        errors.append("L'ISDN només pot contenir dígits.")

    if acc == "":
        errors.append("L'ACC és obligatori.")
    elif len(acc) != 4 or not is_hex(acc):
        errors.append("L'ACC ha de tenir exactament 4 caràcters hexadecimals.")

    if key == "":
        errors.append("La Ki és obligatòria.")
    elif len(key) != 32 or not is_hex(key):
        errors.append("La Ki ha de tenir exactament 32 caràcters hexadecimals.")

    if opc == "":
        errors.append("L'OPc és obligatori.")
    elif len(opc) != 32 or not is_hex(opc):
        errors.append("L'OPc ha de tenir exactament 32 caràcters hexadecimals.")

    if spn != "":
        if len(spn) > 16:
            errors.append("L'SPN no hauria de superar els 16 caràcters.")

    if authenticate != "on":
        errors.append("L'opció --authenticate ha d'estar activada.")

    if noreadafter != "on":
        errors.append("L'opció --noreadafter ha d'estar activada.")

    if iccid != "":
        if len(iccid) != 20:
            errors.append("L'ICCID ha de tenir exactament 20 dígits.")
        elif not is_digits(iccid):
            errors.append("L'ICCID només pot contenir dígits.")
        elif not luhn_ok(iccid):
            errors.append("L'ICCID no supera la comprovació Luhn.")

    if op != "":
        if len(op) != 32 or not is_hex(op):
            errors.append("L'OP ha de tenir exactament 32 caràcters hexadecimals.")

    if op != "" and opc != "":
        errors.append("No s'ha d'informar OP i OPc alhora. Tria només un dels dos.")

    if mnc_size != "":
        if mnc_size not in ["2", "3"]:
            errors.append("La mida de l'MNC només pot ser 2 o 3.")

    return errors
