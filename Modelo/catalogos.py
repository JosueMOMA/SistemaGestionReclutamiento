"""Catálogos de selección usados por las vistas y validaciones del dominio."""

AFP_DESCUENTOS = {
    "AFP Integra": 13.31,
    "AFP Habitat": 12.74,
    "AFP Prima": 13.07,
    "AFP Profuturo": 13.32,
    "ONP": 13.00,
}

PROFESIONES = {
    "Técnico": [
        "Técnico Agropecuario",
        "Técnico en Industrias Alimentarias",
        "Técnico en Mecánica de Mantenimiento",
        "Técnico en Electricidad Industrial",
        "Técnico en Seguridad Industrial",
        "Técnico en Administración",
        "Técnico en Contabilidad",
        "Técnico en Computación e Informática",
    ],
    "Universitario": [
        "Ingeniería Agrónoma",
        "Ingeniería Agroindustrial",
        "Ingeniería Industrial",
        "Ingeniería Mecánica",
        "Ingeniería Ambiental",
        "Ingeniería de Sistemas",
        "Administración",
        "Contabilidad",
        "Economía",
        "Psicología",
        "Derecho",
    ],
}

UBICACIONES = {
    "Lima": {
        "Lima": ["Lima", "Miraflores", "San Isidro", "Santiago de Surco"],
        "Callao": ["Callao", "Bellavista", "La Perla", "Ventanilla"],
    },
    "Arequipa": {
        "Arequipa": ["Arequipa", "Cayma", "Cerro Colorado", "Yanahuara"],
        "Camaná": ["Camaná", "Mariano Nicolás Valcárcel", "Ocoña"],
    },
    "La Libertad": {
        "Trujillo": ["Trujillo", "El Porvenir", "La Esperanza", "Victor Larco Herrera"],
        "Ascope": ["Ascope", "Casa Grande", "Chicama"],
    },
    "Piura": {
        "Piura": ["Piura", "Castilla", "Catacaos", "Veintiséis de Octubre"],
        "Sullana": ["Sullana", "Bellavista", "Marcavelica", "Querecotillo"],
    },
    "Ica": {
        "Ica": ["Ica", "La Tinguiña", "Los Aquijes", "Parcona"],
        "Chincha": ["Chincha Alta", "Alto Larán", "Grocio Prado", "Tambo de Mora"],
    },
}

# (nombre del puesto, sueldo base mensual en soles)
PUESTOS_POR_AREA_Y_GRADO = {
    "Producción Agrícola": {
        "Secundaria completa": [
            ("Operario Agrícola", 1130.00),
            ("Cosechador", 1200.00),
            ("Regador", 1250.00),
        ],
        "Técnico": [
            ("Técnico de Campo", 1800.00),
            ("Supervisor de Riego", 2400.00),
            ("Técnico de Sanidad Vegetal", 2200.00),
        ],
        "Universitario": [
            ("Ingeniero Agrónomo", 4500.00),
            ("Jefe de Producción Agrícola", 6500.00),
        ],
    },
    "Operaciones y Planta": {
        "Secundaria completa": [
            ("Operario de Planta", 1200.00),
            ("Auxiliar de Almacén", 1300.00),
        ],
        "Técnico": [
            ("Técnico de Producción", 2100.00),
            ("Técnico de Mantenimiento", 2300.00),
            ("Supervisor de Planta", 3000.00),
        ],
        "Universitario": [
            ("Ingeniero de Procesos", 4800.00),
            ("Jefe de Planta", 7000.00),
        ],
    },
    "Calidad e Inocuidad": {
        "Secundaria completa": [("Auxiliar de Calidad", 1300.00)],
        "Técnico": [
            ("Técnico de Calidad", 2100.00),
            ("Inspector de Inocuidad", 2200.00),
        ],
        "Universitario": [
            ("Ingeniero de Calidad", 4500.00),
            ("Jefe de Calidad", 6500.00),
        ],
    },
    "Mantenimiento": {
        "Secundaria completa": [("Ayudante de Mantenimiento", 1300.00)],
        "Técnico": [
            ("Técnico Mecánico", 2300.00),
            ("Técnico Electricista", 2300.00),
            ("Supervisor de Mantenimiento", 3200.00),
        ],
        "Universitario": [("Ingeniero de Mantenimiento", 5000.00)],
    },
    "Logística y Almacén": {
        "Secundaria completa": [
            ("Auxiliar de Almacén", 1300.00),
            ("Despachador", 1350.00),
        ],
        "Técnico": [
            ("Técnico Logístico", 2100.00),
            ("Supervisor de Almacén", 2800.00),
        ],
        "Universitario": [
            ("Analista de Logística", 3500.00),
            ("Jefe de Logística", 6000.00),
        ],
    },
    "Seguridad y Salud Ocupacional": {
        "Secundaria completa": [("Auxiliar de Seguridad", 1300.00)],
        "Técnico": [("Técnico de Seguridad Industrial", 2200.00)],
        "Universitario": [
            ("Ingeniero de Seguridad", 4800.00),
            ("Jefe de Seguridad y Salud", 6500.00),
        ],
    },
    "Recursos Humanos": {
        "Secundaria completa": [("Auxiliar de Recursos Humanos", 1300.00)],
        "Técnico": [("Asistente de Recursos Humanos", 2000.00)],
        "Universitario": [
            ("Analista de Recursos Humanos", 3500.00),
            ("Jefe de Recursos Humanos", 6000.00),
        ],
    },
    "Administración y Finanzas": {
        "Secundaria completa": [("Auxiliar Administrativo", 1300.00)],
        "Técnico": [("Asistente Administrativo", 2000.00)],
        "Universitario": [
            ("Analista Contable", 3500.00),
            ("Administrador", 4500.00),
            ("Jefe de Administración y Finanzas", 6500.00),
        ],
    },
    "Comercial": {
        "Secundaria completa": [("Promotor de Ventas", 1300.00)],
        "Técnico": [("Asistente Comercial", 2000.00)],
        "Universitario": [
            ("Analista Comercial", 3500.00),
            ("Jefe Comercial", 6000.00),
        ],
    },
}

REGIMENES = {
    "Régimen General (728)": "general",
    "Régimen Agrario": "agrario",
}


def puestos_disponibles(area, grado):
    """Devuelve los nombres de puestos válidos para área y grado."""
    return [nombre for nombre, _ in PUESTOS_POR_AREA_Y_GRADO.get(area, {}).get(grado, [])]


def sueldo_puesto(area, grado, puesto):
    """Devuelve el sueldo configurado para un puesto o ``None`` si no existe."""
    for nombre, sueldo in PUESTOS_POR_AREA_Y_GRADO.get(area, {}).get(grado, []):
        if nombre == puesto:
            return sueldo
    return None
