import React, { useState } from "react";
import "../Formulario/ButtonStyle.css";
import "../Formulario/formularioCSS.css";
import { BotonNavegar } from "../components/BotonNavegar";
import { useNavigate, useLocation } from 'react-router-dom';
import { BotonError } from "../components/BotonError";

export function IngresoDatosDestinatario() {
    const [nombreDestinatario, setnombreDestinatario] = useState("");
    const [apellidoPaternoDestinatario, setapellidoPaternoDestinatario] = useState("");
    const [apellidoMaternoDestinatario, setapellidoMaternoDestinatario] = useState("");
    const [rutDestinatario, setRutDestinatario] = useState("");
    const [telefono, setFono] = useState("");
    const [correo, setCorreo] = useState("")
    const [direccion, setDireccion] = useState("");
    const [mensajeError, setMensajeError] = useState("");

    const navigate = useNavigate();
    const location = useLocation();
    const remitenteId = location.state?.remitenteId;

    const validarRut = (rut) => {
        const regex = /^(\d{1,2}(?:[\.]?\d{3}){2}-[\dkK])$/;
        return regex.test(rut);
    };

    const validarTelefono = (fono) =>{
        const regex = /^[0-9,$]*$/;
        return regex.test(fono);

    }
    const validarCorreo = (email) => {
        const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return regex.test(email);
    };

    const handleSubmit = async (e) => {
        e.preventDefault();

        if (!validarCorreo(correo)) {
            setMensajeError("Por favor, ingrese un correo electrónico válido.");
            return;
        }
    
        if (!validarRut(rutDestinatario)) {
            setMensajeError("Por favor, ingrese un RUT válido.");
            return;
        }
        if (!validarTelefono(telefono)) {
            setMensajeError("Por favor, ingrese un teléfono válido.");
            return;
        }
    
        try {
            // Primero, buscar si el destinatario ya existe
            let responseBuscar = await fetch(`http://127.0.0.1:5000/destinatarios/buscar?rut=${rutDestinatario}&direccion=${direccion}&telefono=${telefono}&correo=${correo}`);
            
            if (responseBuscar.ok) {
                const dataDestinatario = await responseBuscar.json();
                navigate('/IngresoDatosDeEnvio', { state: { remitenteId, destinatarioId: dataDestinatario.id } });
            } else if (responseBuscar.status === 404) {
                // Cliente no encontrado, entonces crearlo
                let responseCliente = await fetch(`http://127.0.0.1:5000/clientes/${rutDestinatario}`);
                let dataCliente = await responseCliente.json();
    
                if (responseCliente.status === 404) {
                    // Crear cliente
                    let res = await fetch("http://127.0.0.1:5000/clientes", {
                        method: "POST",
                        headers: {
                            "Content-Type": "application/json",
                        },
                        body: JSON.stringify({
                            rut: rutDestinatario,
                            nombre: nombreDestinatario,
                            ap_paterno: apellidoPaternoDestinatario,
                            ap_materno: apellidoMaternoDestinatario,
                            estado: 'activo'
                        }),
                    });
    
                    if (res.ok) {
                        // Crear destinatario
                        let resDestinatario = await fetch("http://127.0.0.1:5000/destinatarios", {
                            method: "POST",
                            headers: {
                                "Content-Type": "application/json",
                            },
                            body: JSON.stringify({
                                rut_destinatario: rutDestinatario,
                                telefono: telefono,
                                direccion: direccion,
                                correo: correo 
                            }),
                        });
    
                        if (resDestinatario.ok) {
                            // Buscar el destinatario creado para obtener su ID
                            responseBuscar = await fetch(`http://127.0.0.1:5000/destinatarios/buscar?rut=${rutDestinatario}&direccion=${direccion}&telefono=${telefono}&correo=${correo}`);
                            const dataDestinatario = await responseBuscar.json();
                            navigate('/IngresoDatosDeEnvio', { state: { remitenteId, destinatarioId: dataDestinatario.id } });
                        } else {
                            setMensajeError('Error al crear destinatario:' + await resDestinatario.text());
                        }
                    } else {
                        setMensajeError('Error al crear el Cliente:' + await res.text());
                    }
                } else {
                    // Cliente existe, crear destinatario
                    let resDestinatario = await fetch("http://127.0.0.1:5000/destinatarios", {
                        method: "POST",
                        headers: {
                            "Content-Type": "application/json",
                        },
                        body: JSON.stringify({
                            rut_destinatario: rutDestinatario,
                            telefono: telefono,
                            direccion: direccion,
                            correo: correo // Este campo puede agregarlo si es necesario
                        }),
                    });
    
                    if (resDestinatario.ok) {
                        // Buscar el destinatario creado para obtener su ID
                        responseBuscar = await fetch(`http://127.0.0.1:5000/destinatarios/buscar?rut=${rutDestinatario}&direccion=${direccion}&telefono=${telefono}&correo=${correo}`);
                        const dataDestinatario = await responseBuscar.json();
                        navigate('/IngresoDatosDeEnvio', { state: { remitenteId, destinatarioId: dataDestinatario.id } });
                    } else {
                        setMensajeError('Error al crear destinatario:' + await resDestinatario.text());
                    }
                }
            } else {
                setMensajeError('Error al buscar destinatario:' + await responseBuscar.text());
            }
        } catch (error) {
            setMensajeError(error.message);
        }
    };
    
    return (
        <form className="form-register" id="div_envio" onSubmit={handleSubmit}>
            <h4>Datos del destinatario</h4>
            <label className="info_campo" htmlFor="nombre">Nombre</label>
                <input
                    className="controls"
                    type="text"
                    value={nombreDestinatario}
                    placeholder="Ingrese su nombre"
                    onChange={(e) => setnombreDestinatario(e.target.value)}
                    id="nombre"
                    required
                />

                <label className="info_campo" htmlFor="Apellido paterno">Apellido paterno</label>
                <input
                    className="controls"
                    type="text"
                    value={apellidoPaternoDestinatario}
                    placeholder="Ingrese su apellido paterno"
                    onChange={(e) => setapellidoPaternoDestinatario(e.target.value)}
                    id="Apellido paterno"
                    required
                />
                <label className="info_campo" htmlFor="Apellido materno">Apellido materno</label>
                <input
                    className="controls"
                    type="text"
                    value={apellidoMaternoDestinatario}
                    placeholder="Ingrese su Apellido materno"
                    onChange={(e) => setapellidoMaternoDestinatario(e.target.value)}
                    id="Apellido materno"
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
                value={telefono}
                placeholder="Numero de telefono"
                onChange={(e) => setFono(e.target.value)}
                id="fono_remitente"
                required
            />
            <label className="info_campo" htmlFor="correo">Correo</label>
            <input
                className="controls"
                type="text"
                value={correo}
                placeholder="Ingrese correo"
                onChange={(e) => setCorreo(e.target.value)}
                id="direccion"
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
            <BotonError mensaje={mensajeError} />
            <BotonNavegar paginaAntes="/IngresoDatosRemitente" />
        </form>
    );
}

