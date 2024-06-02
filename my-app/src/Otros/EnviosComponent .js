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
    <div className="envios-container">
      <h1>Envíos por pagar</h1>
      <ul className="lista-envio">
        {envios.map((envio) => (
          <li key={envio.id} className="envio-item">
            <div className="envio-info">
              <p><strong>Número de Envío:</strong> {envio.id}</p>
              <p><strong>Destinatario:</strong> {envio.destinatario}</p>
              <p><strong>Destino:</strong> {envio.ciudad}</p>
            </div>
            <div className="detalles-envio">
              <button className="detalles-button" onClick={() => handleDetailClick(envio.id)}>
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
