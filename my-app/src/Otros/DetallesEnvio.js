import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import GetDetalleEnvio from './GetDetalleEnvio';
import './DetallesEnvioStyles.css';

const DetallesEnvio = () => {
  const { id } = useParams();
  const [envio, setEnvio] = useState(null);

  useEffect(() => {
    const fetchEnvioDetails = async () => {
      const envioData = await GetDetalleEnvio(id);
      setEnvio(envioData);
    };

    fetchEnvioDetails();
  }, [id]);

  if (!envio) {
    return <div>No se encontro el envio</div>;
  }

  return (
    <div className="detalles-envio-container">
      <h1>Detalles del Envío</h1>
      <p><strong>Número de Envío:</strong> {envio.id}</p>
      <p><strong>Remitente:</strong> {envio.remitente}</p>
      <p><strong>Destinatario:</strong> {envio.destinatario}</p>
      <p><strong>Teléfono:</strong> {envio.fono}</p>
      <p><strong>Dirección de Envío:</strong> {envio.direccionEnvio}</p>
      <p><strong>Ciudad:</strong> {envio.ciudad}</p>
      <p><strong>Tipo de Envío:</strong> {envio.tipoEnvio}</p>
      <p><strong>Correo:</strong> {envio.correo}</p>
      <p><strong>Por Pagar:</strong> {envio.porPagar ? 'Sí' : 'No'}</p>
      <p><strong>Fecha de Recepción:</strong> {envio.fechaRecepcion}</p>
      <p><strong>Código Postal:</strong> {envio.codigoPostal}</p>
      <p><strong>Es Sobre:</strong> {envio.esSobre ? 'Sí' : 'No'}</p>
      <p><strong>Peso:</strong> {envio.peso} kg</p>
      <p><strong>Recogida a Domicilio:</strong> {envio.recogidaADomicilio ? 'Sí' : 'No'}</p>
      <p><strong>Dirección del Remitente:</strong> {envio.direccionRemitente}</p>
      <p><strong>Reparto a Domicilio:</strong> {envio.repartoADomicilio ? 'Sí' : 'No'}</p>
      <p><strong>RUT Destinatario:</strong> {envio.rutDestinatario}</p>
      <p><strong>Pagado:</strong> {envio.pagado ? 'Sí' : 'No'}</p>
      <p><strong>Entregado:</strong> {envio.entregado ? 'Sí' : 'No'}</p>
    </div>
  );
};

export default DetallesEnvio;
