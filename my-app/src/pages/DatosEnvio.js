import React, { useState, useEffect } from "react";

import { useNavigate, useLocation } from 'react-router-dom';
import "../Formulario/formularioCSS.css";
import "../Formulario/ButtonStyle.css";
import { BotonNavegar } from "../components/BotonNavegar"

export function DatosEnvio() {

    //Definicion useStates para paquete
    const [tipo, setEs_sobre] = useState("");
    const [peso, setPeso] = useState(0.0);

    //Definicion useStates para envio
    const [cod_postal, setCodigo_postal] = useState("");
    const [tipo_envio, setTipo_de_envio] = useState("");
    const [pagado, setPagado] = useState(false);
    const [recogida_a_domicilio, setRecogida_a_domicilio] = useState(false);
    const [por_pagar, setPor_pagar] = useState(false);
    const [reparto_a_domicilio, setReparto_a_domicilio] = useState(false);


    const navigate = useNavigate();
    //funciones varias para el jsx

    const redirectToPage = () => {
        navigate('/IngresoDatosRemitente');
    };
    const handleSubmit = async (e) => {
        e.preventDefault();

        const paqueteRes = await fetch("http://127.0.0.1:5000/paquetes", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                tipo,
                peso:parseFloat(peso)
            }),
        });

        const envioRes = await fetch("http://127.0.0.1:5000/envios", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                cod_postal,
                tipo_envio,
                pagado,
                recogida_a_domicilio,
                reparto_a_domicilio,
                por_pagar
                /*id_paquete,
                id_remitente:remitenteId,
                id_destinatario:destinatarioId*/
            }),
        });
        navigate('/IngresoDatosRemitente');
    };
    const handleViewJson = () => {
        const data = {
            tipo,
            peso,
            cod_postal,
            tipo_envio,
            pagado,
            recogida_a_domicilio,
            reparto_a_domicilio,
            por_pagar
        };
        alert(JSON.stringify(data, null, 2));
    };
    
    return (
        <div>
        <pre>
                {JSON.stringify({
                    tipo,
                    peso,
                    cod_postal,
                    tipo_envio,
                    pagado,
                    recogida_a_domicilio,
                    reparto_a_domicilio,
                    por_pagar
                }, null, 2)}
            </pre>
         
        <form className="form-register" id="div_envio" onSubmit={redirectToPage}>
            <h4>Datos de envio</h4>
            <label className="info_campo">Código postal</label>
            <input
                className="controls"
                type="text"
                value={cod_postal}
                placeholder="Ingrese codigo postal"
                onChange={(e) => setCodigo_postal(e.target.value)}
                required
            />
            <label className="info_campo" htmlFor="tipo_entrega">
                Tipo de entrega
            </label>
            <select
                name="tipo_entrega"
                className="controls"
                value={tipo_envio}
                onChange={(e) => setTipo_de_envio(e.target.value)}
            >
                <option disabled value="">
                Selecciona una opción
                </option>
                <option value="Entrega en el dia">Entrega en el día</option>
                <option value="Entrega rapida">Entrega rápida</option>
                <option value="Entrega normal">Entrega normal</option>
            </select>
            <label className="info_campo" htmlFor="tipo_paquete">
                    Tipo de paquete
                </label>
                <select
                    name="tipo_paquete"
                    className="controls"
                    value={tipo}
                    onChange={(e) => setEs_sobre(e.target.value)}
                >
                    <option disabled value="">
                        Selecciona una opción
                    </option>
                    <option value="sobre">Sobre</option>
                    <option value="encomienda">Encomienda</option>
                </select>
                {tipo === "encomienda" && (
                    <React.Fragment>
                        <label className="info_campo" htmlFor="tipo_paquete">
                            Indique peso en KG
                        </label>
                        <input
                            className="controls"
                            type="text"
                            value={peso}
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
                value={por_pagar ? "true" : "false"}
                onChange={(e) => setPor_pagar(e.target.value === "true")}
            >
                <option disabled selected hidden value="">
                Selecciona una opción
                </option>
                <option value="false">Remitente</option>
                <option value="true">Destinatario</option>
            </select>
            <label className="etiquetas" htmlFor="pago">Recogida a domicilio</label>
            <select
                name="pago"
                className="controls"
                value={recogida_a_domicilio ? "true" : "false"}
                onChange={(e) => setRecogida_a_domicilio(e.target.value === "true")}>
                <option disabled selected hidden value="">
                Selecciona una opción
                </option>
                <option value="true">Si</option>
                <option value="false">No</option>
            </select>
            <label className="etiquetas" htmlFor="pago">Reparto a domicilio</label>
            <select
                name="pago"
                className="controls"
                value={reparto_a_domicilio ? "true" : "false"}
                onChange={(e) => setReparto_a_domicilio(e.target.value === "true")}>
                <option disabled selected hidden value="">
                Selecciona una opción
                </option>
                <option value="true">Si</option>
                <option value="false">No</option>
            </select>

            <BotonNavegar paginaAntes="/IngresoDatosDestinatario"/>

        </form>
        </div>
    )
}

