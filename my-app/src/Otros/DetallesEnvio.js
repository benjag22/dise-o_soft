import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import GetDetalleEnvio from './GetDetalleEnvio';
import "./DetallesEnvioStyles.css";

const DetalleEnvio = () => {
  const { envioId } = useParams();
  const [envio, setEnvio] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchEnvio = async () => {
      try {
        const envioData = await GetDetalleEnvio(envioId);
        if (envioData) {
          setEnvio(envioData);
        } else {
          setError('No se encontraron detalles del envío');
        }
      } catch (error) {
        setError('Error al cargar los detalles del envío');
      } finally {
        setLoading(false);
      }
    };

    fetchEnvio();
  }, [envioId]);

  if (loading) {
    return <div>Loading...</div>;
  }

  if (error) {
    return <div>{error}</div>;
  }

  if (!envio) {
    return <div>No se encontraron detalles del envío</div>;
  }

  return (
    <div className="detalle-envio-container">
      <h1>Detalle del Envío</h1>
      <div className="envio-info">
        <p><strong>ID Envío:</strong> {envio.id_envio}</p>
        <p><strong>Estado:</strong> {envio.estado}</p>
        <p><strong>Tipo de Envío:</strong> {envio.tipo_envio}</p>
        <p><strong>Código Postal:</strong> {envio.codigo_postal}</p>
        <p><strong>Fecha de Recepción:</strong> {envio.fecha_recepcion}</p>
        <p><strong>Reparto a Domicilio:</strong> {envio.reparto_a_domicilio}</p>
        <p><strong>Pagado:</strong> {envio.pagado ? 'Sí' : 'No'}</p>
        <h2>Paquete</h2>
        <p><strong>ID Paquete:</strong> {envio.paquete.id_paquete}</p>
        <p><strong>Tipo:</strong> {envio.paquete.tipo}</p>
        <p><strong>Peso:</strong> {envio.paquete.peso} kg</p>
        <p><strong>Fecha de Ingreso:</strong> {envio.paquete.fecha_ingreso}</p>
        <h2>Remitente</h2>
        <p><strong>Nombre:</strong> {envio.remitente.nombre}</p>
        <p><strong>RUT:</strong> {envio.remitente.rut_remitente}</p>
        <p><strong>Dirección:</strong> {envio.remitente.direccion}</p>
        <p><strong>Correo:</strong> {envio.remitente.correo}</p>
        <h2>Destinatario</h2>
        <p><strong>Nombre:</strong> {envio.destinatario.nombre}</p>
        <p><strong>RUT:</strong> {envio.destinatario.rut_destinatario}</p>
        <p><strong>Teléfono:</strong> {envio.destinatario.telefono}</p>
        <p><strong>Dirección:</strong> {envio.destinatario.direccion}</p>
        <p><strong>Correo:</strong> {envio.destinatario.correo}</p>
      </div>
      <button onClick={() => navigate(-1)}>Volver</button>
    </div>
  );
};

export default DetalleEnvio;
