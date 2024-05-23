import React, { useState, useEffect } from "react";
import { format } from "date-fns";
import "../Formulario/formularioCSS.css";
import "../Formulario/ButtonStyle.css";

export function DatosEnvio() {
    const [Fecha_de_recepcion, setFecha_de_recepcion] = useState("");
    const [Ciudad, setCiudad] = useState("");
    const [Codigo_postal, setCodigo_postal] = useState("");
  
    const [Direccion_envio, setDireccion_envio] = useState("");
    const [Es_sobre, setEs_sobre] = useState(false);
    const [Por_pagar, setPor_pagar] = useState(false);
    const [Tipo_de_envio, setTipo_de_envio] = useState("");
    const [Peso, setPeso] = useState(0.0);
    const [Reparto_a_domicilio, setReparto_a_domicilio] = useState(false);
    return (
        <form className="form-register" id="div_envio">
            <h4>Datos de envio</h4>
            <label className="info_campo">Direccion</label>
            <input
                className="controls"
                type="text"
                value={Direccion_envio}
                placeholder="Ingrese la direccion"
                onChange={(e) => setDireccion_envio(e.target.value)}
            />
            
            <label className="info_campo">Ciudad</label>

            <input
                className="controls"
                type="text"
                value={Ciudad}
                placeholder="Ingrese ciudad"
                onChange={(e) => setCiudad(e.target.value)}
            />
            <label className="info_campo">Código postal</label>

            <input
                className="controls"
                type="text"
                value={Codigo_postal}
                placeholder="Ingrese codigo postal"
                onChange={(e) => setCodigo_postal(e.target.value)}
            />
            <label className="info_campo" htmlFor="tipo_entrega">
                Tipo de entrega
            </label>
            <select
                name="tipo_entrega"
                className="controls"
                onChange={(e) => setTipo_de_envio(e.target.value)}
            >
                <option disabled value="">
                Selecciona una opción
                </option>
                <option value="Entrega en el dia">Entrega en el día</option>
                <option value="Entrega rápida">Entrega rápida</option>
                <option value="Entrega normal">Entrega normal</option>
            </select>
            <label className="info_campo" htmlFor="tipo_paquete">
                Tipo de paquete
            </label>
            <select
                name="tipo_paquete"
                className="controls"
                value={Es_sobre}
                onChange={(e) => setEs_sobre(e.target.value === "true")}
            >
                <option disabled value="">
                Selecciona una opción
                </option>
                <option value="true">Sobre</option>
                <option value="false">Encomienda</option>
            </select>
            {Es_sobre === false && (
                <React.Fragment>
                <label className="info_campo" htmlFor="tipo_paquete">
                    Indique peso en KG
                </label>
                <input
                    className="controls"
                    type="text"
                    value={Peso}
                    onChange={(e) => setPeso(e.target.value)}
                />
                </React.Fragment>
            )}

            <label className="etiquetas" htmlFor="pago">
                Pagado por
            </label>
            <select
                name="pago"
                className="controls"
                value={Por_pagar ? "true" : "false"}
                onChange={(e) => setPor_pagar(e.target.value === "true")}
            >
                <option disabled selected hidden value="">
                Selecciona una opción
                </option>
                <option value="false">Remitente</option>
                <option value="true">Destinatario</option>
            </select>

            <div className="pasar_pagina">
                <a href= "#/IngresoDatosDestinatario"className="buttons" type="submit" value="Registrar">
                    Volver
                </a>
                <a href= "#/envio"className="buttons" type="submit" value="Registrar">
                    Enviar
                </a>
            </div>

        </form>
    )
}

