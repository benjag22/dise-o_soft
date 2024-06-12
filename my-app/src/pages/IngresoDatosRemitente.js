import React, { useState } from "react";
import "../Formulario/formularioCSS.css";
import "../Formulario/ButtonStyle.css";
import { BotonNavegar } from "../components/BotonNavegar";
import { useNavigate, useLocation } from 'react-router-dom';
import { BotonError } from "../components/BotonError";

export function IngresoDatosRemitente() {
    const navigate = useNavigate();
    const [rut_remitente, setRut_remitente] = useState("")
    const [nombreRemitente, setNombreRemitente] = useState("");
    const [apellidoPaternoRemitente, setApellidoPaternoRemitente] = useState("");
    const [apellidoMaternoRemitente, setApellidoMaternoRemitente] = useState("");


    const [correo, setEmail] = useState("");
    const [direccion_remitente, setDireccion_recogida] = useState("");
    const [remitenteId, setRemitenteId] = useState(null);
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
            setMensajeError("Por favor, ingrese un RUT válido.");
            return;
        }

        try {
            // Primero, buscar si el remitente ya existe
            let responseBuscar = await fetch(`http://127.0.0.1:5000/remitentes/buscar?rut=${rut_remitente}&direccion=${direccion_remitente}&correo=${correo}`);
            
            if (responseBuscar.ok) {
                const dataRemitente = await responseBuscar.json();
                setRemitenteId(dataRemitente.id);
                navigate('/IngresoDatosDestinatario', { state: { remitenteId: dataRemitente.id } });
            } else if (responseBuscar.status === 404) {
                // Cliente no encontrado, entonces crearlo
                let responseCliente = await fetch(`http://127.0.0.1:5000/clientes/${rut_remitente}`);
                let dataCliente = await responseCliente.json();

                if (responseCliente.status === 404) {
                    // Crea al cliente
                    let res = await fetch("http://127.0.0.1:5000/clientes", {
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
                        let resRemitente = await fetch("http://127.0.0.1:5000/remitentes", {
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
                            // Buscar el remitente creado para obtener su ID
                            responseBuscar = await fetch(`http://127.0.0.1:5000/remitentes/buscar?rut=${rut_remitente}&direccion=${direccion_remitente}&correo=${correo}`);
                            const dataRemitente = await responseBuscar.json();
                            setRemitenteId(dataRemitente.id);
                            navigate('/IngresoDatosDestinatario', { state: { remitenteId: dataRemitente.id } });
                        } else {
                            console.error('Error al crear remitente:', await resRemitente.text());
                        }
                    } else {
                        console.error('Error al crear el Cliente:', await res.text());
                    }
                } else {
                    // Cliente existe, crear remitente
                    let resRemitente = await fetch("http://127.0.0.1:5000/remitentes", {
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
                        // Buscar el remitente creado para obtener su ID
                        responseBuscar = await fetch(`http://127.0.0.1:5000/remitentes/buscar?rut=${rut_remitente}&direccion=${direccion_remitente}&correo=${correo}`);
                        const dataRemitente = await responseBuscar.json();
                        setRemitenteId(dataRemitente.id);
                        navigate('/IngresoDatosDestinatario', { state: { remitenteId: dataRemitente.id } });
                    } else {
                        console.error('Error al crear remitente:', await resRemitente.text());
                    }
                }
            } else {
                console.error('Error al buscar remitente:', await responseBuscar.text());
            }
        } catch (error) {
            setMensajeError(error.message);
        }
    };

    return (
        <>
            <form className="form-register" id="div_remitente" onSubmit={handleSubmit}>
                <h2>Datos Remitente</h2>

                <label className="info_campo" htmlFor="rut">Ingrese su RUT</label>
                <input
                    className="controls"
                    type="text"
                    value={rut_remitente}
                    placeholder="Ingrese su RUT"
                    onChange={(e) => setRut_remitente(e.target.value)}
                    id="rut"
                    required
                />
                <label className="info_campo" htmlFor="nombre">Nombre</label>
                <input
                    className="controls"
                    type="text"
                    value={nombreRemitente}
                    placeholder="Ingrese su nombre"
                    onChange={(e) => setRemitente(e.target.value)}
                    id="nombre"
                    required
                />

                <label className="info_campo" htmlFor="Apellido paterno">Apellido paterno</label>
                <input
                    className="controls"
                    type="text"
                    value={apellidoPaternoRemitente}
                    placeholder="Ingrese su apellido paterno"
                    onChange={(e) => setRemitente(e.target.value)}
                    id="Apellido paterno"
                    required
                />
                <label className="info_campo" htmlFor="apellido materno">Apellido materno</label>
                <input
                    className="controls"
                    type="text"
                    value={apellidoMaternoRemitente}
                    placeholder="Ingrese su Apellido materno"
                    onChange={(e) => setRemitente(e.target.value)}
                    id="Apellido materno"
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
        </>
    )
}