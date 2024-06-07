import React, { useState } from "react";
import "../Formulario/formularioCSS.css";
import "../Formulario/ButtonStyle.css";
import { BotonNavegar } from "../components/BotonNavegar";
import { useNavigate } from 'react-router-dom';
import { BotonError } from "../components/BotonError";

export function IngresoDatosDestinatario() {
    const [destinatario, setDestinatario] = useState("");
    const [rutDestinatario, setRutDestinatario] = useState("");
    const [fono, setFono] = useState("");
    const [direccion, setDireccion] = useState("");

    const navigate = useNavigate();

    const validarRut = (rut) => {
        const regex = /^(\d{1,2}(?:[\.]?\d{3}){2}-[\dkK])$/;
        return regex.test(rut);
    };

    const handleSubmit = async (e) => {
        e.preventDefault();

        if (!validarRut(rutDestinatario)) {
            alert("Por favor, ingrese un RUT válido.");
            return;
        }

        const responseClient = await fetch(`http://127.0.0.1:5000/clientes/${rutDestinatario}`);
        const data = await responseClient.json();

        if (responseClient.status === 404) {
            // Crear cliente
            const res = await fetch("http://127.0.0.1:5000/clientes", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({
                    rut: rutDestinatario,
                    nombre: destinatario
                }),
            });

            if (res.ok) {
                // Crear destinatario
                const resDestinatario = await fetch("http://127.0.0.1:5000/destinatarios", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                    },
                    body: JSON.stringify({
                        rut_destinatario: rutDestinatario,
                        telefono: fono,
                        direccion: direccion
                    }),
                });

                if (resDestinatario.ok) {
                    navigate('/IngresoDatosDeEnvio');
                } else {
                    console.error('Error al crear destinatario:', await resDestinatario.text());
                }
            } else {
                console.error('Error al crear el Cliente:', await res.text());
            }
        } else {
            // Cliente existe entonces se crea un destinatario con el rut del cliente
            const resDestinatario = await fetch("http://127.0.0.1:5000/destinatarios", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({
                    rut_destinatario: rutDestinatario,
                    telefono: fono,
                    direccion: direccion
                }),
            });
            if (resDestinatario.ok) {
                navigate('/IngresoDatosDeEnvio');
            } else {
                console.error('Error al crear destinatario:', await resDestinatario.text());
            }
        }
    };

    return (
        <form className="form-register" id="div_envio" onSubmit={handleSubmit}>
            <h4>Datos del destinatario</h4>
            <label className="info_campo" htmlFor="nombre_destinatario">Nombre destinatario</label>
            <input
                className="controls"
                type="text"
                value={destinatario}
                placeholder="Ingrese nombre del destinatario"
                onChange={(e) => setDestinatario(e.target.value)}
                id="nombre_destinatario"
                required
            />
            <label className="info_campo" htmlFor="rut_destinatario">R.U.T</label>
            <input
                className="controls"
                type="text"
                value={rutDestinatario}
                placeholder="Ingrese Rut"
                onChange={(e) => setRutDestinatario(e.target.value)}
                id="rut_destinatario"
                required
            />
            <label className="info_campo" htmlFor="fono_remitente">Telefóno</label>
            <input
                className="controls"
                type="text"
                value={fono}
                placeholder="Numero de telefono"
                onChange={(e) => setFono(e.target.value)}
                id="fono_remitente"
                required
            />
            <label className="info_campo" htmlFor="direccion">Dirección</label>
            <input
                className="controls"
                type="text"
                value={direccion}
                placeholder="Ingrese dirección"
                onChange={(e) => setDireccion(e.target.value)}
                id="direccion"
                required
            />
            {/*<label className="Info_campo" htmlFor="repartoADomicilio">
                Reparto a domicilio
            </label>
            <select
                className="controls"
                value={repartoADomicilio}
                onChange={(e) => setRepartoADomicilio(e.target.value === "true")}
            >
                <option disabled value="">
                    Seleccione una opción
                </option>
                <option value="true">Sí</option>
                <option value="false">No</option>
            </select>*/}

            <BotonError mensaje="hola mundo" />
            <BotonNavegar paginaAntes="/IngresoDatosRemitente" />
        </form>
    );
}

