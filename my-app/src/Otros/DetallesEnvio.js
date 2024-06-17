import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import GetDetalleEnvio from './GetDetalleEnvio';
import "./DetallesEnvioStyles.css";

const DetalleEnvio = () => {
  const { envioId } = useParams();
  const [envio, setEnvio] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [preciosDetallados, setPreciosDetallados] = useState(null);
  const [precioRecogidaDomicilio, setPrecioRecogidaDomicilio] = useState(0)
  const [precioRepartoDomicilio, setPrecioRepartoDomicilio] = useState(0)
  const [precioEnvio, setPrecioEnvio] = useState(0)
  const [totalConIva, setTotaConIva] = useState(0)
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

          const response = await fetch(`http://127.0.0.1:5000/historial/${envioId}`);
          const historialData = await response.json();
          
          if (response.ok) {
            setHistorialEstados(historialData.map(h => ({
              estado: h.estado,
              fechaHora: new Date(h.fecha_mod).toLocaleString(),
            })));
          } else {
            setError(historialData.mensaje || 'Error al cargar el historial');
          }
          const preciosResponse = await fetch(`http://127.0.0.1:5000/calcular_precio/${envioId}`);
          const preciosData = await preciosResponse.json();
          if (preciosResponse.ok) {
            console.log(preciosData.precios_detallados)
            setPreciosDetallados(preciosData);
            setPrecioRecogidaDomicilio(parseInt(preciosData.precios_detallados.precio_por_recogida_a_domicilio))
            setPrecioRepartoDomicilio(parseInt(preciosData.precios_detallados.precio_por_reparto_a_domicilio))
            setPrecioEnvio(parseInt(preciosData.precios_detallados.precio_por_tipo_de_envio))
            setTotaConIva(parseInt(preciosData.precios_detallados.total_con_IVA))
          } else {
            setError(preciosData.error || 'Error al calcular los precios detallados');
          }
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

  const avanzarEstado = async () => {
    if (estadoActual < estadosEnvio.length - 1) {
      const nuevoEstado = estadosEnvio[estadoActual + 1];
      const nuevoHistorial = {
        fecha_mod: new Date().toISOString(),
        estado: nuevoEstado,
        id_envio: envioId
      };
      try {
        const response = await fetch('http://127.0.0.1:5000/historial', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(nuevoHistorial)
        });

        if (response.ok) {
          setEstadoActual(estadoActual + 1);
          setHistorialEstados([
            ...historialEstados,
            { estado: nuevoEstado, fechaHora: new Date().toLocaleString() },
          ]);
        } else {
          const errorData = await response.json();
          setError(errorData.error || 'Error al avanzar el estado');
        }
      } catch (error) {
        setError('Error al comunicarse con el servidor');
      }
    }
  };

  return (
    <div className="detalle-envio-container">
      <h1>Detalle del Envío</h1>

      {error && <div className="mensaje-de-error">{error}</div>}

      <div className="envio-info">
        <div className="datos-principales">
          <p><strong>ID Envío:</strong> {envio?.id_envio}</p>
          <p><strong>Estado:</strong> {estadosEnvio[estadoActual]}</p>
          <p><strong>Remitente:</strong> {envio?.remitente.nombre}</p>
          <p><strong>Destinatario:</strong> {envio?.destinatario.nombre}</p>
          {preciosDetallados && (
            <div className="precios-detallados">
              <h2>Precios Detallados</h2>
              <p><strong>Precio por tipo de envío:</strong> {precioEnvio}</p>
              {preciosDetallados.precios_detallados.precio_por_recogida_a_domicilio && (
                <p><strong>Precio por recogida a domicilio:</strong> {precioRecogidaDomicilio}</p>
              )}
              {preciosDetallados.precios_detallados.precio_por_reparto_a_domicilio && (
                <p><strong>Precio por reparto a domicilio:</strong> {precioRepartoDomicilio}</p>
              )}
              <p><strong>Total + IVA:</strong> {totalConIva}</p>
            </div>
          )}
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
