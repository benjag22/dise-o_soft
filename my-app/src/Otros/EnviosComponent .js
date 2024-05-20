import React, { useState, useEffect } from "react";
import { GetEnvios } from "./GetEnvios";
import "./EnviosComponentStyles.css";
import GetVerificacion from "./GetVerification";
import GetEntregado from "./GetEntregado";

const EnviosComponent = () => {
  const [envios, setEnvios] = useState([]);
  const [verificacionExitosa, setVerificacionExitosa] = useState(false); // Estado para controlar si la verificación ha sido exitosa

  useEffect(() => {
    const fetchEnvios = async () => {
      const enviosData = await GetEnvios();
      const enviosConEstado = enviosData.map((envio) => ({
        ...envio,
        verificacionVisible: false,
        entregado: false,
      }));
      setEnvios(enviosConEstado);
    };

    fetchEnvios();
  }, []);

  const toggleVerificacion = async (index) => {
    setEnvios((prevEnvios) => {
      const updatedEnvios = [...prevEnvios];
      updatedEnvios[index].verificacionVisible = !updatedEnvios[index].verificacionVisible;
      return updatedEnvios;
    });
  };

  const handleSubmit = (index) => {
    if (envios[index].verificacionVisible && verificacionExitosa) {
      setEnvios((prevEnvios) => {
        const updatedEnvios = [...prevEnvios];
        updatedEnvios[index].entregado = true;
        return updatedEnvios;
      });
    } else {
      alert("Debes verificar el envío antes de poder entregarlo.");
    }
  };

  return (
    <div className="envios-container">
      <h1>Envíos por pagar</h1>
      <ul>
        {envios.map((envio, index) => (
          <li key={index}>
            <p>Remitente: {envio.Remitente}</p>
            <p>Correo Remitente: {envio.Correo}</p>
            <p>Destinatario: {envio.Destinatario}</p>
            <p>Rut del destinatario: {envio.Rut_Destinatario}</p>
            <button onClick={() => toggleVerificacion(index)}>
              Verificar rut
            </button>
            {envio.verificacionVisible && <GetVerificacion className="verificacion" id={envio.id} rut={envio.Rut_Destinatario} />}
            {envio.verificacionVisible && <GetEntregado className="entregado" id={envio.id} Correo={envio.Correo} Destinatario={envio.Destinatario} />}
            {!envio.verificacionVisible && (
              <form onSubmit={() => handleSubmit(index)}>
                <button type="submit" disabled={!verificacionExitosa}>Marcar como entregado</button>
              </form>
            )}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default EnviosComponent;
