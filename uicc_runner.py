import shlex
import subprocess


def read_card(uicc_bin, uicc_port, simulate):
    """
    Llegeix una targeta UICC.

    En mode simulació retorna dades inventades.
    En mode real executa el binari configurat.
    """
    if simulate:
        return {
            "ok": True,
            "command": "[SIMULACIÓ] program_uicc --port /dev/ttyUSB0",
            "stdout": """Existing values in USIM

ICCID: 89860061100000000123
USIM IMSI: 208920100001123
USIM MSISDN: 00000123
USIM Service Provider Name: OpenCells
""",
            "stderr": "",
        }

    command = [uicc_bin, "--port", uicc_port]

    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=30,
            check=False,
        )

        return {
            "ok": result.returncode == 0,
            "command": " ".join(command),
            "stdout": result.stdout,
            "stderr": result.stderr,
        }

    except FileNotFoundError:
        return {
            "ok": False,
            "command": " ".join(command),
            "stdout": "",
            "stderr": f"No s'ha trobat el binari: {uicc_bin}",
        }

    except subprocess.TimeoutExpired:
        return {
            "ok": False,
            "command": " ".join(command),
            "stdout": "",
            "stderr": "Timeout llegint la targeta.",
        }


def hide_secret(value):
    """
    Amaga un valor sensible.
    """
    if value == "":
        return ""
    return "********"


def build_program_command(form_data, uicc_bin, uicc_port):
    """
    Construeix la comanda de programació.
    """
    port = form_data.get("port", uicc_port).strip()

    command = [uicc_bin, "--port", port]
    safe_command = [uicc_bin, "--port", port]

    fields = [
        ("adm", "--adm", True),
        ("iccid", "--iccid", False),
        ("imsi", "--imsi", False),
        ("isdn", "--isdn", False),
        ("acc", "--acc", False),
        ("key", "--key", True),
        ("opc", "--opc", True),
        ("op", "--xx", True),
        ("spn", "--spn", False),
        ("mnc_size", "--MNCsize", False),
        ("act", "--act", False),
        ("ust", "--ust", False),
    ]

    for field_name, option_name, is_secret in fields:
        value = form_data.get(field_name, "").strip()

        if value != "":
            command.append(option_name)
            command.append(value)

            safe_command.append(option_name)

            if is_secret:
                safe_command.append(hide_secret(value))
            else:
                safe_command.append(value)

    if form_data.get("authenticate") == "on":
        command.append("--authenticate")
        safe_command.append("--authenticate")

    if form_data.get("noreadafter") == "on":
        command.append("--noreadafter")
        safe_command.append("--noreadafter")

    return {
        "real_command_list": command,
        "safe_command_list": safe_command,
        "real_command": shlex.join(command),
        "safe_command": shlex.join(safe_command),
    }


def execute_program_command(form_data, uicc_bin, uicc_port, simulate):
    """
    Executa la programació real de la targeta.
    En mode simulació no executa res.
    """
    preview = build_program_command(
        form_data,
        uicc_bin=uicc_bin,
        uicc_port=uicc_port,
    )

    if simulate:
        return {
            "ok": False,
            "command": preview["safe_command"],
            "stdout": "",
            "stderr": "Execució bloquejada: l'aplicació està en mode simulació.",
        }

    try:
        result = subprocess.run(
            preview["real_command_list"],
            capture_output=True,
            text=True,
            timeout=60,
            check=False,
        )

        return {
            "ok": result.returncode == 0,
            "command": preview["safe_command"],
            "stdout": result.stdout,
            "stderr": result.stderr,
        }

    except FileNotFoundError:
        return {
            "ok": False,
            "command": preview["safe_command"],
            "stdout": "",
            "stderr": f"No s'ha trobat el binari: {uicc_bin}",
        }

    except subprocess.TimeoutExpired:
        return {
            "ok": False,
            "command": preview["safe_command"],
            "stdout": "",
            "stderr": "Timeout programant la targeta.",
        }
