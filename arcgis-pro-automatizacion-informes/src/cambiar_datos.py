 Calculate field: Arcade:
 

    iif($feature["Zonificacion"] == "CV", "005",
    iif($feature["Zonificacion"] == "CZ", "006",
    iif($feature["Zonificacion"] == "E1", "010",
    iif($feature["Zonificacion"] == "H4", "016",
    iif($feature["Zonificacion"] == "I1", "008",
    iif($feature["Zonificacion"] == "OU", "018",
    iif($feature["Zonificacion"] == "RDA", "003",
    iif($feature["Zonificacion"] == "RDM", "002",
    iif($feature["Zonificacion"] == "VT", "004",
    iif($feature["Zonificacion"] == "ZRP", "017",
    iif($feature["Zonificacion"] == "ZTE-2", "023",

    $feature["CODIGO_ZONIFICACION"]
    ))))))))))))

revisar los paréntesis mismo numero de parámetros

$feature.Codigo_Zonificacion