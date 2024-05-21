import React, { useState, useEffect } from "react";
import { format } from "date-fns";
import "../Formulario/formularioCSS.css";
import "../Formulario/ButtonStyle.css";

export function IngresoDatosRemitente() {
    const [Remitente, setRemitente] = useState("");
    const [Correo, setEmail] = useState("");
    const [Recogida_a_domicilio, setRecogidaADomicilio] = useState(false);
    const [Direccion_remitente, setDireccion_recogida] = useState("");

    return (
        <form>
            <section className="form-register" id="div_remitente">

                <h4>Datos Remitente</h4>
                <label className="info_campo">Nombre completo</label>
                <input
                    className="controls"
                    type="text"
                    value={Remitente}
                    placeholder="Ingrese su nombre"
                    onChange={(e) => setRemitente(e.target.value)}
                />
                <label className="info_campo">Correo electronico</label>
                <input
                    className="controls"
                    type="email"
                    value={Correo}
                    placeholder="Ingrese su correo"
                    onChange={(e) => setEmail(e.target.value)}
                />
                <label className="info_campo" htmlFor="direccionRecogida">
                    Recogida a domicilio
                </label>
                <select
                    className="controls"
                    value={Recogida_a_domicilio}
                    onChange={(e) => setRecogidaADomicilio(e.target.value === "true")}
                >
                    <option disabled value="">
                    Seleccione una opción
                    </option>
                    <option value="true">Sí</option>
                    <option value="false">No</option>
                </select>
                {Recogida_a_domicilio === true && (
                    <input
                    className="controls"
                    type="text"
                    value={Direccion_remitente}
                    placeholder="Ingrese su dirección de recogida"
                    onChange={(e) => setDireccion_recogida(e.target.value)}
                    />
                )}
                <div className="pasar_pagina">
                    <button href= "/envios"className="buttons" type="submit" value="Registrar">
                        Volver
                    </button>
                    <button href= "/envios"className="buttons" type="submit" value="Registrar">
                        Siguiente
                    </button>
                </div>

            </section>
        </form>
    )
}

