import React from 'react';
import { useNavigate } from 'react-router-dom';
import BuscarEnvio from '../Otros/BuscarEnvio';
import './Home.css';
import logo from '../components/assets/logo.png'

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
      <h1>Empresa de envios generica</h1>
      <img src={logo} width="250"/>
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