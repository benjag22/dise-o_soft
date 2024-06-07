import React from 'react';
import { useNavigate } from 'react-router-dom';
import BuscarEnvio from '../Otros/BuscarEnvio';
import './Home.css';

export default function Home() {
  const navigate = useNavigate();

  const irAEnviosPorPagar = () => {
    navigate('/enviosPorPagar');
  };

  const irAcrearEnvio = () => {
    navigate('/IngresoDatosRemitente');
  };

  return (
    <div className="home-container">
      <h1>Proyecto de envios</h1>
      <br></br>
      <br></br>
      <br></br>

      <BuscarEnvio />
      <br></br>
      <br></br>
      <br></br>
      <br></br>
      
      <div className="button-container">
        <button onClick={irAEnviosPorPagar}>Ver Envíos</button>
        <button onClick={irAcrearEnvio}>Crear Envío</button>
      </div>
    </div>
  );
}