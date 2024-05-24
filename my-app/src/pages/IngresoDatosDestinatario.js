import React, { useState, useEffect } from "react";
import { format } from "date-fns";
import "../Formulario/formularioCSS.css";
import "../Formulario/ButtonStyle.css";
import { BotonNavegar } from "../components/BotonNavegar";
import { useNavigate } from 'react-router-dom';
import { BotonError } from "../components/BotonError";



export function IngresoDatosDestinatario() {
    const [Destinatario, setDestinatario] = useState("");
    const [Rut_Destinatario, setRut_Destinatario] = useState("");
    const [Fono, setFono] = useState("");
    const [Reparto_a_domicilio, setReparto_a_domicilio] = useState(false);


    const navigate = useNavigate();

    const redirectToPage = () => {
        const regex = /^(\d{1,2}(?:[\.]?\d{3}){2}-[\dkK])$/;
        if (regex.test(Rut_Destinatario)){

            navigate('/IngresoDatosDeEnvio');
        }else{

        }
    };

    return (
        <form className="form-register" id="div_envio" onSubmit={redirectToPage}>
            <h4>Datos del destinatario</h4>
            <label className="info_campo" htmlFor="nombre_destinatario">Nombre destinatario</label>
            <input
                className="controls"
                type="text"
                value={Destinatario}
                placeholder="Ingrese nombre del destinatario"
                onChange={(e) => setDestinatario(e.target.value)}
                id="nombre_destinatario"
                required
            />
            <label className="info_campo" htmlFor="rut_destinatario">R.U.T</label>
            <input
                className="controls"
                type="text"
                value={Rut_Destinatario}
                placeholder="Ingrese Rut"
                onChange={(e) => setRut_Destinatario(e.target.value)}
                id="rut_destinatario"
                required
            />
            <label className="info_campo" htmlFor="fono_remitente">Telefóno</label>
            <input
                className="controls"
                type="text"
                value={Fono}
                placeholder="Numero de telefono"
                onChange={(e) => setFono(e.target.value)}
                id="fono_remitente"
                required
            />
            <label className="Info_campo" htmlFor="direccionRecogida">
                Reparto a domicilio
            </label>
            <select
                className="controls"
                value={Reparto_a_domicilio}
                onChange={(e) => setReparto_a_domicilio(e.target.value === "true")}
            >
                <option disabled value="">
                Seleccione una opción
                </option>
                <option value="true">Sí</option>
                <option value="false">No</option>
            </select>
            
            <BotonError mensaje="hola mundo"></BotonError>
            <BotonNavegar paginaAntes="/IngresoDatosRemitente"/>
            

        </form>
    )
}

