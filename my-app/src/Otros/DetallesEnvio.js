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

  const estadosEnvio = [
    "en preparación",
    "en tránsito",
    "en sucursal",
    "en reparto",
    "entregado"
  ];
  const [estadoActual, setEstadoActual] = useState(0); 
  const [historialEstados, setHistorialEstados] = useState([]);

  useEffect(() => {
    const fetchEnvio = async () => {
      try {
        const envioData = await GetDetalleEnvio(envioId);
        if (envioData) {
          setEnvio(envioData);
          setEstadoActual(estadosEnvio.indexOf(envioData.estado));
          setHistorialEstados([
            { estado: envioData.estado, fechaHora: new Date().toLocaleString() },
          ]);
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

  const avanzarEstado = () => {
    if (estadoActual < estadosEnvio.length - 1) {
      setEstadoActual(estadoActual + 1);
      setHistorialEstados([
        ...historialEstados,
        { estado: estadosEnvio[estadoActual + 1], fechaHora: new Date().toLocaleString() },
      ]);
    }
  };
  if (error) {
    return <div>{error}</div>;
  }

  return (
    <div className="detalle-envio-container">
      <h1>Detalle del Envío</h1>

      <div className="envio-info">
        <div className="datos-principales">
          <p><strong>ID Envío:</strong> {envio?.id_envio}</p>
          <p><strong>Estado:</strong> {estadosEnvio[estadoActual]}</p>
          <p><strong>Remitente:</strong> {envio?.remitente.nombre}</p>
          <p><strong>Destinatario:</strong> {envio?.destinatario.nombre}</p>
        </div>

        <div className="estados-envio">
          <h2>Historial de Estados</h2>
          <ul>
            {historialEstados.map((item, index) => (
              <li key={index}>
                {item.estado} - {item.fechaHora}
              </li>
            ))}
          </ul>
          {estadoActual < estadosEnvio.length - 1 && (
            <button onClick={avanzarEstado}>Avanzar Estado</button>
          )}
        </div>
      </div>
      <button className="volver-button" onClick={() => navigate(-1)}>Volver</button>
    </div>
  );
};

export default DetalleEnvio;
