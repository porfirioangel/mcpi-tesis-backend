**TESIS MCPI BACKEND**
---

Proyecto de desarrollo para la tesis de la Maestría en Ciencias del Procesamiento de la Información.

- [Requisitos](#requisitos)
- [Instrucciones de instalación](#instrucciones-de-instalación)
- [Instrucciones de ejecución](#instrucciones-de-ejecución)
- [Comandos útiles](#comandos-útiles)
  - [Manejo de procesos](#manejo-de-procesos)
- [Recursos](#recursos)
- [Solución de problemas](#solución-de-problemas)
- [Jupyter is already running:](#jupyter-is-already-running)

# Requisitos

- Pipenv
- Nodejs

# Instrucciones de instalación

Instalar dependencias:

```bash
pipenv install --dev
```

# Instrucciones de ejecución

Activar virtualenv:

```bash
pipenv shell
```

Correr proyecto:

```bash
python run.py
```

# Comandos útiles

## Manejo de procesos

Obtener id del proceso iniciado por un comando:

```bash
ps aux | grep python | awk '{ print $2,$11,$12 }'
```

Detener un proceso por medio de su id:

```bash
kill -9 <pid>
```

# Recursos

- [Resultados encuesta](https://drive.google.com/drive/u/1/folders/19EUNpSZYqA0abc3yoJ8vnRST6V9SuH8E)

# Solución de problemas

# Jupyter is already running:

```bash
lsof -i -P -n | grep "8888 (LISTEN)"
```
