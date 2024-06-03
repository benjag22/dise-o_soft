import React, { useState, useEffect } from "react";
import { format } from "date-fns";
import "../Formulario/formularioCSS.css";
import "../Formulario/ButtonStyle.css";
import { BotonNavegar } from "../components/BotonNavegar";
import { useNavigate } from 'react-router-dom';


export function IngresoDatosRemitente() {
    const [Remitente, setRemitente] = useState("");
    const [Correo, setEmail] = useState("");
    const [Recogida_a_domicilio, setRecogidaADomicilio] = useState(false);
    const [Direccion_remitente, setDireccion_recogida] = useState("");


    const navigate = useNavigate();

    const redirectToPage = () => {
        navigate('/IngresoDatosDestinatario');
    };
    return (
        <form className="form-register" id="div_remitente" onSubmit={redirectToPage}>
            <h4>Datos Remitente</h4>
            <label className="info_campo" htmlFor="nombre">Nombre completo</label>
            <input
                className="controls"
                type="text"
                value={Remitente}
                placeholder="Ingrese su nombre"
                onChange={(e) => setRemitente(e.target.value)}
                id="nombre"
                required
            />
            <label className="info_campo" htmlFor="correo">Correo electronico</label>
            <input
                className="controls"
                type="email"
                value={Correo}
                placeholder="Ingrese su correo"
                onChange={(e) => setEmail(e.target.value)}
                id="correo"
                required
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
                <div>
                    <label>Direccion Recogida</label>
                    <input
                    className="controls"
                    type="text"
                    value={Direccion_remitente}
                    placeholder="Ingrese su dirección de recogida"
                    onChange={(e) => setDireccion_recogida(e.target.value)}
                    />
                </div>
            )}
            <BotonNavegar paginaAntes="/" botonsiguientetexto="siguiente"/>
        </form>
    )
}

