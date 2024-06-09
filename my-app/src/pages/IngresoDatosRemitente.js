import React, { useState, useEffect } from "react";
import { format } from "date-fns";
import "../Formulario/formularioCSS.css";
import "../Formulario/ButtonStyle.css";
import { BotonNavegar } from "../components/BotonNavegar";
import { useNavigate } from 'react-router-dom';
import { BotonError } from "../components/BotonError";

export function IngresoDatosRemitente() {
    const [rut_remitente, setRut_remitente] = useState("")
    const [remitente, setRemitente] = useState("");
    const [correo, setEmail] = useState("");
    const [recogida_a_domicilio, setRecogidaADomicilio] = useState(false);
    const [direccion_remitente, setDireccion_recogida] = useState("");
    const [remitenteId, setRemitenteId] = useState(null);  // ID por defecto

    const navigate = useNavigate();

    const [mensajeError, setMensajeError] = useState("");

    const redirectToPage = () => {
        navigate('/IngresoDatosDestinatario');
    };
    const validarCorreo = (email) => {
        const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return regex.test(email);
    };
    const validarRut = (rut) => {
        const regex = /^(\d{1,2}(?:[\.]?\d{3}){2}-[\dkK])$/;
        return regex.test(rut_remitente)
    };
    const handleSubmit = async (e) => {
        e.preventDefault();

        if (!validarCorreo(correo)) {
            setMensajeError("Por favor, ingrese un correo electrónico válido.");
            return;
        }
        if (!validarRut(rut_remitente)) {
            setMensajeError("Por favor, ingrese un RUT válido.")
            return;
        }

        const responseClient = await fetch(`http://127.0.0.1:5000/clientes/${rut_remitente}`);
        const data = await responseClient.json();

        if (responseClient.status === 404) {
            // Crea al cliente
            const res = await fetch("http://127.0.0.1:5000/clientes", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({
                    rut: rut_remitente,
                    nombre: remitente
                }),
            });

            if (res.ok) {
                // Crear Remitente
                const resRemitente = await fetch("http://127.0.0.1:5000/remitentes", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                    },
                    body: JSON.stringify({
                        rut_remitente: rut_remitente,
                        correo: correo,
                        direccion: direccion_remitente
                    }),
                });

                if (resRemitente.ok) {
                    redirectToPage();
                } else {
                    setMensajeError('Error al crear remitente:' + await resRemitente.text());
                }
            } else {
                setMensajeError('Error al crear el Cliente:' + await res.text());
            }
        } else {
            // Cliente existe entonces se crea un remitente con el rut del cliente
            const resRemitente = await fetch("http://127.0.0.1:5000/remitentes", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({
                    rut_remitente: rut_remitente,
                    correo: correo,
                    direccion: direccion_remitente
                }),
            });
        }
    };


    return (
        <form className="form-register" id="div_remitente" onSubmit={handleSubmit}>
            <h2>Datos Remitente</h2>

            <label className="info_campo" htmlFor="nombre">Ingrese su RUT</label>
            <input
                className="controls"
                type="text"
                value={rut_remitente}
                placeholder="Ingrese su nombre"
                onChange={(e) => setRut_remitente(e.target.value)}
                id="nombre"
                required
            />
            <label className="info_campo" htmlFor="nombre">Nombre completo</label>
            <input
                className="controls"
                type="text"
                value={remitente}
                placeholder="Ingrese su nombre"
                onChange={(e) => setRemitente(e.target.value)}
                id="nombre"
                required
            />
            <label className="info_campo" htmlFor="correo">Correo electronico</label>
            <input
                className="controls"
                type="email"
                value={correo}
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
                value={recogida_a_domicilio}
                onChange={(e) => setRecogidaADomicilio(e.target.value === "true")}
            >
                <option disabled value="">
                    Seleccione una opción
                </option>
                <option value="true">Sí</option>
                <option value="false">No</option>
            </select>
            <label className="info_campo">Ingrese su dirección</label>
            <input
                className="controls"
                type="text"
                value={direccion_remitente}
                placeholder="Ingrese su dirección de recogida"
                onChange={(e) => setDireccion_recogida(e.target.value)}
            />
            <BotonError mensaje={mensajeError} />
            <BotonNavegar paginaAntes="/" botonsiguientetexto="siguiente"/>
        </form>
    )
}