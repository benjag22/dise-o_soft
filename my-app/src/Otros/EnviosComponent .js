import React, { useState, useEffect } from "react";
import { useNavigate } from 'react-router-dom';
import { GetEnvios } from "./GetEnvios";
import "./EnviosComponentStyles.css";

const EnviosComponent = () => {
  const [envios, setEnvios] = useState([]);

  useEffect(() => {
    const fetchEnvios = async () => {
      const enviosData = await GetEnvios();
      setEnvios(enviosData);
    };

    fetchEnvios();
  }, []);

  const navigate = useNavigate();

  const handleDetailClick = (envioId) => {
    navigate(`/detalle-envio/${envioId}`);
  }

  return (
    <div className="Eenvios-container">
      <br>
      </br>
      <br>
      </br>
      <br>
      </br>
      <h1>Envíos por pagar</h1>
      <ul className="Elista-envio">
        {envios.map((envio) => (
          <li key={envio.id_envio} className="Eenvio-item"> 
            <div className="Eenvio-info">
              <p><strong>Número de Envío:</strong> {envio.id_envio}</p> 
              <p><strong>Nombre del Remitente:</strong> {envio.remitente.nombre}</p>
              <p><strong>Correo del Remitente:</strong> {envio.remitente.correo}</p>
              <p><strong>Nombre del Destinatario:</strong> {envio.destinatario.nombre}</p>
              <p><strong>Correo del Destinatario:</strong> {envio.destinatario.correo}</p>
              <p><strong>Destino:</strong> {envio.destinatario.direccion}</p>
            </div>
            <div className="Edetalles-envio">
              <button className="Edetalles-button" onClick={() => handleDetailClick(envio.id_envio)}>
                Detalles
              </button>
            </div>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default EnviosComponent;
