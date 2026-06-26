from flask import Flask, render_template, request, redirect, url_for, session

from config import UICC_BIN_DEFAULT, UICC_PORT_DEFAULT, UICC_SIMULATE_DEFAULT
from uicc_runner import build_program_command, execute_program_command, read_card
from validators import validate_program_form

app = Flask(__name__)
app.secret_key = "uicc-lab-local-dev-key"


def get_runtime_config():
    """
    Retorna la configuració activa del web.
    Es pot canviar des de la pantalla principal.
    """
    return {
        "uicc_bin": session.get("uicc_bin", UICC_BIN_DEFAULT),
        "uicc_port": session.get("uicc_port", UICC_PORT_DEFAULT),
        "simulate": session.get("simulate", UICC_SIMULATE_DEFAULT),
    }


def normalize_program_form(form_data):
    """
    Ajusta dades del formulari abans de validar o construir la comanda.
    Fusiona els 3 camps IMSI en un sol camp 'imsi'.
    """
    data = dict(form_data)

    imsi_mcc = data.get("imsi_mcc", "").strip()
    imsi_mnc = data.get("imsi_mnc", "").strip()
    imsi_msin = data.get("imsi_msin", "").strip()

    data["imsi"] = imsi_mcc + imsi_mnc + imsi_msin

    return data


@app.route("/")
def index():
    cfg = get_runtime_config()
    return render_template(
        "index.html",
        uicc_bin=cfg["uicc_bin"],
        uicc_port=cfg["uicc_port"],
        simulate=cfg["simulate"],
    )


@app.route("/mode", methods=["POST"])
def mode():
    session["simulate"] = request.form.get("simulate") == "on"
    session["uicc_bin"] = request.form.get("uicc_bin", UICC_BIN_DEFAULT).strip()
    session["uicc_port"] = request.form.get("uicc_port", UICC_PORT_DEFAULT).strip()
    return redirect(url_for("index"))


@app.route("/read")
def read():
    cfg = get_runtime_config()
    result = read_card(
        uicc_bin=cfg["uicc_bin"],
        uicc_port=cfg["uicc_port"],
        simulate=cfg["simulate"],
    )
    return render_template("result.html", result=result)


@app.route("/program")
def program():
    cfg = get_runtime_config()
    return render_template(
        "program.html",
        uicc_port=cfg["uicc_port"],
        simulate=cfg["simulate"],
    )


@app.route("/program/preview", methods=["POST"])
def program_preview():
    cfg = get_runtime_config()
    form_data = normalize_program_form(request.form.to_dict())
    errors = validate_program_form(form_data)

    if errors:
        return render_template(
            "program.html",
            errors=errors,
            form_data=form_data,
            uicc_port=cfg["uicc_port"],
            simulate=cfg["simulate"],
        )

    preview = build_program_command(
        form_data,
        uicc_bin=cfg["uicc_bin"],
        uicc_port=cfg["uicc_port"],
    )

    return render_template(
        "program_preview.html",
        preview=preview,
        form_data=form_data,
    )

@app.route("/program/execute", methods=["POST"])
def program_execute():
    cfg = get_runtime_config()
    form_data = normalize_program_form(request.form.to_dict())
    errors = validate_program_form(form_data)

    if errors:
        return render_template(
            "program.html",
            errors=errors,
            form_data=form_data,
            uicc_port=cfg["uicc_port"],
            simulate=cfg["simulate"],
        )

    result = execute_program_command(
        form_data,
        uicc_bin=cfg["uicc_bin"],
        uicc_port=cfg["uicc_port"],
        simulate=cfg["simulate"],
    )

    return render_template("result.html", result=result)

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
