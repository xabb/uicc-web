# uicc-web
## Instal·lació

Aquest projecte és una GUI web de laboratori local per llegir, validar i programar targetes UICC/SIM amb `program_uicc` ja compilat i funcional.

L'aplicació web no inclou el binari `program_uicc`: només el crida des de Python. Abans d'arrencar el web cal assegurar-se que l'executable existeix i és accessible.

https://open-cells.com/index.php/uiccsim-programing/

### Clonar el projecte

```bash
git clone https://github.com/xabb/uicc-web.git
cd uicc-web
```

### Crear l'entorn virtual de Python

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Comprovar que s'està utilitzant Python 3 dins del virtualenv:

```bash
which python
python --version
```

La ruta hauria d'apuntar a alguna cosa semblant a:

```text
/home/usuari/uicc-web/.venv/bin/python
```

### Instal·lar dependències

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### Comprovar el binari `program_uicc`

L'aplicació està preparada per trobar l'executable en aquesta ruta per defecte:

```text
/usr/local/bin/program_uicc
```

Comprova que existeix:

```bash
which program_uicc
program_uicc --help
```

El resultat esperat és que `which` retorni:

```text
/usr/local/bin/program_uicc
```

Si el binari ja està compilat però encara no està instal·lat en aquesta ruta, es pot copiar, per exemple, així:

```bash
sudo mkdir -p /opt/program-uicc
sudo cp program_uicc /opt/program-uicc/
sudo chmod 755 /opt/program-uicc/program_uicc
sudo ln -sf /opt/program-uicc/program_uicc /usr/local/bin/program_uicc
```

Després torna a comprovar:

```bash
which program_uicc
program_uicc --help
```

### Configuració del port sèrie

Per defecte, l'aplicació està pensada per treballar amb un lector sèrie exposat com:

```text
/dev/ttyUSB0
```

Es pot comprovar amb:

```bash
ls -l /dev/ttyUSB*
```

Si el lector apareix amb un altre nom, per exemple `/dev/ttyUSB1`, cal canviar la configuració des de la pantalla inicial del web o bé arrencar l'aplicació amb la variable d'entorn corresponent:

```bash
export UICC_PORT=/dev/ttyUSB1
```

### Permisos del port sèrie

Si el dispositiu és `/dev/ttyUSB0`, l'usuari pot necessitar pertànyer al grup `dialout`:

```bash
sudo usermod -aG dialout $USER
```

Després cal tancar la sessió i tornar a entrar.

Es pot comprovar amb:

```bash
groups
ls -l /dev/ttyUSB0
```

### Evitar interferències de ModemManager

Alguns lectors USB-sèrie poden ser capturats per `ModemManager`.

Per aturar-lo temporalment:

```bash
sudo systemctl stop ModemManager
```

Per comprovar si algun procés està utilitzant el port:

```bash
sudo fuser -v /dev/ttyUSB0
sudo lsof /dev/ttyUSB0
```

### Arrencar l'aplicació

Des de la carpeta del projecte:

```bash
source .venv/bin/activate
python app.py
```

Obrir el navegador a:

```text
http://127.0.0.1:5000
```

### Configuració per defecte

La configuració per defecte de l'aplicació és:

```text
Mode: real
Executable: /usr/local/bin/program_uicc
Port: /dev/ttyUSB0
```

Aquests valors es defineixen a `config.py`.

També es poden sobreescriure amb variables d'entorn abans d'arrencar el web:

```bash
export UICC_SIMULATE=0
export UICC_BIN=/usr/local/bin/program_uicc
export UICC_PORT=/dev/ttyUSB0
python app.py
```

### Mode simulació

Per provar el web sense lector ni targeta:

```bash
export UICC_SIMULATE=1
python app.py
```

En mode simulació:

* la lectura retorna dades de prova;
* l'execució real queda bloquejada;
* no s'escriu res a cap targeta.

També es pot canviar entre mode real i mode simulació des de la pantalla inicial del web.

### Prova recomanada abans d'utilitzar el web

Abans de dependre de la interfície web, és recomanable comprovar que el binari funciona directament:

```bash
sudo /usr/local/bin/program_uicc --port /dev/ttyUSB0
```

Si aquesta ordre no funciona, el web tampoc podrà comunicar-se correctament amb la targeta.

### Com troba `app.py` l'executable

L'aplicació no busca el binari automàticament per tot el sistema. La ruta ve definida per la configuració.

Per defecte, `config.py` defineix:

```python
UICC_BIN_DEFAULT = os.environ.get("UICC_BIN", "/usr/local/bin/program_uicc")
UICC_PORT_DEFAULT = os.environ.get("UICC_PORT", "/dev/ttyUSB0")
```

Això vol dir que, si no s'indica res més, el web executarà:

```bash
/usr/local/bin/program_uicc --port /dev/ttyUSB0
```

Si el binari està en una altra ruta, hi ha dues opcions:

1. Crear un enllaç simbòlic cap a `/usr/local/bin/program_uicc`.
2. Indicar la ruta amb `UICC_BIN` abans d'arrencar:

```bash
export UICC_BIN=/ruta/al/binari/program_uicc
python app.py
```
